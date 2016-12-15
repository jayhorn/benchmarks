import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.nio.ByteBuffer;
import java.util.Queue;
import java.util.concurrent.PriorityBlockingQueue;

// Not vulnerable packet receive queues (UDP)
// 1 second per request max ten requests -> max response time ~10 seconds
public class Category10_not_vulnerable {
    private static DatagramSocket server;
    private static int bufferSize = Integer.SIZE;
    private static Queue<Cat10Request> requestQueue;
    private static final int maxQueueSize = 10;

    private static class Cat10Request implements Comparable<Cat10Request>{
        private InetAddress myIPAddress;
        private int myPort;
        private int myData;
        public Cat10Request(DatagramPacket packet){
            myIPAddress = packet.getAddress();
            myPort = packet.getPort();
            myData = ByteBuffer.wrap(packet.getData()).getInt();
        }
        public InetAddress getIPAddress(){return  myIPAddress;}
        public int getPort() {return myPort;}
        public int getData() {return myData;}
        @Override
        public int compareTo( Cat10Request ctr) {
            return Integer.compare(myData, ctr.getData());
        }
    }
    private static void startServer(){
        System.out.println("Server Started on port 5678");
        try {
            //Start server
            server = new DatagramSocket(5678);
            boolean queueStatus = true;
            while(true){
                //Get incoming requests
                DatagramPacket packetIn = new DatagramPacket(new byte[bufferSize], bufferSize);
                server.receive(packetIn);

                //If request queue not full add request to queue
                if(requestQueue.size() < maxQueueSize) {
                    queueStatus = requestQueue.offer(new Cat10Request(packetIn));
                }
                //If request queue full return -1
                if(requestQueue.size() >= maxQueueSize || !queueStatus){
                    respond(packetIn.getAddress(), packetIn.getPort(), -1);
                }
            }
        } catch(IOException e) {
            System.exit(-1);
        }
    }
    private static void processRequests(){
        System.out.println("Process Thread Started");
        try {
            Cat10Request c10Request;
            int request;
            int response;
            while(true){
                //Read request from request queue, process request and return 1
                c10Request = requestQueue.poll();
                if(c10Request != null){
                    request = c10Request.getData();
                    response = doRequest(request);
                    respond(c10Request.getIPAddress(), c10Request.getPort(), response);
                }
            }
        } catch(IOException e) {
            System.exit(-1);
        }
    }
    private static int doRequest(int request){
        for(int x = 0; x<70000000;x++){} //wait 1 second
        return 1;
    }
    private static void respond(InetAddress IPAddress, int port, int response) throws IOException {
        ByteBuffer bytesOut = ByteBuffer.allocate(bufferSize);
        bytesOut.putInt(response);
        DatagramPacket packetOut = new DatagramPacket(bytesOut.array(), bufferSize, IPAddress, port);
        server.send(packetOut);
    }
    public static void main (String[] args){
        requestQueue = new PriorityBlockingQueue<>();

        //Start Server Thread
        Thread t1 = new Thread(new Runnable() {
            @Override
            public void run() {
                startServer();
            }
        });
        t1.start();

        Thread t2 = new Thread(new Runnable() {
            @Override
            public void run() {
                processRequests();
            }
        });
        t2.start();
    }
}
