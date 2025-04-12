package com.ztna.deviceapp;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;

import androidx.appcompat.app.AppCompatActivity;

public class ActivityConnect extends AppCompatActivity {

    private static final int DELAY_DURATION = 12000; // 12 seconds

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_connect);

        // Redirect after delay
        new Handler().postDelayed(() -> {
            Intent intent = new Intent(ActivityConnect.this, AuthorizationActivity.class);
            intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_NEW_TASK);
            startActivity(intent);
            finish();
        }, DELAY_DURATION);
    }
}
