package com.coronacharts.appCurrentActivities;

import android.annotation.SuppressLint;
import android.app.Dialog;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.view.inputmethod.EditorInfo;
import android.widget.SearchView;
import android.widget.TextView;
import android.widget.Toast;

import com.coronacharts.R;
import com.github.mikephil.charting.charts.LineChart;
import com.github.mikephil.charting.components.AxisBase;
import com.github.mikephil.charting.components.XAxis;
import com.github.mikephil.charting.data.Entry;
import com.github.mikephil.charting.data.LineData;
import com.github.mikephil.charting.data.LineDataSet;
import com.github.mikephil.charting.formatter.IAxisValueFormatter;
import com.github.mikephil.charting.formatter.ValueFormatter;
import com.github.mikephil.charting.interfaces.datasets.ILineDataSet;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.Objects;

/**
 * Fragment for displaying graphs with crucial data and conclusions of the situations..
 */
public class FragmentGraphs extends Fragment {

    private DatabaseReference databaseReference;
    private View view;
    private TextView title1, title2, title3;
    private LineChart graph1, graph2, graph3;
    private LineDataSet lineDataSet = new LineDataSet(null, null);
    private LineDataSet lineDataSet2 = new LineDataSet(null, null);
    private LineDataSet lineDataSet3 = new LineDataSet(null, null);
    private ArrayList<ILineDataSet> sets1 = new ArrayList<>();
    private ArrayList<ILineDataSet> sets2 = new ArrayList<>();
    private ArrayList<ILineDataSet> sets3 = new ArrayList<>();

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
        title2 = view.findViewById(R.id.graph2_title);
        title3 = view.findViewById(R.id.graph3_title);
        graph1 = view.findViewById(R.id.graph1);
        graph1.setVisibility(View.INVISIBLE);
        graph2 = view.findViewById(R.id.graph2);
        graph2.setVisibility(View.INVISIBLE);
        graph3 = view.findViewById(R.id.graph3);
        graph3.setVisibility(View.INVISIBLE);
        String query = "ירושלים";
        treeSearching(query, graph1, "Cumulative_verified_cases", title1, sets1, lineDataSet);
        treeSearching(query, graph2, "Cumulated_recovered", title2, sets2, lineDataSet2);
        treeSearching(query, graph3, "Cumulated_deaths", title3, sets3, lineDataSet3);
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
                treeSearching(query, graph1,"Cumulative_verified_cases", title1, sets1, lineDataSet);
                treeSearching(query, graph2,  "Cumulated_recovered", title2, sets2, lineDataSet2);
                treeSearching(query, graph3, "Cumulated_deaths", title3, sets3, lineDataSet3);
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

    @SuppressLint("SetTextI18n")
    private void treeSearching(final String query, final LineChart graph, final String parameterForSearch, final TextView title, final ArrayList<ILineDataSet> sets, final LineDataSet lineDataSetFun) {
        final String[] finalQuery = new String[1];
        DatabaseReference databaseReference1 = FirebaseDatabase.getInstance().getReference("graphs_3").child("חולים לפי תאריך");
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
                databaseReference = FirebaseDatabase.getInstance().getReference("graphs_3").child("חולים לפי תאריך").child(finalQuery[0]).child("data").child(parameterForSearch);
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
                            String toTitle = "";
                            if(parameterForSearch.contains("verified")) {toTitle = "חולים לפי תאריך";}
                            else if(parameterForSearch.contains("recovered")) {toTitle = "מחלימים לפי תאריך";}
                            else if(parameterForSearch.contains("deaths")) {toTitle = "מתים לפי תאריך";}
                            title.setText(toTitle + " ב: " + finalQuery[0]);
                            updateGraph(new ArrayList<>(values), graph, title.getText().toString(), sets, lineDataSetFun);
                            finalQuery[0] = null;
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


    private void updateGraph(ArrayList<Entry> values, LineChart graph, String labelTitle, ArrayList<ILineDataSet> sets, LineDataSet lineDataSetFun) {
        // Creates a graph
        graph.setVisibility(View.VISIBLE);
        lineDataSetFun.setValues(values);
        lineDataSetFun.setLabel(labelTitle);
        sets.clear();
        sets.add(lineDataSetFun);
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
        // Date formatter
        @Override
        public String getFormattedValue(float value, AxisBase axis) {
            Date date = new Date((long) value);
            @SuppressLint("SimpleDateFormat")
            SimpleDateFormat simpleDateFormat = new SimpleDateFormat("dd/MM");
            return simpleDateFormat.format(date);
        }
    }
}

