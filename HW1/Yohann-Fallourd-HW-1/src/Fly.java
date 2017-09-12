/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author root
 */
public class Fly extends Creature implements Flyer {

    public Fly(String name) {
        super(name);
    }

    @Override
    public void move() {
        fly();
    }

    @Override
    public void fly() {
        System.out.println(this.toString()+" is buzzing around in flight.");
    }
    
    public void eat(Thing thing) {
        if ("Thing".equals(thing.getClass().getSimpleName())) {
            super.eat(thing);
        } else {
            System.out.println(this.toString()+" won't eat a "+ thing.toString());
        }
    }
    
}
