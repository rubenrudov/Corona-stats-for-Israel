package com.coronacharts.appCurrentActivities;

import android.annotation.SuppressLint;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.ImageButton;
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

import java.util.Objects;

/**
 *  * Fragment for searching data by city
 */
public class FragmentByCity extends Fragment {
    private DatabaseReference databaseReference;
    private EditText editTextCityInsert;
    private TextView cityName, vaccined, verified, tests, recovered, deaths;
    private View view;
    private CityStats[] cityStats = new CityStats[1];

    @Override
    public View onCreateView(
            @NonNull LayoutInflater layoutInflater, ViewGroup viewGroup,
            Bundle savedInstanceState) {
        view = layoutInflater.inflate(R.layout.fragment_by_city_search, viewGroup, false);
        setAllElements();
        return view;
    }

    private void setAllElements() {
        databaseReference = FirebaseDatabase.getInstance().getReference().child("cities_final");
        editTextCityInsert = view.findViewById(R.id.editTextCityInsert);
        cityName = view.findViewById(R.id.cityName);
        vaccined = view.findViewById(R.id.vaccined);
        verified = view.findViewById(R.id.verified);
        tests = view.findViewById(R.id.tests);
        recovered = view.findViewById(R.id.healed);
        deaths = view.findViewById(R.id.dead);
        // Search button and onClockListener
        ImageButton searchBtn = view.findViewById(R.id.searchBtn);
        searchBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                treeSearching(editTextCityInsert.getText().toString());
            }
        });
    }

    private void treeSearching(final String inputCityName) {
        // Function that searches for the city name in the data base and inserts it into a variable (Type: CityStats)
        databaseReference.addListenerForSingleValueEvent(new ValueEventListener() {
            @SuppressLint("SetTextI18n")
            @Override
            public void onDataChange(@NonNull DataSnapshot snapshot) {
                for (DataSnapshot dataSnapshot: snapshot.getChildren()) {
                    Log.d("Ruby", Objects.requireNonNull(dataSnapshot.getValue()).toString());
                    if (Objects.requireNonNull(dataSnapshot.getKey()).contains(inputCityName)) {
                        for (DataSnapshot snapshot1: dataSnapshot.getChildren()) {
                            // Create an instance of CityStats
                            cityStats[0] = snapshot1.getValue(CityStats.class);
                            assert cityStats[0] != null;
                            // Date format
                            assert cityStats[0].getDate() != null;
                            String[] date = cityStats[0].getDate().split("-");
                            String format = date[2] + "/" + date[1] + "/" + date[0];
                            // Set stats in TextViews
                            cityName.setText(cityStats[0].getCity_Name().replaceAll("שבט", "").replace("(", "").replace(")", "") + " נכון לתאריך: \n" + format);
                            vaccined.setText(cityStats[0].getCumulated_vaccinated());
                            verified.setText(cityStats[0].getCumulative_verified_cases());
                            recovered.setText(cityStats[0].getCumulated_recovered());
                            tests.setText(cityStats[0].getCumulated_number_of_tests());
                            deaths.setText(cityStats[0].getCumulated_deaths());
                            // Stop the the loop
                            break;
                        }
                        // Stops the loop after the required city found
                        break;
                    }
                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError error) {

            }
        });
    }
}