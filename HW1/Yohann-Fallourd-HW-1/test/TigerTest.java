
import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import static org.junit.Assert.*;

public class TigerTest {
    
    public TigerTest() {
    }

    @Test
    public void testMove() {
        java.io.ByteArrayOutputStream out = new java.io.ByteArrayOutputStream();
        System.setOut(new java.io.PrintStream(out));
        Creature test = new Tiger("test");        
        String expResult = "test Tiger has just pounced.\n";
        test.move();
        String result = out.toString();
        assertEquals(expResult, result);
    }
    
}
