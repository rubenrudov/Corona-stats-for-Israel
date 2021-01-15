package com.coronacharts.appCurrentActivities;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.Handler;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ImageView;

import com.coronacharts.R;

public class SplashActivity extends AppCompatActivity {
    // TODO: Add notification each 24 hour handling
    SharedPreferences sp;
    @SuppressLint("CommitPrefEdits")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash);
        // Animation setting
        Animation slide  = AnimationUtils.loadAnimation(this, R.anim.side_slide_anomation);
        ImageView bg = findViewById(R.id.bg);
        bg.startAnimation(slide);
        new Handler().postDelayed(new Runnable() {
            @Override
            public void run() {
                startActivity(new Intent(SplashActivity.this, MainActivity.class));
            }
        }, 1500);
    }
}
