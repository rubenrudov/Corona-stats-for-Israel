package com.coronacharts.appCurrentActivities;

import android.annotation.SuppressLint;
import android.app.AlertDialog;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.view.inputmethod.EditorInfo;
import android.widget.EditText;
import android.widget.SearchView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;

import com.coronacharts.R;
import com.coronacharts.models.CityStats;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.io.InputStream;
import java.io.OutputStream;
import java.sql.Date;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Objects;

import javax.annotation.Nullable;

public class FragmentCountryData extends Fragment {
    private DatabaseReference databaseReference;
    private TextView cityName, vaccined, verified, tests, recovered, isolated, deaths;
    private ArrayList<Object> params;
    private View view;

    public FragmentCountryData() {
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater layoutInflater,  ViewGroup viewGroup, Bundle savedInstanceState){
        view = layoutInflater.inflate(R.layout.fragment_country_data, viewGroup, false);
        setHasOptionsMenu(true);
        try {
            setAllElements();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        return view;
    }

    private void setAllElements() throws InterruptedException {
        databaseReference = FirebaseDatabase.getInstance().getReference().child("israel_final").child("data");
        vaccined = view.findViewById(R.id.vaccined);
        verified = view.findViewById(R.id.verified);
        tests = view.findViewById(R.id.tests);
        recovered = view.findViewById(R.id.healed);
        isolated = view.findViewById(R.id.isolated);
        deaths = view.findViewById(R.id.dead);
        // searchTree();
    }

    private void searchTree() {
        // Function for finding the stats of the whole country in the db
        params = new ArrayList<>();
        databaseReference.addListenerForSingleValueEvent(new ValueEventListener() {
            @SuppressLint("SetTextI18n")
            @Override
            public void onDataChange(@NonNull DataSnapshot snapshot) {
                for (DataSnapshot dataSnapshot: snapshot.getChildren()) {
                    for (DataSnapshot dataSnapshot1: dataSnapshot.getChildren()) {
                        int i = 0;
                        for (DataSnapshot dataSnapshot2: dataSnapshot1.getChildren()){
                            if (i == 1){
                                params.add(dataSnapshot2.getValue());
                                break;
                            }
                            i++;
                        }
                    }
                }
                setTextForTextView();
            }

            @Override
            public void onCancelled(@NonNull DatabaseError error) {
                Log.d("Exception", "connection collapsed");
            }
        });
    }


    private void setTextForTextView() {
        vaccined.setText(params.get(4).toString());
        verified.setText(params.get(5).toString());
        recovered.setText(params.get(3).toString());
        tests.setText(params.get(1).toString());
        isolated.setText("Need data");
        deaths.setText(params.get(0).toString());
    }

    @Override
    public void onCreateOptionsMenu(@NonNull Menu menu, @NonNull MenuInflater inflater) {
        inflater.inflate(R.menu.app_bar_options, menu);
        MenuItem item = menu.findItem(R.id.filterCountries);
        item.setVisible(false);
        super.onCreateOptionsMenu(menu, inflater);
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        if (item.getItemId() == R.id.guide)
        {
            AlertDialog.Builder builder = new AlertDialog.Builder(getContext());
            View viewGroup = view.findViewById(android.R.id.custom);
            View dialogView = LayoutInflater.from(view.getContext()).inflate(R.layout.guide_diaglog, (ViewGroup) viewGroup, false);
            builder.setView(dialogView);
            AlertDialog alertDialog = builder.create();
            alertDialog.show();
        }
        return super.onOptionsItemSelected(item);
    }
}
