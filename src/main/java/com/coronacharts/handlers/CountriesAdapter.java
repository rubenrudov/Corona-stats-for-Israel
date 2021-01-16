package com.coronacharts.handlers;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import com.coronacharts.R;
import com.coronacharts.models.Country;
import java.util.ArrayList;

public class CountriesAdapter extends RecyclerView.Adapter<CountriesAdapter.ViewHolder> {

    private Context context;
    private ArrayList<Country> countries;

    public CountriesAdapter(Context context, ArrayList<Country> countries) {
        this.context = context;
        this.countries = countries;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        if(viewType == 1){
            return new CountriesAdapter.ViewHolder(LayoutInflater.from(context).inflate(R.layout.recycler_view_item_green, parent, false));
        } else{
            return new CountriesAdapter.ViewHolder(LayoutInflater.from(context).inflate(R.layout.recycler_view_item_red, parent, false));
        }
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder viewHolder, int index) {
        Country country = countries.get(index);
        viewHolder.country.setText(country.getName());
        viewHolder.statusOfCountry.setText(country.getStatus());
    }

    @Override
    public int getItemCount() {
        return countries.size();
    }

    @Override
    public int getItemViewType(int index) {
        String status = countries.get(index).getStatus();
        return status.equals("ירוק") ? 1 : 0;
    }

    static class ViewHolder extends RecyclerView.ViewHolder {
        TextView country, statusOfCountry;
        ViewHolder(@NonNull View itemView) {
            super(itemView);
            country = itemView.findViewById(R.id.country);
            statusOfCountry = itemView.findViewById(R.id.statusOfCountry);
        }
    }
}
