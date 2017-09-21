/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package problem4;
import java.util.Random;

public class ImprovedRandom extends Random{
    
    public ImprovedRandom(){
        super();
    }
    
    public ImprovedRandom(long seed){
        super(seed);
    }
    
    public int boundRandInt(int lowerbound, int higherbound){
        int result = this.nextInt(higherbound-lowerbound+1); //returns a random int between 0 and higherbound
        result += lowerbound; //move the result between lowerbound and higherbound
        return result;
    }
    
}
