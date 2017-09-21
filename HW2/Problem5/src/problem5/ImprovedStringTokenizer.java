/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package problem5;

import java.util.StringTokenizer;

/**
 *
 * @author root
 */
public class ImprovedStringTokenizer extends StringTokenizer {

    public ImprovedStringTokenizer(String str) {
        super(str);
    }

    public ImprovedStringTokenizer(String str, String delim) {
        super(str, delim);
    }

    public ImprovedStringTokenizer(String str, String delim, boolean returnDelims) {
        super(str, delim, returnDelims);
    }

    public String[] inArray() {
        String arr[] = new String[this.countTokens()];
        int i = 0;
        while (i<arr.length) {
            arr[i] = this.nextToken();
            ++i;
        }
        return arr;
    }
}
