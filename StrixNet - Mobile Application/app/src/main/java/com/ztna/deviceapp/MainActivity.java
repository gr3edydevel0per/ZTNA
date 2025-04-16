package com.ztna.deviceapp;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.os.Handler;
import android.os.Looper;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.ImageView;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Animate wave_shape
        View waveContainer = findViewById(R.id.waveContainer);
        Animation scrollAnim = AnimationUtils.loadAnimation(this, R.anim.wave_slide);
        waveContainer.startAnimation(scrollAnim);



        // Auto navigate to login page after 5 seconds
        new Handler(Looper.getMainLooper()).postDelayed(() -> {
            Intent intent = new Intent(MainActivity.this, LoginActivity.class);
            startActivity(intent);
            overridePendingTransition(R.anim.fade_in, R.anim.fade_out);
            finish();
        }, 5000);
    }
}
