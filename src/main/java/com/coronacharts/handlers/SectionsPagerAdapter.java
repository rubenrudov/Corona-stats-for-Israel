package com.coronacharts.handlers;

import android.content.Context;

import androidx.annotation.Nullable;
import androidx.annotation.StringRes;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentPagerAdapter;

import com.coronacharts.appCurrentActivities.FragmentByCity;
import com.coronacharts.appCurrentActivities.FragmentCountryData;
import com.coronacharts.appCurrentActivities.FragmentRedCountries;
import com.coronacharts.R;

/**
 * A [FragmentPagerAdapter] that returns a fragment corresponding to
 * one of the sections/tabs/pages.
 */
public class SectionsPagerAdapter extends FragmentPagerAdapter {

    @StringRes
    private static final int[] TAB_TITLES = new int[]{R.string.by_city_fragment_title, R.string.whole_country_fragment_title, R.string.states_list};
    private final Context mContext;

    public SectionsPagerAdapter(Context context, FragmentManager fm) {
        super(fm);
        mContext = context;
    }

    @Override
    public Fragment getItem(int position) {
        Fragment fragment = new FragmentCountryData();;
        switch (position){
            case 0:
                fragment = new FragmentByCity();
                break;
            case 1:
                fragment = new FragmentCountryData();
                break;
            /* case 2:
                fragment = new FragmentCharts();
                break;
            */
            case 2:
                fragment = new FragmentRedCountries();
                break;
        }
        return fragment;
    }

    @Nullable
    @Override
    public CharSequence getPageTitle(int position) {
        return mContext.getResources().getString(TAB_TITLES[position]);
    }

    @Override
    public int getCount() {
        // Total amount of pages in this tab layout
        return 3;
    }
}