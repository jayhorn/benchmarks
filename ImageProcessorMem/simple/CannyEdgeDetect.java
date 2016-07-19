import java.util.Random;

public class CannyEdgeDetect
{
    public static BufferedImage detect(final BufferedImage image, final int min, final int thresh, int size) {
        final BufferedImage blurred = BufferedImage.copy(image,size);//Convolve.convolve(image, null/*Convolve.Gausian5x5*/);
        final BufferedImage grey = BufferedImage.copy(blurred,size);//ConvertImage.otherGray(blurred);
        final BufferedImage sobelH = BufferedImage.copy(grey,size);//getSobelH(grey);
        final BufferedImage sobelV = BufferedImage.copy(grey,size);//getSobelV(grey);
        final BufferedImage angle = BufferedImage.copy(sobelH,size);//getAngles(sobelH, sobelV);
        final BufferedImage grad = BufferedImage.copy(angle,size);//getGradient(sobelH, sobelV);
        final BufferedImage nms = BufferedImage.copy(grad,size);//nonMaxSupression(angle, grad);
        final BufferedImage output = BufferedImage.copy(nms,size);//hysteresisThresholding(nms, min, thresh);
        return output;
    }

    public static void main(String args[]) {
	int size = 100;

	// create image
        BufferedImage bi = new BufferedImage(size);
	CostModel.copies++;
	CostModel.costs += 4 * size;

	// run
        detect(bi,0,0,size);

	// assert
	if (CostModel.copies <= 9) {
        	assert(CostModel.costs <= 9*4*size);
	}
    }
}
