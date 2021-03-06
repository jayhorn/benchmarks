import model.BufferedImage;
//import java.util.Random;

import cost.CostModel;

// JayHorn hangs in the construction of the CFG.
public class Driver {
	public static void main (String args[]) {
		CostModel.bytes = 0;
//		Random rand = new Random();
//		int W = rand.nextInt(10);
//		int H = rand.nextInt(10);
		int W = 10;
		int H = 10;
		BufferedImage bi = new BufferedImage(W,H,BufferedImage.TYPE_INT_ARGB);
		BufferedImage cannied = CannyEdgeDetect.detect(bi, 125, 220);
//		CostModel.bytes += 10;
		System.out.println("Costs: " + CostModel.bytes);
		assert(CostModel.bytes <= 2*4*10*H);//2 * W*H*4);
//		assert true;
	}
}
