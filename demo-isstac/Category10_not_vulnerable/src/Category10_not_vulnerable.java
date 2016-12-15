import java.util.Random;

class Category10_not_vulnerable {

	public static void main(String args[]) {
		Random r = new Random();

		int queueSize = 0;
		int maxQueueSize = 10;

		Queue q = new Queue(maxQueueSize);

		while (true) {
			if (r.nextBoolean()) {
				// server
				if (q.size() < maxQueueSize) {
					q.offer(null);
				}
			} else {
				// processRequest
				if (q.size() > 0) {
					q.poll();
				}
			}
			assert (q.size() >= 0);
			assert (q.size() <= maxQueueSize);

			if (r.nextBoolean()) return;
		}
	}
}

class Queue {
	private int size = 0;
	private int maxQueueSize;
	
	public Queue(int maxSize) {
		this.maxQueueSize = maxSize;
	}

	public void offer(Cat10Request e) {
		if (size < maxQueueSize)
			size++;
	}

	public Cat10Request poll() {
		if (size > 0)
			size--;
		return null;
	}

	public int size() {
		return size;
	}
}


class Cat10Request {}
