package com.coronacharts.models;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

public class CityStats {
    private String City_Code;
    private String City_Name;
    private String Cumulated_deaths;
    private String Cumulated_number_of_diagnostic_tests;
    private String Cumulated_number_of_tests;
    private String Cumulated_recovered;
    // private String Cumulated_vaccinated;
    private String Cumulative_verified_cases;
    @Nullable private String Date;
    private String _id;

    public CityStats(){ }

    public CityStats(String city_Code, String city_Name, String cumulated_deaths, String cumulated_diagnostic, String cumulated_number_of_tests, String cumulated_recovered, String cumulative_verified_cases, String date, String _id) {
        City_Code = city_Code;
        City_Name = city_Name;
        Cumulated_deaths = cumulated_deaths;
        Cumulated_number_of_diagnostic_tests = cumulated_diagnostic;
        Cumulated_number_of_tests = cumulated_number_of_tests;
        Cumulated_recovered = cumulated_recovered;
        // Cumulated_vaccinated = cumulated_vaccinated;
        Cumulative_verified_cases = cumulative_verified_cases;
        Date = date;
        this._id = _id;
    }

    public String getCity_Code() {
        return City_Code;
    }

    public void setCity_Code(String city_Code) {
        City_Code = city_Code;
    }

    public String getCity_Name() {
        return City_Name;
    }

    public void setCity_Name(String city_Name) {
        City_Name = city_Name;
    }

    public String getCumulated_deaths() {
        return Cumulated_deaths;
    }

    public void setCumulated_deaths(String cumulated_deaths) {
        Cumulated_deaths = cumulated_deaths;
    }

    public String getCumulated_number_of_diagnostic_tests() {
        return Cumulated_number_of_diagnostic_tests;
    }

    public void setCumulated_number_of_diagnostic_tests(String cumulated_number_of_diagnostic_tests) {
        Cumulated_number_of_diagnostic_tests = cumulated_number_of_diagnostic_tests;
    }

    public String getCumulated_number_of_tests() {
        return Cumulated_number_of_tests;
    }

    public void setCumulated_number_of_tests(String cumulated_number_of_tests) {
        Cumulated_number_of_tests = cumulated_number_of_tests;
    }

    public String getCumulated_recovered() {
        return Cumulated_recovered;
    }

    public void setCumulated_recovered(String cumulated_recovered) {
        Cumulated_recovered = cumulated_recovered;
    }

    // public String getCumulated_vaccinated() {
    //    return Cumulated_vaccinated;
    // }

    // public void setCumulated_vaccinated(String cumulated_vaccinated) {
    //    Cumulated_vaccinated = cumulated_vaccinated;
    // }

    public String getCumulative_verified_cases() {
        return Cumulative_verified_cases;
    }

    public void setCumulative_verified_cases(String cumulative_verified_cases) {
        Cumulative_verified_cases = cumulative_verified_cases;
    }

    public String getDate() {
        return Date;
    }

    public void setDate(String date) {
        Date = date;
    }

    public String get_id() {
        return _id;
    }

    public void set_id(String _id) {
        this._id = _id;
    }

    @NonNull
    @Override
    public String toString() {
        return "CityStats{" +
                "City_Code='" + City_Code + '\'' +
                ", City_Name='" + City_Name + '\'' +
                ", Cumulated_deaths='" + Cumulated_deaths + '\'' +
                ", Cumulated_number_of_tests='" + Cumulated_number_of_tests + '\'' +
                ", Cumulated_recovered='" + Cumulated_recovered + '\'' +
                ", Cumulative_verified_cases='" + Cumulative_verified_cases + '\'' +
                ", Date='" + Date + '\'' +
                ", _id=" + _id +
                '}';
    }

    @Override
    protected void finalize() throws Throwable {
        super.finalize();
    }
}
