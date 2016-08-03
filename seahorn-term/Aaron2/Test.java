import java.util.Random;

class Test {
  public static void main(String args[]) {
    Random r = new Random();
    int x = r.nextInt();
    int y = r.nextInt();
    int tx = r.nextInt();
    if (y>x) return;
    int counter = x-y+1;
    while (x >= y && tx >= 0) {
		if (r.nextBoolean()) {
			x = x - 1 - tx;
		} else {
			y = y + 1 + tx;
		}
      counter--;
    }
    assert (counter>=0);
  }
}
