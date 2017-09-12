/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author root
 */
public class Ant extends Creature{

    public Ant(String name) {
        super(name);
    }

    @Override
    public void move() {
        System.out.println(this.toString()+" is crawling around.");
    }
    
}
