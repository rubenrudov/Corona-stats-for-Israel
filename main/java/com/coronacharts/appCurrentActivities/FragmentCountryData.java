package com.coronacharts.appCurrentActivities;

import android.app.Dialog;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;

import com.coronacharts.R;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.ArrayList;
import java.util.Objects;

import javax.annotation.Nullable;

public class FragmentCountryData extends Fragment {
    private DatabaseReference databaseReference;
    private TextView active, verified, recovered, deaths;
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
        active = view.findViewById(R.id.active);
        verified = view.findViewById(R.id.verified);
        recovered = view.findViewById(R.id.healed);
        deaths = view.findViewById(R.id.dead);
        getData("Active", active);
        getData("Confirmed", verified);
        getData("Recovered", recovered);
        getData("Deaths", deaths);
    }

    private void getData(String query, final TextView active) {
        databaseReference = FirebaseDatabase.getInstance().getReference().child("israel_UN_WHO").child(query);
        databaseReference.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot snapshot) {
                setTextForTextView(active, String.valueOf(snapshot.getValue(Long.class)));
            }

            @Override
            public void onCancelled(@NonNull DatabaseError error) {

            }
        });
    }


    private void setTextForTextView(TextView view, String param) {
        view.setText(param);
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
            Dialog dialog = new Dialog(Objects.requireNonNull(getContext()));
            dialog.requestWindowFeature(Window.FEATURE_NO_TITLE);
            dialog.setContentView(R.layout.guide_diaglog);
            dialog.show();
        }
        return super.onOptionsItemSelected(item);
    }
}
