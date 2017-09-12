
import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import static org.junit.Assert.*;


public class ThingTest {
    
    public ThingTest() {
    }
    
    
    @Test
    public void testToStringOverride() {
        Thing instance = new Thing("test");
        String expResult = "test";
        String result = instance.toString();
        assertEquals(expResult, result);
        instance = new Tiger("test");
        expResult = "test Tiger";
        result = instance.toString();
        assertEquals(expResult, result);
        
    }
    
}
