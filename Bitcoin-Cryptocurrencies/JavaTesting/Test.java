
public class Test {

   public static void main() {
       int x, y;
       x = 5;
       y = 23;
       TestPair testGame = new TestPair(x, y);

       System.out.println (testGame.PairList.get(0).p1);
       System.out.println (testGame.PairList.get(0).p2);
       
       
   }
}
