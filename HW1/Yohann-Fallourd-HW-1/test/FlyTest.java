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
    public void shouldntEatACreature() throws Exception {
        Creature t1 = new Tiger("test");
        Creature t2 = new Fly("test2");
        t2.eat(t1);
        Assert.assertTrue("Fly hasn't eaten the Creature", t2.stomachContent == null);
    }
    
}
