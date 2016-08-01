import java.util.Random;

public class FindEntry {

	static Random rand = new Random();

	static boolean equals(int m) {
		for (int i = 0; i < m; i++) {
			if (rand.nextBoolean()) {
				return false;
			}
		}
		return true;
	}
	
	public static void main(String args[]) {
		final int n = rand.nextInt(); 
		final int m = 2;//rand.nextInt();
		//assume(n > 0); assume (m > 0);
		if (n <= 0 || m <= 0) return; // assume. Is there a better way to do this?
		int r = n*m;
		for (int i = 0; i < n; i++) {
			
			r = r - 1;
			assert(r >= 0);
			
			if (equals(m)) {
				return;
			}
		}
		return;
	}
}
