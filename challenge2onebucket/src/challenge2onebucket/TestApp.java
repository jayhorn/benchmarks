package challenge2onebucket;

import java.util.Random;

import challenge2onebucket.util.HashTable;
//import gov.nasa.jpf.symbc.Debug;

public class TestApp {


  public static void main(final java.lang.String[] args) {

    final int HASH_TABLE_SIZE = 1;
    int KEY_SIZE = 4;
    
    int N=Integer.parseInt(args[0]);
    final HashTable hashTable = new HashTable(HASH_TABLE_SIZE);
        
    Random rand = new Random(42);
    
    for(int i=0;i<N;i++) {
      char[] input = new char[KEY_SIZE];
      for(int s = 0; s < input.length; s++) {
    	//input[s] = Debug.makeSymbolicChar("in"+i+s);
    	char c = (char)(rand.nextInt(26) + 'a');
        input[s] = c;
      }
     // input[3] = (char)i;
     System.out.println("Size string " + input.length);
//      System.out.println("calling put #" + i);  
      hashTable.put(new String(input), "value");
    }   

    char[] input = new char[KEY_SIZE];
    for(int s = 0; s < input.length; s++) {
      //input[s] = Debug.makeSymbolicChar("get"+s);
      char c = (char)(rand.nextInt(26) + 'a');
      input[s] = c;
    }
  //  input[3] = '1';
//    System.out.println("calling get");
//    System.out.println("size of hashtable " + hashTable.size());
    hashTable.get(new String(input));
    
    int str_counter = hashTable.str_counter;
    int char_counter = hashTable.char_counter;
    
    System.out.println("Str Counter " + str_counter);
    System.out.println("Char Counter " + char_counter);
    
    System.out.println("Worst " + 4*N);
    //assert(char_counter <= 4*N);
    assert(false);
    
//    System.err.println("Goodbye!");
  }
}
