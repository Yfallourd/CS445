
import org.junit.After;
import org.junit.AfterClass;
import org.junit.Assert;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import static org.junit.Assert.*;


public class BatTest {
    
    public BatTest() {
    }

    @Test
    public void testFly() {
        java.io.ByteArrayOutputStream out = new java.io.ByteArrayOutputStream();
        System.setOut(new java.io.PrintStream(out));
        Creature test = new Bat("test");        
        String expResult = "test Bat is swooping through the dark.\n";
        test.move();
        String result = out.toString();
        assertEquals(expResult, result);
    }
    
    @Test
    public void testEat() throws Exception {
        Creature t1 = new Tiger("test");
        Creature t2 = new Bat("test2");
        Thing t3 = new Thing("test3");
        java.io.ByteArrayOutputStream out = new java.io.ByteArrayOutputStream();
        System.setOut(new java.io.PrintStream(out));       
        String expResult = "test2 Bat has just eaten a test Tiger\n";
        t2.eat(t1);
        String result = out.toString();
        assertEquals(expResult, result);
        out.reset();
        expResult = "test2 Bat won't eat a test3\n";
        t2.eat(t3);
        result = out.toString();
        assertEquals(expResult, result);
    }
    
}
