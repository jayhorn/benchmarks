import java.util.Random;

class Mysore {
  public static void main(String args[]) {
    Random r = new Random();
    int x = r.nextInt();
    int c = r.nextInt();
    int counter = x+c;
    if (c >= 2) {
      while (x + c >= 0) {
        x = x - c;
        c = c + 1;
        counter--;
      }
    }
    assert (counter>=0);
  }
}
