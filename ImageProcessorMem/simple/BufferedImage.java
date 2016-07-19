public class BufferedImage {

	int size;

	public BufferedImage(int size) {
		this.size = size;
	}

    static BufferedImage copy(BufferedImage bi, int size) {
	CostModel.copies++;
	CostModel.costs += 4*size;
	return bi;
    }

}
