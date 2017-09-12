

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Assert;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import static org.junit.Assert.*;

public class FlyTest {
    
    public FlyTest() {
    }
    
    @Test
    public void testMove() {        
        Thing instance = new Thing("test");
        String expResult = "test";
        String result = instance.toString();
        assertEquals(expResult, result);
    }

    @Test
    public void testFly() {
        java.io.ByteArrayOutputStream out = new java.io.ByteArrayOutputStream();
        System.setOut(new java.io.PrintStream(out));
        Creature test = new Fly("test");        
        String expResult = "test Fly is buzzing around in flight.\n";
        test.move();
        String result = out.toString();
        assertEquals(expResult, result);
    }


    @Test
    public void testEat() throws Exception {    
        Creature t1 = new Tiger("test");
        Creature t2 = new Fly("test2");
        Thing t3 = new Thing("test3");
        java.io.ByteArrayOutputStream out = new java.io.ByteArrayOutputStream();
        System.setOut(new java.io.PrintStream(out));       
        String expResult = "test2 Fly won't eat a test Tiger\n";
        t2.eat(t1);
        String result = out.toString();
        assertEquals(expResult, result);
        out.reset();
        expResult = "test2 Fly has just eaten a test3\n";
        t2.eat(t3);
        result = out.toString();
        assertEquals(expResult, result);
    }
    
}
