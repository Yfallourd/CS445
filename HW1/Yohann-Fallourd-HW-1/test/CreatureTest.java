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
public class CreatureTest {
    
    public CreatureTest() {
    }
    
    @BeforeClass
    public static void setUpClass() {
    }
    
    @AfterClass
    public static void tearDownClass() {
    }
    
    @Before
    public void setUp() {
    }
    
    @After
    public void tearDown() {
    }

    /**
     * Test of eat method, of class Creature.
     */
    @Test
    public void testEat() {
        System.out.println("eat");
        Thing thing = null;
        Creature instance = null;
        instance.eat(thing);
        // TODO review the generated test code and remove the default call to fail.
        fail("The test case is a prototype.");
    }

    /**
     * Test of move method, of class Creature.
     */
    @Test
    public void testMove() {
        System.out.println("move");
        Creature instance = null;
        instance.move();
        // TODO review the generated test code and remove the default call to fail.
        fail("The test case is a prototype.");
    }

    /**
     * Test of whatDidYouEat method, of class Creature.
     */
    @Test
    public void testWhatDidYouEat() {
        System.out.println("whatDidYouEat");
        Creature instance = null;
        instance.whatDidYouEat();
        // TODO review the generated test code and remove the default call to fail.
        fail("The test case is a prototype.");
    }

    public class CreatureImpl extends Creature {

        public CreatureImpl() {
            super("");
        }

        public void move() {
        }
    }
    
}
