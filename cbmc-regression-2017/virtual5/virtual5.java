public class virtual5 {

  public static void main(String args[]){
	parent p = new parent();
	child c = new child();
	test(p, c);
  }

  public static void test(parent p, child c) {

    if(p==null)
      return;
    assert(p.get()==1);

  }

}

class parent {

  public int get() { return 1; }

}

class child extends parent {

  public int get() { return 2; }

}
