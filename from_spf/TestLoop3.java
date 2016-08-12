public class TestLoop3 {
		  // safe inductive invariant: y + i <= x + j
		  public static void main(String[] args) {
		      int x,y,i,j;
		      x=i;
		      y=j;
		      while (x != 0){
		          x--;
		          y--;
		      }
		      if (i ==j )
		          assert(y <= 0);
		  }
}
