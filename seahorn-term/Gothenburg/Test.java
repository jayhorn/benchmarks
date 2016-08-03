import java.util.Random;

class Test {
  public static void main(String args[]) {
    Random r = new Random();
    int a = r.nextInt();
    int b = r.nextInt();
    int x = r.nextInt();
    int y = r.nextInt();
    if (x<=0 || y<=0) return;
    int counter = x+y;
    if (a == b) {
      while (x >= 0 || y >= 0) {
        x = x + a - b - 1;
        y = y + b - a - 1;
	counter--;
      }
    }
    assert (counter>=0);
  }
}
