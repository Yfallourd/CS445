public abstract class Creature extends Thing {
    
    protected Thing stomachContent;
    
    public Creature(String name) {
        super(name);
    }    
    
    public void eat(Thing thing) {
        System.out.println(this.toString()+
                           " has just eaten a "+
                           thing.toString());
        this.stomachContent = thing;
    }
    
    public abstract void move();
    
    public void whatDidYouEat() {
        if(stomachContent != null) {
            System.out.println(this.toString()+
                               " has eaten a "+
                               stomachContent.toString());
        } else {
            System.out.println(this.toString()+" has had nothing to eat");
        }
    }
    
}
