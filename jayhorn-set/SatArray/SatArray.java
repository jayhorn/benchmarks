import java.util.Random;

class A
{
  public int i;
};

class B {
  A as[];
}

class SatArray
{

	  public static void main(String[] args)
	  {
	    A a0=new A();
	    a0.i = 999;
	    A a1 = new A();
	    a1.i = 666;

            B b = new B();
            b.as = new A[2];
            b.as[0] = a0;
	    b.as[1] = a1;

	    assert 999 == b.as[0].i;
	  }
}
  
