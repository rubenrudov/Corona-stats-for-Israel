package com.coronacharts.models;

import com.google.android.gms.maps.model.LatLng;

public class Country {
    private String name;
    private String status;
    // private LatLng location; - Next versions...


    public Country(String name, String status) {
        this.name = name;
        this.status = status;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    @Override
    public String toString() {
        return "State{" +
                "name='" + name + '\'' +
                ", status='" + status + '\'' +
                '}';
    }
}
