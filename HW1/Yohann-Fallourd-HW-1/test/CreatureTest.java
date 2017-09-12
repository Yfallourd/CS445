

import java.util.logging.Level;
import java.util.logging.Logger;
import org.junit.*;
import static org.junit.Assert.assertEquals;
import org.junit.rules.ExpectedException;

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
    public void testWhatDidYouEat() throws Exception {
        Creature t1 = new Tiger("test");
        Creature t2 = new Tiger("test2");
        java.io.ByteArrayOutputStream out = new java.io.ByteArrayOutputStream();
        System.setOut(new java.io.PrintStream(out));       
        String expResult = "test Tiger has had nothing to eat\n";
        t1.whatDidYouEat();
        String result = out.toString();
        assertEquals(expResult, result);   
        t1.eat(t2);     
        out.reset();
        t1.whatDidYouEat();
        expResult = "test Tiger has eaten a test2 Tiger\n";
        result = out.toString();
        assertEquals(expResult, result);
    }


}
