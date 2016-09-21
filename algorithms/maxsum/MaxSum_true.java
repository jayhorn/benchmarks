// JayHorn-Option : -rta

import java.util.Random;

/**
 * @author Kasper Luckow
 *
 */
public class MaxSum_true {
  /**
   * Recursive maximum contiguous subsequence sum algorithm.
   * Finds maximum sum in subarray spanning a[left..right].
   * Does not attempt to maintain actual best sequence.
   */
  private static int maxSumRec( int [ ] a, int left, int right )
  {
      int maxLeftBorderSum = 0, maxRightBorderSum = 0;
      int leftBorderSum = 0, rightBorderSum = 0;
      int center = ( left + right ) / 2;

      if( left == right )  // Base case
          return a[ left ] > 0 ? a[ left ] : 0;

      int maxLeftSum  = maxSumRec( a, left, center );
      int maxRightSum = maxSumRec( a, center + 1, right );

      for( int i = center; i >= left; i-- )
      {
          leftBorderSum += a[ i ];
          if( leftBorderSum > maxLeftBorderSum )
              maxLeftBorderSum = leftBorderSum;
      }

      for( int i = center + 1; i <= right; i++ )
      {
          rightBorderSum += a[ i ];
          if( rightBorderSum > maxRightBorderSum )
              maxRightBorderSum = rightBorderSum;
      }

      return max3( maxLeftSum, maxRightSum,
                   maxLeftBorderSum + maxRightBorderSum );
  }

  /**
   * Return maximum of three integers.
   */
  private static int max3( int a, int b, int c )
  {
      return a > b ? a > c ? a : c : b > c ? b : c;
  }

  /**
   * Driver for divide-and-conquer maximum contiguous
   * subsequence sum algorithm.
   */
  public static int maxSubSum4( int [ ] a )
  {
      return a.length > 0 ? maxSumRec( a, 0, a.length - 1 ) : 0;
  }

  /**
   * Simple test program.
   */
  public static void main( String [ ] args )
  {
    
      //int N = Integer.parseInt(args[0]);
      
      //int[] a = new int[N];
      //Random randomGenerator = new Random();
    	
      //for(int i = 0; i < N; i++) {
//	  a[i] =  randomGenerator.nextInt(100);
     // }
    
      int a[] = { 4, -3, 5, -2, -1, 2, 6, -2 };
      int maxSum;
      
      maxSum = maxSubSum4( a );
      //System.out.println( "Max sum is " + maxSum );
      assert (maxSum > 0); 
      
  }
}
