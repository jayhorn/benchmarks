import java.util.Random;

class MenloPark_true{
  public static void main(String args[]) {
    Random r = new Random();
    int x = r.nextInt();
    if (x < 0) return;
    int y = 100;
    int z = 1;
    int counter = x;
    while (x >= 0) {
      x = x - y;
      y = y - z;
      z = -z;
      counter--;
    }
    assert (x >=0 && counter>=0) || x < 0);
  }
}
