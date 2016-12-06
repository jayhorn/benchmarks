import java.util.Random;

class Category10_not_vulnerable {

	static int queueSize = 0;

	public static void main(String args[]) {
		//int queueSize = 0;
		int maxQueueSize = 10;
		Random r = new Random();

		while (true) {
			if (r.nextBoolean()) {
				// server
				if (queueSize < maxQueueSize) {
					queueSize++;
				}
			} else {
				// processRequest
				if (queueSize>0) {
					queueSize--;
				}
			}
			assert (queueSize <= maxQueueSize);

			if (r.nextBoolean()) return;
		}
	}
}
