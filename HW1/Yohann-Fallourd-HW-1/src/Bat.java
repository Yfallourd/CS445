public class Bat extends Creature implements Flyer {

    public Bat(String name) {
        super(name);
    }

    @Override
    public void move() {
        fly();
    }
    
    @Override
    public void eat(Thing thing) throws Exception {
        //A Bat can only eat Creatures
        if (!"Thing".equals(thing.getClass().getSimpleName())) {
            super.eat(thing);
        } else {
            System.out.println(this.toString()+" won't eat a "+ thing.toString());
        }
    }
    
    @Override
    public void fly() {
        System.out.println(this.toString()+" is swooping through the dark.");
    }
    
}
