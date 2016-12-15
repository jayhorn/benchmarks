//import java.util.Random;

/**
 *
 * Minimal model for BufferedImage that makes everything symbolic.
 * 
 * @author Rody Kersten
 */

public class BufferedImage //extends java.awt.Image
//                           implements WritableRenderedImage, Transparency
{
	//Simple model: just int width and height, plus 2-dimensional array of pixels.
	public int width;
	int height;
	int pixels[][];
	
	// each symbolic image has a unique ID
	int id;
	static int nextID = 0;
	
	// has all these defines
//    public static final int TYPE_CUSTOM = 0;
//    public static final int TYPE_INT_RGB = 1;
    public static final int TYPE_INT_ARGB = 2;
//    public static final int TYPE_INT_ARGB_PRE = 3;
//    public static final int TYPE_INT_BGR = 4;
//    public static final int TYPE_3BYTE_BGR = 5;
//    public static final int TYPE_4BYTE_ABGR = 6;
//    public static final int TYPE_4BYTE_ABGR_PRE = 7;
//    public static final int TYPE_USHORT_565_RGB = 8;
//    public static final int TYPE_USHORT_555_RGB = 9;
//    public static final int TYPE_BYTE_GRAY = 10;
//    public static final int TYPE_USHORT_GRAY = 11;
//    public static final int TYPE_BYTE_BINARY = 12;
//    public static final int TYPE_BYTE_INDEXED = 13;

    public BufferedImage(int width,
                         int height,
                         int imageType) {
        this.width = width;
        this.height = height;
        this.pixels = new int[width][height];
        //this.id = nextID++;
        
        // symbolic pixels
//        Random rand = new Random();
//    	for (int x = 0; x < width; x++) {
//    		for (int y = 0; y < height; y++) {
//    			pixels[x][y] = 0;//rand.nextInt(10);
//    		}
//    	}
        
        // Don't do anything, except update costs
        //CostModel.bytes += 4 * width * height;
    }

    public int getType() {
        return TYPE_INT_ARGB;
    }

    public int getRGB(int x, int y) {
        return pixels[x][y];
    }

    public int[] getRGB(int startX, int startY, int w, int h,
                        int[] rgbArray, int offset, int scansize) {
    	if (rgbArray==null) {
    		rgbArray = new int[w*h];
    		offset = 0;
    	}
    	
    	int i = 0;
    	for (int x = startX; x < startX+w; x++) {
    		for (int y = startY; y < startY+h; y++) {
    			rgbArray[i++] = pixels[x][y];
    		}
    	}
    	
    	return rgbArray;
    }

    public synchronized void setRGB(int x, int y, int rgb) {
        pixels[x][y] = rgb;
    }

    public int getWidth() {
        return width;
    }

    public int getHeight() {
        return height;
    }

    public String toString() {
        return "Symbolic BufferedImage";
    }

    public int getMinX() {
        return 0;
    }

    public int getMinY() {
        return 0;
    }

    public int getNumXTiles() {
        return 1;
    }

    public int getNumYTiles() {
        return 1;
    }

    public int getMinTileX() {
        return 0;
    }

    public int getMinTileY() {
        return 0;
    }

    public int getTileWidth() {
       return width;
    }

    public int getTileHeight() {
       return height;
    }
    
    public BufferedImage getCopy() {
    	BufferedImage copy = new BufferedImage(width,height,0);
    	for (int x = 0; x < width; x++) {
    		for (int y = 0; y < height; y++) {
    			copy.setRGB(x, y, pixels[x][y]);
    		}
    	}
    	return copy;
    }
    
//    public void getCopyCosts() {
//    	CostModel.bytes += 4;// * width * height;
//    }
}
