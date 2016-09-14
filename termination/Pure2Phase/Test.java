import java.util.Random;

class Test {
  public static void main(String args[]) {
    Random r = new Random();
    int y = r.nextInt();
    int z = r.nextInt();
    int zorig = z;
    int yorig = y;
    int counter = zorig;
    while (z >= 0) {
      y = y - 1;
      if (y >= 0) {
      //  z = r.nextInt();
      } else {
        z = z - 1;
      }
      counter--;  
    }
    assert (counter<=zorig+1+yorig+1);
  }
}
