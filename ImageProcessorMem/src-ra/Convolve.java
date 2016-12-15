
import java.awt.image.Kernel;


public class Convolve
{
//    public static final Kernel Gausian5x5 = new Kernel(5, 5, new float[] { 0.003021148f, 0.012084592f, 0.021148037f, 0.012084592f, 0.003021148f, 0.012084592f, 0.06042296f, 0.09969789f, 0.06042296f, 0.012084592f, 0.021148037f, 0.09969789f, 0.16616315f, 0.09969789f, 0.021148037f, 0.012084592f, 0.06042296f, 0.09969789f, 0.06042296f, 0.012084592f, 0.003021148f, 0.012084592f, 0.021148037f, 0.012084592f, 0.003021148f });
;    
    public static BufferedImage convolve(final BufferedImage image, final Kernel kernel) {
    	// removed library call
//        return new ConvolveOp(kernel, 1, null).filter(image, null);
//    	CostModel.bytes += 1; //image.getWidth() * image.getHeight();
    	return image;
    }
}
