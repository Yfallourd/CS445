/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package problem4;


public class Problem4 {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        ImprovedRandom ran = new ImprovedRandom();
        int i=50;
        while(i>0){
            System.out.println(ran.boundRandInt(5, 25));
            i--;
        }
    }
    
}
