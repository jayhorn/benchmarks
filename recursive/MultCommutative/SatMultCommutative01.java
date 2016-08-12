import java.util.Random;

public class SatMultCommutative01 {
	static int mult(int n, int m) {
	    if (m < 0) {
	        return mult(n, -m);
	    }
	    if (m == 0) {
	        return 0;
	    }
	    return n + mult(n, m - 1);
	}

	public static void main(String[] args) {
		Random rand = new Random(42);
	    int m = rand.nextInt();
	    if (m < 0 || m > 46340) {
	        return;
	    }
	    int n = rand.nextInt();
	    if (n < 0 || n > 46340) {
	        return;
	    }
	    int res1 = mult(m, n);
	    int res2 = mult(n, m);
	    if (res1 != res2 && m > 0 && n > 0) {
	    	assert false;
	    } else {
	        return;
	    }
	}
}
