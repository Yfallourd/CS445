/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import java.util.logging.Level;
import java.util.logging.Logger;
import org.junit.*;
import org.junit.rules.ExpectedException;

/**
 *
 * @author root
 */
public class CreatureTest {

    public CreatureTest() {
    }

   
    @Test(expected = Exception.class)
    public void shouldntEatNullThing() throws Exception{
        Thing thing = null;
        Creature testCreature = new Tiger("test");
        testCreature.eat(thing);
    }
    
    @Test
    public void eatingShouldFillStomach() throws Exception {
        Thing thing = new Thing("testthing");
        Creature testCreature = new Tiger("test");
        testCreature.eat(thing);
        Assert.assertTrue("Stomach is full", testCreature.stomachContent != null);
    }

   

   
    @Test
    public void whatDidYouEatShouldWorkForAnyStomachContent() throws Exception {
        Creature t1 = new Tiger("test");
        Creature t2 = new Tiger("test2");
        t1.whatDidYouEat();
        t1.eat(t2);
        t1.whatDidYouEat();
    }


}
