package com.coronacharts.handlers;

import android.annotation.SuppressLint;
import android.app.Dialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.text.Layout;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.widget.Adapter;
import android.widget.Filter;
import android.widget.Filterable;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.ContentView;
import androidx.annotation.NonNull;
import androidx.constraintlayout.widget.ConstraintLayout;
import androidx.recyclerview.widget.RecyclerView;
import com.coronacharts.R;
import com.coronacharts.models.Country;

import java.lang.invoke.ConstantCallSite;
import java.util.ArrayList;
import java.util.Objects;

public class CountriesAdapter extends RecyclerView.Adapter<CountriesAdapter.ViewHolder> implements Filterable {

    private Context context;
    private ArrayList<Country> countries, countriesDuplicate;

    public CountriesAdapter(Context context, ArrayList<Country> countries) {
        this.context = context;
        this.countries = countries;
        countriesDuplicate = new ArrayList<>(countries);
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        return new CountriesAdapter.ViewHolder(LayoutInflater.from(context).inflate(R.layout.recycler_view_item, parent, false));
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder viewHolder, final int index) {
        Country country = countries.get(index);
        viewHolder.country.setText(country.getName());
        switch (country.getStatus()) {
            case "אדום":
                viewHolder.country.setBackgroundColor(Color.rgb(178, 0, 0));
                viewHolder.country.setTextColor(Color.WHITE);
                break;
            case "ירוק":
                viewHolder.country.setBackgroundColor(Color.rgb(0, 178, 0));
                viewHolder.country.setTextColor(Color.WHITE);
                break;
            case "סטטוס":
                viewHolder.country.setBackgroundColor(Color.WHITE);
                viewHolder.country.setTextColor(Color.BLACK);
                break;
        }
        viewHolder.itemView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(context, Country.class);
                intent.putExtra("Name", CountriesAdapter.this.countriesDuplicate.get(index).getName());
                intent.putExtra("Status", CountriesAdapter.this.countriesDuplicate.get(index).getStatus());
                // intent.putExtra("Name", CountriesAdapter.this.countriesDuplicate.get(index).getIsoType());
                // intent.putExtra("Name", CountriesAdapter.this.countriesDuplicate.get(index).getLastUpdate());
                final DestinationDataDialog dialog = new DestinationDataDialog(context, intent);
                dialog.requestWindowFeature(Window.FEATURE_NO_TITLE);
                dialog.setContentView(R.layout.guide_diaglog);
                // TODO: Create dialog view of country & it's data following the db
                dialog.show();
            }
        });
    }

    @Override
    public int getItemCount() {
        return countries.size();
    }

    @Override
    public Filter getFilter() {
        return filter;
    }

    private Filter filter = new Filter() {
        @Override
        protected FilterResults performFiltering(CharSequence constraint) {
            ArrayList<Country> filtered = new ArrayList<>();
            if (constraint == null || constraint.length() == 0){
                filtered.addAll(CountriesAdapter.this.countriesDuplicate);
            }
            else {
                String pattern = constraint.toString().toLowerCase().trim();
                for (Country country: CountriesAdapter.this.countries) {
                    if(country.getName().toLowerCase().contains(pattern) || country.getStatus().toLowerCase().contains(pattern)){
                        filtered.add(country);
                    }
                    else if (constraint.length() == 0){
                        filtered.clear();
                        filtered.addAll(CountriesAdapter.this.countriesDuplicate);
                    }
                }
            }
            FilterResults results = new FilterResults();
            results.values = filtered;
            return results;
        }

        @Override
        protected void publishResults(CharSequence constraint, FilterResults results) {
            CountriesAdapter.this.countries.clear();
            CountriesAdapter.this.countries.addAll((ArrayList<Country>) results.values);
            notifyDataSetChanged();
        }
    };

    public void updateData(ArrayList<Country> cs) {
        countriesDuplicate.clear();
        countriesDuplicate.addAll(cs);
        notifyDataSetChanged();
    }

    static class ViewHolder extends RecyclerView.ViewHolder {
        TextView country;
        ViewHolder(@NonNull View itemView) {
            super(itemView);
            country = itemView.findViewById(R.id.country);
        }
    }

    static class DestinationDataDialog extends Dialog {
        Context context;
        Intent intent;
        public TextView countryName, countyStatus, isoType, lastUpdate;
        public DestinationDataDialog(@NonNull Context context, Intent intent) {
            super(context);
            this.context = context;
            this.intent = intent;
        }

        @SuppressLint("SetTextI18n")
        @Override
        protected void onCreate(Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);
            setContentView(R.layout.country_data_dialog);
            this.countryName  = findViewById(R.id.name);
            this.countryName.setText("שם: " + Objects.requireNonNull(this.intent.getExtras()).getString("Name"));
            this.countyStatus  = findViewById(R.id.status);
            this.countyStatus.setText( "סטטוס: " + Objects.requireNonNull(this.intent.getExtras()).getString("Status"));
            // TODO this.isoType  = ;
            // TODO this.lastUpdate  = ;
            ConstraintLayout constraintLayout = findViewById(R.id.dialogBg);
            switch (countyStatus.getText().toString()){
                case "סטטוס: אדום":
                    constraintLayout.setBackgroundResource(R.drawable.country_dialog_bg);
                    break;
                case "סטטוס: ירוק":
                    constraintLayout.setBackgroundResource(R.drawable.country_dialog_bg2);
                    break;
            }
        }
    }

}
