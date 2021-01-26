package com.coronacharts.appCurrentActivities;

import android.annotation.SuppressLint;
import android.app.AlertDialog;
import android.app.Dialog;
import android.os.Bundle;
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
import android.widget.Filter;
import android.widget.ImageButton;
import android.widget.ScrollView;
import android.widget.SearchView;
import android.widget.TextView;
import android.widget.Toast;

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
    private TextView cityName, verified, tests, recovered, deaths;
    private View view;
    private CityStats[] cityStats = new CityStats[1];

    @Override
    public View onCreateView(
            @NonNull LayoutInflater layoutInflater, ViewGroup viewGroup,
            Bundle savedInstanceState) {
        setHasOptionsMenu(true);
        view = layoutInflater.inflate(R.layout.fragment_by_city_search, viewGroup, false);
        setElements();
        return view;
    }

    private void setElements() {
        databaseReference = FirebaseDatabase.getInstance().getReference().child("cities_final");
        cityName = view.findViewById(R.id.cityName);
        verified = view.findViewById(R.id.verified);
        tests = view.findViewById(R.id.tests);
        recovered = view.findViewById(R.id.healed);
        deaths = view.findViewById(R.id.dead);
    }

    private void treeSearching(final String inputCityName) {
        // Function that searches for the city name in the data base and inserts it into a variable (Type: CityStats)
        databaseReference.addListenerForSingleValueEvent(new ValueEventListener() {
            @SuppressLint("SetTextI18n")
            @Override
            public void onDataChange(@NonNull DataSnapshot snapshot) {
                for (DataSnapshot dataSnapshot: snapshot.getChildren()) {
                    if (Objects.requireNonNull(dataSnapshot.getKey()).contains(inputCityName)) {
                        for (DataSnapshot snapshot1: dataSnapshot.getChildren()) {
                            // Create an instance of CityStats
                            cityStats[0] = snapshot1.getValue(CityStats.class);
                            // Date format
                            if (cityStats[0] != null && cityStats[0].getDate() != null) {
                                String[] date = cityStats[0].getDate().split("-");
                                String format = date[2] + "/" + date[1] + "/" + date[0];
                                // Set stats in TextViews                       \
                                cityName.setText(cityStats[0].getCity_Name().replaceAll("שבט", "").replace("(", "").replace(")", "") + " נכון לתאריך: \n" + format);
                                // vaccined.setText(cityStats[0].getCumulated_vaccinated());
                                verified.setText(cityStats[0].getCumulative_verified_cases());
                                recovered.setText(cityStats[0].getCumulated_recovered());
                                tests.setText(cityStats[0].getCumulated_number_of_tests());
                                deaths.setText(cityStats[0].getCumulated_deaths());
                                // Stop the the loop
                            }
                            else{
                                Toast.makeText(getContext(),"נדרש שם של עיר הקיימת במאגר", Toast.LENGTH_LONG).show();
                            }
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

    @Override
    public void onCreateOptionsMenu(@NonNull Menu menu, @NonNull MenuInflater inflater) {
        inflater.inflate(R.menu.app_bar_options, menu);
        MenuItem searchItem = menu.findItem(R.id.filterCountries);
        SearchView searchView = (SearchView) searchItem.getActionView();
        searchView.setImeOptions(EditorInfo.IME_ACTION_DONE);

        searchView.setOnQueryTextListener(new SearchView.OnQueryTextListener() {
            @Override
            public boolean onQueryTextSubmit(String query) {
                treeSearching(query);
                return true;
            }

            @Override
            public boolean onQueryTextChange(String searchText) {
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
}
