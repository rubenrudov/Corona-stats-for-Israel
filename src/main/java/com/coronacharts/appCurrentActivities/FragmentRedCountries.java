package com.coronacharts.appCurrentActivities;

import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.RecyclerView;

import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

import com.coronacharts.R;

import java.util.ArrayList;


/**
 * Fragment for listing red and green countries with search and filter options.
 */
public class FragmentRedCountries extends Fragment {
    RecyclerView recyclerView;
    // ArrayList<Object> countries;
    public FragmentRedCountries() {
        // Required empty public constructor
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_red_countries, container, false);
    }
}
