package challenge2onebucket;

import java.util.LinkedList;
import java.util.Random;


public class TestApp2 {

	 private static int char_counter = 0;
	 
	 //Interesting method for worst case complexity
	    private static boolean findEntry(LinkedList<String> ll,  char[] str) {
	        for (String s : ll) {
	         // char str_char [] = str.toCharArray(); // get second array of chars
	          char s_char [] = s.toCharArray(); // get second array of chars
	          if (myEquals(s_char, str)){
	        	  return true;
	          }
	        }
	        return false;
	    }
	    

     private static boolean myEquals(char v1[], char v2[]) {
         int n = v1.length;
         if (n == v2.length) {
        	 int i = 0;
        	 while (n-- != 0) {	
         		 char_counter += 1; 
        		 if (v1[i] != v2[i]){
        			 return false;
        		 }
        		 i++;
        	 }
        	 return true;
         }
         return false;
     }	
     
  public static void main(final java.lang.String[] args) {

    final int HASH_TABLE_SIZE = 1;
    int KEY_SIZE = 4;
    
    int N=Integer.parseInt(args[0]);
    LinkedList<String> ll = new LinkedList<String>();

    Random rand = new Random(42);
    
    for(int i=0;i<N;i++) {
      char[] input = new char[KEY_SIZE];
      for(int s = 0; s < input.length; s++) {
    	//input[s] = Debug.makeSymbolicChar("in"+i+s);
    	char c = (char)(rand.nextInt(26) + 'a');
        input[s] = c;
      }
      ll.add(new String(input));    
    }   

    char[] input = new char[KEY_SIZE];
    for(int s = 0; s < input.length; s++) {
      //input[s] = Debug.makeSymbolicChar("get"+s);
      char c = (char)(rand.nextInt(26) + 'a');
      input[s] = c;
    }
    findEntry(ll, input);
    
   
    assert(char_counter <= KEY_SIZE*N);  
    assert(false);

  }
}
