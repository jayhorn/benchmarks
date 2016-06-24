import java.util.Stack;
import java.util.ArrayList;
import java.util.List;
import java.util.Collection;

public class SimplifiedSorter
{
    public static void main(String args[]) {
        
	// for now, fixed list
	ArrayList<String> toSort = new ArrayList<String>();
	toSort.add("test");
	toSort.add("abcd");

	SimplifiedSorter ss = new SimplifiedSorter();
 	ss.sort(toSort);

	// UNSAFE
	//assert(false);

	// SAFE (not really)
	assert(toSort.get(0).equals("test"));

	// SAFE
	assert(toSort.get(0).equals("abcd"));

	// SAFE (not really)
	assert (toSort.get(0) == null);
    }

    public List<String> sort(final Collection<String> stuff) {
        final List<String> stuffList = new ArrayList<String>(stuff);
        this.changingSort(stuffList, 0, stuffList.size() - 1);
        return stuffList;
    }
    
    private void changingSort(final List<String> list, final int initStart, final int initEnd) {
        final ArrayIndex initial = ArrayIndex.partition(initStart, initEnd);
        final Stack<ArrayIndex> indexStack = new Stack<ArrayIndex>();
        indexStack.push(initial);
        while (!indexStack.empty()) {
            final ArrayIndex index = indexStack.pop();
            if (index.getStart() < index.getEnd()) {
                if (index.isPartition()) {
                    final int q1 = (int)Math.floor((index.getStart() + index.getEnd()) / 2);
                    final int q2 = (int)Math.floor((q1 + 1 + index.getEnd()) / 2);
                    final int q3 = (int)Math.floor((q2 + 1 + index.getEnd()) / 2);
                    final int q4 = (int)Math.floor((q3 + 1 + index.getEnd()) / 2);
                    final int q5 = (int)Math.floor((q4 + 1 + index.getEnd()) / 2);
                    indexStack.push(ArrayIndex.merge(index.getStart(), q1, index.getEnd()));
                    indexStack.push(ArrayIndex.merge(q1 + 1, q2, index.getEnd()));
                    indexStack.push(ArrayIndex.merge(q2 + 1, q3, index.getEnd()));
                    indexStack.push(ArrayIndex.merge(q3 + 1, q4, index.getEnd()));
                    indexStack.push(ArrayIndex.merge(q4 + 1, q5, index.getEnd()));
                    indexStack.push(ArrayIndex.partition(index.getStart(), q1));
                    indexStack.push(ArrayIndex.partition(q1 + 1, q2));
                    indexStack.push(ArrayIndex.partition(q2 + 1, q3));
                    indexStack.push(ArrayIndex.partition(q3 + 1, q4));
                    indexStack.push(ArrayIndex.partition(q4 + 1, q5));
                    indexStack.push(ArrayIndex.partition(q5 + 1, index.getEnd()));
                }
                else {
                    if (!index.isMerge()) {
                        throw new RuntimeException("Not merge or partition");
                    }
                    this.merge(list, index.getStart(), index.getMidpoint(), index.getEnd());
                }
            }
        }
    }
    
    private void merge(final List<String> list, final int initStart, final int q, final int initEnd) {
        final List<String> left = new ArrayList<String>(q - initStart + 1);
        final List<String> right = new ArrayList<String>(initEnd - q);
        for (int i = 0; i < q - initStart + 1; ++i) {
            this.mergeHelper(list, left, initStart, i);
        }
        for (int j = 0; j < initEnd - q; ++j) {
            this.mergeHelper1(q, list, j, right);
        }
        int i = 0;
        int k = 0;
        for (int m = initStart; m < initEnd + 1; ++m) {
            if (i < left.size() && (k >= right.size() || left.get(i).compareTo(right.get(k)) < 0)) {
                list.set(m, left.get(i++));
            }
            else if (k < right.size()) {
                list.set(m, right.get(k++));
            }
        }

    }
    
    private void mergeHelper(final List<String> list, final List<String> left, final int initStart, final int i) {
        left.add(list.get(initStart + i));
    }
    
    private void mergeHelper1(final int q, final List<String> list, final int j, final List<String> right) {
        right.add(list.get(q + 1 + j));
    }

}
