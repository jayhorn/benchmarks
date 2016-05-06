//import java.awt.color.*;
//import java.awt.image.*;
//import java.awt.*;
import model.BufferedImage;
import cost.CostModel;

public class ConvertImage
{
    public static BufferedImage grayscale(final BufferedImage image) {
//        return new ColorConvertOp(ColorSpace.getInstance(1003), null).filter(image, null);
    	CostModel.bytes += 1; //image.getWidth() * image.getHeight();
    	return image;
    }
    
    public static BufferedImage boostedGray(final BufferedImage image) {
        final BufferedImage out = new BufferedImage(image.getWidth(), image.getHeight(), 2);
        for (int i = 0; i < image.getWidth(); ++i) {
            for (int j = 0; j < image.getHeight(); ++j) {
                final int argb = image.getRGB(i, j);
                final int a = ARGB.rawA(argb);
                final int r = ARGB.rawR(argb);
                final int g = ARGB.rawG(argb);
                final int b = ARGB.rawB(argb);
                final int val = (r + r + r + b + g + g + g + g) / 8;
                out.setRGB(i, j, ARGB.toARGB(a, val, val, val));
            }
        }
        return out;
    }
    
    // Seems to convert image into grayscale
    public static BufferedImage otherGray(final BufferedImage image) {
//        final BufferedImage out = new BufferedImage(image.getWidth(), image.getHeight(), BufferedImage.TYPE_BYTE_GRAY);
//        final Graphics g = out.getGraphics();
//        g.drawImage(image, 0, 0, null);
//        return out;
    	CostModel.bytes += 1; //image.getWidth() * image.getHeight();
    	return image;
    }
}
