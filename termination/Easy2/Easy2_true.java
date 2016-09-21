import java.util.Random;

class Easy2_true {
  public static void main(String args[]) {
    Random r = new Random();
    int x = 12;
    int y = 0;
    int z = r.nextInt();
    if (z <= 0) return;
    int counter = z;
    while (z > 0) {
      x = x + 1;
      y = y - 1;
      z = z - 1;
      counter--;
    }
    assert (counter>=0);
  }
}
