package com.coronacharts;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;

import javax.annotation.Nullable;

public class FragmentCountryData extends Fragment {
    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater layoutInflater,  ViewGroup viewGroup, Bundle savedInstanceState){
        return layoutInflater.inflate(R.layout.fragment_country_data, viewGroup, false);
    }
}
