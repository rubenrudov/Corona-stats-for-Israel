package com.coronacharts;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.app.AlarmManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import com.coronacharts.notification_classes.NotificationReceiver;

import java.util.Calendar;

public class NotificationSettingActivity extends AppCompatActivity {
    Button setAlarm;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_notification_setting);
        setAlarm = findViewById(R.id.setAlarmToUpdateEveryday);
        setAlarm.setOnClickListener(new View.OnClickListener() {
            @SuppressLint("ShortAlarm")
            @Override
            public void onClick(View v) {
                AlarmManager alarmManager = (AlarmManager)getApplicationContext().getSystemService(Context.ALARM_SERVICE);
                Intent intent = new Intent(getApplicationContext(), NotificationReceiver.class);
                PendingIntent alarmIntent = PendingIntent.getBroadcast(getApplicationContext(), 0, intent, 0);

                Calendar calendar = Calendar.getInstance();
                calendar.setTimeInMillis(System.currentTimeMillis());
                calendar.set(Calendar.HOUR_OF_DAY, 9);
                calendar.set(Calendar.MINUTE, 47);
                assert alarmManager != null;
                alarmManager.setRepeating(AlarmManager.RTC_WAKEUP, 100,
                        AlarmManager.INTERVAL_DAY, alarmIntent);
                startActivity(new Intent(NotificationSettingActivity.this, MainActivity.class));
                finish();
            }
        });
        finish();
    }
}
