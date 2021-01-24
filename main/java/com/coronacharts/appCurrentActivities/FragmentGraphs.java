package com.coronacharts.appCurrentActivities;

import android.annotation.SuppressLint;
import android.app.AlertDialog;
import android.graphics.Canvas;
import android.graphics.ColorFilter;
import android.graphics.drawable.Drawable;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.view.inputmethod.EditorInfo;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.SearchView;
import android.widget.TextView;
import android.widget.Toast;

import com.coronacharts.R;
import com.coronacharts.handlers.GraphPoint;
import com.github.mikephil.charting.charts.LineChart;
import com.github.mikephil.charting.components.AxisBase;
import com.github.mikephil.charting.components.XAxis;
import com.github.mikephil.charting.data.Entry;
import com.github.mikephil.charting.data.LineData;
import com.github.mikephil.charting.data.LineDataSet;
import com.github.mikephil.charting.formatter.IAxisValueFormatter;
import com.github.mikephil.charting.formatter.IndexAxisValueFormatter;
import com.github.mikephil.charting.formatter.ValueFormatter;
import com.github.mikephil.charting.interfaces.datasets.ILineDataSet;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.EventListener;
import java.util.Map;
import java.util.Objects;
import java.util.SimpleTimeZone;

/**
 * Fragment for displaying graphs with crucial data and conclusions of the situations..
 */
public class FragmentGraphs extends Fragment {

    private DatabaseReference databaseReference;
    private View view;
    private TextView title1, title2, title3;
    private LineChart graph1, graph2, graph3;
    private LineDataSet lineDataSet = new LineDataSet(null, null);
    private ArrayList<ILineDataSet> sets = new ArrayList<>();

    public FragmentGraphs() {
        // Required empty constructor
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        setHasOptionsMenu(true);
        view = inflater.inflate(R.layout.fragment_graphs, container, false);
        setElements();
        return view;
    }

    private void setElements() {
        title1 = view.findViewById(R.id.graph1_title);
        graph1 = view.findViewById(R.id.graph1);
        graph1.setVisibility(View.INVISIBLE);
        String currentCity = "ירושלים";
        treeSearching(currentCity);
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
                treeSearching(query, graph1, "חולים לפי תאריך");
                // treeSearching(query, graph2);
                // treeSearching(query, graph3);
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
            AlertDialog.Builder builder = new AlertDialog.Builder(getContext());
            View viewGroup = view.findViewById(android.R.id.custom);
            View dialogView = LayoutInflater.from(view.getContext()).inflate(R.layout.guide_diaglog, (ViewGroup) viewGroup, false);
            builder.setView(dialogView);
            AlertDialog alertDialog = builder.create();
            alertDialog.show();
        }
        return super.onOptionsItemSelected(item);
    }

    @SuppressLint("SetTextI18n")
    private void treeSearching(final String query, final LineChart graph, final String parameterForSearch) {
        final String[] finalQuery = new String[1];
        DatabaseReference databaseReference1 = FirebaseDatabase.getInstance().getReference("graphs").child(parameterForSearch);
        databaseReference1.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot snapshot) {
                for(DataSnapshot val : snapshot.getChildren()){
                    if(Objects.requireNonNull(val.getKey()).contains(query)){
                        finalQuery[0] = val.getKey();
                        break;
                    }
                }
                if (finalQuery[0] == null)
                    finalQuery[0] = query;
                databaseReference = FirebaseDatabase.getInstance().getReference("graphs").child(parameterForSearch).child(finalQuery[0]).child("data").child("Cumulative_verified_cases");
                databaseReference.addValueEventListener(new ValueEventListener() {
                    @Override
                    public void onDataChange(@NonNull DataSnapshot snapshot) {
                        ArrayList<Entry> values = new ArrayList<>();
                        int i = 0;
                        for (DataSnapshot dataSnapshot: snapshot.getChildren()){
                            assert dataSnapshot.getValue() != null;
                            values.add(new Entry(i, Integer.parseInt((String) dataSnapshot.getValue())));
                            i++;
                        }
                        if (values.size() != 0){
                            title1.setText(parameterForSearch + "ב:" + finalQuery[0]);
                            updateGraph(new ArrayList<>(values), graph);
                        }
                        else {
                            Toast.makeText(getContext(), "העיר אינה קיימת במאגר", Toast.LENGTH_SHORT).show();
                        }
                    }
                    @Override
                    public void onCancelled(@NonNull DatabaseError error) {

                    }
                });
            }

            @Override
            public void onCancelled(@NonNull DatabaseError error) {

            }
        });
    }


    private void updateGraph(ArrayList<Entry> values, LineChart graph) {
        // Creates a graph
        graph1.setVisibility(View.VISIBLE);
        lineDataSet.setValues(values);
        lineDataSet.setLabel("חולים לפי תאריך");
        sets.clear();
        sets.add(lineDataSet);
        LineData lineData = new LineData(sets);
        graph.clear();
        graph.getDescription().setEnabled(false);
        graph.getXAxis().setPosition(XAxis.XAxisPosition.BOTTOM);
        graph.getXAxis().setEnabled(true);
        graph.getXAxis().setValueFormatter(new DateValueFormatter());
        graph.setData(lineData);
        graph.invalidate();
    }

    private static class DateValueFormatter extends ValueFormatter implements IAxisValueFormatter{
        @Override
        public String getFormattedValue(float value, AxisBase axis) {
            Date date = new Date((long) value);
            @SuppressLint("SimpleDateFormat")
            SimpleDateFormat simpleDateFormat = new SimpleDateFormat("dd/MM");
            return simpleDateFormat.format(date);
        }
    }
}

