package com.coronacharts.upcomingNext;

import android.graphics.Color;
import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.coronacharts.R;
import com.github.mikephil.charting.charts.Chart;
import com.github.mikephil.charting.charts.PieChart;
import com.github.mikephil.charting.components.Description;
import com.github.mikephil.charting.data.PieData;
import com.github.mikephil.charting.data.PieDataSet;
import com.github.mikephil.charting.data.PieEntry;
import com.github.mikephil.charting.utils.ColorTemplate;

import java.util.ArrayList;


/**
    A fragment for displaying charts, will be added in the next version of the app.
 */
public class FragmentCharts extends Fragment {
    public FragmentCharts() {

    }
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_charts, container, false);
        ArrayList<String> ageGroups = createAgeList();
        // sickByAge = view.findViewById(R.id.sickByAge);
        // chartSetting(sickByAge, ageGroups);
        return view;
    }

    private void chartSetting(PieChart pieChart, ArrayList<String> categories){
        ArrayList<PieEntry> entries = new ArrayList<>();
        for (int i = 0; i < categories.toArray().length; i++){
            entries.add( new PieEntry(50 * i + 100 ,categories.toArray()[i].toString()));
        }
        //
        PieDataSet pieDataSet = new PieDataSet(entries, "התפלגות תחלואה לפי קבוצות גיל");
        pieDataSet.setColors(ColorTemplate.LIBERTY_COLORS);
        pieDataSet.setValueTextColor(Color.BLACK);
        pieDataSet.setValueTextSize(14f);
        //
        PieData pieData = new PieData(pieDataSet);
        //
        pieChart.setData(pieData);
        pieChart.getDescription().setEnabled(false);
        pieChart.setDrawHoleEnabled(false);
        pieChart.getLegend().setEnabled(false);
        pieChart.setEntryLabelColor(Color.BLACK);
        pieChart.setEntryLabelTextSize(11f);
        pieChart.animate();
    }

    private ArrayList<String> createAgeList(){
        // For clean onCreateView code.
        ArrayList<String> lst = new ArrayList<>();
        lst.add("0-19.9");
        lst.add("20-29.9");
        lst.add("30-39.9");
        lst.add("40-49.9");
        lst.add("50-59.9");
        lst.add("60-69.9");
        lst.add("70-79.9");
        lst.add("80+");
        return lst;
    }
}
