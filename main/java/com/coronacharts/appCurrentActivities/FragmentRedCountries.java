package com.coronacharts.appCurrentActivities;

import android.app.AlertDialog;
import android.app.Dialog;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.DividerItemDecoration;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.os.Handler;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.view.inputmethod.EditorInfo;
import android.widget.EditText;
import android.widget.SearchView;
import android.widget.Toast;
import android.widget.Toolbar;

import com.coronacharts.R;
import com.coronacharts.handlers.CountriesAdapter;
import com.coronacharts.models.Country;
import com.google.android.material.appbar.MaterialToolbar;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Objects;


/**
 * Fragment for listing red and green countries with search and filter options.
 */
public class FragmentRedCountries extends Fragment {
    private RecyclerView recyclerView;
    private ArrayList<Country> countries;
    private View view;
    private DatabaseReference databaseReference;
    private CountriesAdapter countriesAdapter;
    public FragmentRedCountries() {
        // Required empty public constructor
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        setHasOptionsMenu(true);
        databaseReference = FirebaseDatabase.getInstance().getReference("Countries_Red_Green").child("color_by_country");
        countries = new ArrayList<>();
        searchTree();
        Log.d("List", countries.toString());
        view = inflater.inflate(R.layout.fragment_red_countries, container, false);
        setElements();
        return view;
    }

    @Override
    public void onCreateOptionsMenu(@NonNull Menu menu, @NonNull MenuInflater inflater) {
        inflater.inflate(R.menu.app_bar_options, menu);
        MenuItem searchItem = menu.findItem(R.id.filterCountries);
        SearchView searchView = (SearchView) searchItem.getActionView();
        searchView.setImeOptions(EditorInfo.IME_ACTION_DONE);
        searchView.setOnQueryTextListener(new SearchView.OnQueryTextListener() {
            @Override
            public boolean onQueryTextSubmit(String query) {
                return false;
            }
            @Override
            public boolean onQueryTextChange(String searchText) {
                countriesAdapter.getFilter().filter(searchText);
                return false;
            }
        });
        super.onCreateOptionsMenu(menu, inflater);
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        if (item.getItemId() == R.id.guide)
        {
            Dialog dialog = new Dialog(Objects.requireNonNull(getContext()));
            dialog.requestWindowFeature(Window.FEATURE_NO_TITLE);
            dialog.setContentView(R.layout.guide_diaglog);
            dialog.show();
        }
        return super.onOptionsItemSelected(item);
    }

    private void setElements(){
        countries.add(new Country("מדינה", "סטטוס"));
        recyclerView = view.findViewById(R.id.recyclerViewCountries);
        countriesAdapter = new CountriesAdapter(getContext(), countries);
        LinearLayoutManager linearLayoutManager = new LinearLayoutManager(getActivity());
        recyclerView.setLayoutManager(linearLayoutManager);
        DividerItemDecoration dividerItemDecoration = new DividerItemDecoration(recyclerView.getContext(), linearLayoutManager.getOrientation());
        recyclerView.addItemDecoration(dividerItemDecoration);
        recyclerView.setAdapter(countriesAdapter);
    }

    private void searchTree() {
        databaseReference.addListenerForSingleValueEvent(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot snapshot) {
                for(DataSnapshot snapshot1: snapshot.getChildren()){
                    String country = snapshot1.getKey();
                    String status = "";
                    for(DataSnapshot snapshot2: snapshot1.getChildren()){
                        status = snapshot2.getValue(String.class);
                        assert status != null;
                        countries.add(new Country(country, status));
                        countriesAdapter.updateData(countries);
                    }
                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError error) {

            }
        });
    }

    
}
