package com.coronacharts.models;

import android.graphics.drawable.Drawable;

import com.coronacharts.R;

import java.util.ArrayList;
import java.util.HashMap;

public class CountryFlags {
    private HashMap<String, Integer> countryNflag;
    private int[] drawables;

    public CountryFlags(ArrayList<Country> countries){
        countryNflag = new HashMap<>();
        drawables = new int[]{

        };

        for (int i = 0; i < drawables.length; i++){
            countryNflag.put(countries.get(i).getName(), drawables[i]);
        }
    }
}
