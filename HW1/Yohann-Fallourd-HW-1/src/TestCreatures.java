
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.text.EditorKit;


public class TestCreatures {


    public static void main(String[] args) {
        final int THING_COUNT = 4;
        final int CREATURE_COUNT = 5;
        Thing things[] = new Thing[THING_COUNT + CREATURE_COUNT];
        Creature creatures[] = new Creature[CREATURE_COUNT];
        //<editor-fold desc="Array filling">
        things[0] = new Thing("Bob");
        things[1] = new Thing("Bobby");
        things[2] = new Thing("Bobby 2");
        things[3] = new Thing("Bobby 3, return of the Bobby");
        things[4] = new Tiger("Jake");
        things[5] = new Tiger("John");
        things[6] = new Fly("Pretty");
        things[7] = new Ant("Man");
        things[8] = new Bat("Bruce Wayne");
        creatures[0] = (Tiger) things[4];
        creatures[1] = (Tiger) things[5];
        creatures[2] = (Fly) things[6];
        creatures[3] = (Ant) things[7];
        creatures[4] = (Bat) things[8];
        //</editor-fold>

        System.out.println("Things :\n");
        for (Thing i : things) {
            System.out.println(i);
        }
        System.out.println("\nCreatures :\n");
        for (Creature i : creatures) {
            i.move();
        }

        System.out.println("\nEating time :\n");
        try {
            creatures[0].eat(creatures[1]);
            creatures[4].eat(creatures[0]);
            creatures[3].eat(creatures[2]);
        } catch (Exception ex) {
            ex.getMessage();
        }

        System.out.println("\nChecking time :\n");
        creatures[0].whatDidYouEat();
        creatures[4].whatDidYouEat();
        creatures[3].whatDidYouEat();
    }

}
