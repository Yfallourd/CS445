/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package problem5;



public class Problem5 {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        ImprovedStringTokenizer imp = new ImprovedStringTokenizer("This sentence is just a test");
        System.out.println(imp.countTokens());
        for(String word : imp.inArray()){
            System.out.println(word);
        }
    }
    
}
