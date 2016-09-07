import java.util.Random;

class Easy {
  public static void main(String args[]) {
    Random r = new Random();
    int x = 0;
    int y = 100;
    int z = r.nextInt();
    int counter = 40-x;
    while (x < 40) {
      if (z == 0) {
        x = x + 1;
      } else {
        x = x + 2;
      }
    counter--;  
    }
    assert (counter>=0);
  }
}
