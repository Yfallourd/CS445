/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Assert;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import static org.junit.Assert.*;

/**
 *
 * @author root
 */
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
    public void shouldntEatAThing() throws Exception {
        Creature t1 = new Tiger("test");
        Creature t2 = new Bat("test2");
        t2.eat(t1);
        Assert.assertTrue("Bat hasn't eaten the Thing", t2.stomachContent == null);
    }
    
}
