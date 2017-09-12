/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author root
 */
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
