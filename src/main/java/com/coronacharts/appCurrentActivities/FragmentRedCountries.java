package com.coronacharts.appCurrentActivities;

import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.DividerItemDecoration;
import androidx.recyclerview.widget.LinearLayoutManager;
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
import com.coronacharts.handlers.CountriesAdapter;
import com.coronacharts.models.Country;

import java.util.ArrayList;
import java.util.Objects;


/**
 * Fragment for listing red and green countries with search and filter options.
 */
public class FragmentRedCountries extends Fragment {
    private RecyclerView recyclerView;
    private ArrayList<Country> countries;
    private View view;
    public FragmentRedCountries() {
        // Required empty public constructor
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        view = inflater.inflate(R.layout.fragment_red_countries, container, false);
        setElements();
        return view;
    }

    private void setElements(){
        recyclerView = view.findViewById(R.id.recyclerViewCountries);
        // TODO: get countries by scraping the Excel file of red/green countries
        countries = new ArrayList<>();
        countries.add(new Country("ארה''ב", "אדום"));
        countries.add(new Country("צרפת", "אדום"));
        countries.add(new Country("איטליה", "ירוק"));
        countries.add(new Country("ספרד", "אדום"));
        countries.add(new Country("ארה''ב", "אדום"));
        countries.add(new Country("צרפת", "אדום"));
        countries.add(new Country("איטליה", "ירוק"));
        countries.add(new Country("ספרד", "אדום"));
        countries.add(new Country("ארה''ב", "אדום"));
        countries.add(new Country("צרפת", "אדום"));
        countries.add(new Country("איטליה", "ירוק"));
        countries.add(new Country("ספרד", "אדום"));
        countries.add(new Country("ארה''ב", "אדום"));
        countries.add(new Country("צרפת", "אדום"));
        countries.add(new Country("איטליה", "ירוק"));
        countries.add(new Country("ספרד", "אדום"));
        LinearLayoutManager linearLayoutManager = new LinearLayoutManager(getActivity());
        recyclerView.setLayoutManager(linearLayoutManager);
        DividerItemDecoration dividerItemDecoration = new DividerItemDecoration(recyclerView.getContext(), linearLayoutManager.getOrientation());
        recyclerView.addItemDecoration(dividerItemDecoration);
        recyclerView.setAdapter(new CountriesAdapter(getContext(), countries));
    }
}
