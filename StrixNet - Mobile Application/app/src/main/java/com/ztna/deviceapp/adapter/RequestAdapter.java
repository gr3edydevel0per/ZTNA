package com.ztna.deviceapp.adapter;

import android.content.Context;
import android.content.Intent;
import android.os.Handler;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.ztna.deviceapp.ActivityConnect;
import com.ztna.deviceapp.ActivityDecline;
import com.ztna.deviceapp.model.DeviceRequest;

public class RequestAdapter {

    public static View createRequestView(Context context, DeviceRequest request) {
        LinearLayout card = new LinearLayout(context);
        card.setOrientation(LinearLayout.VERTICAL);
        card.setBackgroundColor(0xFFF5F5F5); // light gray
        card.setPadding(24, 24, 24, 24);
        LinearLayout.LayoutParams cardParams = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
        );
        cardParams.setMargins(0, 0, 0, 20);
        card.setLayoutParams(cardParams);
        card.setElevation(6f);

        // Device Name
        TextView nameView = new TextView(context);
        nameView.setText(request.getDeviceName());
        nameView.setTextSize(18);
        nameView.setTextColor(0xFF000000);
        nameView.setPadding(0, 0, 0, 8);
        card.addView(nameView);

        // IP Address
        TextView ipView = new TextView(context);
        ipView.setText("IP: " + request.getIpAddress());
        card.addView(ipView);

        // MAC Address
        TextView macView = new TextView(context);
        macView.setText("MAC: " + request.getMacAddress());
        card.addView(macView);

        // Buttons container
        LinearLayout buttonsLayout = new LinearLayout(context);
        buttonsLayout.setOrientation(LinearLayout.HORIZONTAL);
        buttonsLayout.setGravity(Gravity.END);
        buttonsLayout.setPadding(0, 16, 0, 0);

        // Accept Button
        Button acceptBtn = new Button(context);
        acceptBtn.setText("Allow");
        acceptBtn.setBackgroundColor(0xFF4CAF50);
        acceptBtn.setTextColor(0xFFFFFFFF);
        buttonsLayout.addView(acceptBtn);

        // Decline Button
        Button declineBtn = new Button(context);
        declineBtn.setText("Decline");
        declineBtn.setBackgroundColor(0xFFF44336);
        declineBtn.setTextColor(0xFFFFFFFF);
        buttonsLayout.addView(declineBtn);

        card.addView(buttonsLayout);

        // Button Logic
        acceptBtn.setOnClickListener(v -> {
            // TODO: Send Accept Response to server
            context.startActivity(new Intent(context, ActivityConnect.class));
            delayedReturn(context);
        });

        declineBtn.setOnClickListener(v -> {
            // TODO: Send Decline Response to server
            context.startActivity(new Intent(context, ActivityDecline.class));
            delayedReturn(context);
        });

        return card;
    }

    private static void delayedReturn(Context context) {
        new Handler().postDelayed(() -> {
            Intent backIntent = new Intent(context, com.ztna.deviceapp.AuthorizationActivity.class);
            backIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
            context.startActivity(backIntent);
        }, 12000); // 12 seconds
    }
}
