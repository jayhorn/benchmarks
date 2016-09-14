function myprog() {
  CURRENT=`pwd`
  BASENAME=`basename "$CURRENT"`
  echo $CURRENT
  echo $BASENAME
  for d in *; do
      echo $d
      cd $d
      ls
      javac Main.java
      cd $CURRENT
    done
}
myprog;
