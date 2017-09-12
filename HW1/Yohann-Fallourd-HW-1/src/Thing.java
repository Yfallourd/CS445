
public class Thing {

    protected final String name;
    
    public Thing(String name){
        this.name = name;
    }
    @Override
    public String toString() {
        String classname = getClass().getSimpleName();
        return ("Thing".equals(classname))? name : name+" "+classname;
    }
}
