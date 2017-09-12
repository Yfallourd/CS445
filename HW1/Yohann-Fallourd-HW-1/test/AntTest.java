/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import static org.junit.Assert.*;

/**
 *
 * @author root
 */
public class AntTest {
    
    public AntTest() {
    }

    @Test
    public void testMove() {
        java.io.ByteArrayOutputStream out = new java.io.ByteArrayOutputStream();
        System.setOut(new java.io.PrintStream(out));
        Creature test = new Ant("test");        
        String expResult = "test Ant is crawling around.\n";
        test.move();
        String result = out.toString();
        assertEquals(expResult, result);
    }
    
}
