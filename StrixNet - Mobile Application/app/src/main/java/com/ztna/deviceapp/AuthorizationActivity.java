package com.ztna.deviceapp;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.view.Gravity;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;
import android.os.AsyncTask;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.*;

import androidx.appcompat.app.AppCompatActivity;
import com.ztna.deviceapp.model.DeviceRequest;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import android.os.Looper;




public class AuthorizationActivity extends AppCompatActivity {
    private String token;
    private String uuid;
    private LinearLayout requestContainer;
    private final Handler pollHandler = new Handler();
    private final int POLL_INTERVAL = 10000; // 10 seconds
    private final ExecutorService executor = Executors.newSingleThreadExecutor();
    private final Handler mainHandler = new Handler(Looper.getMainLooper());

    private final Runnable pollRunnable = new Runnable() {
        @Override
        public void run() {
            fetchRequestsFromServer();
            pollHandler.postDelayed(this, POLL_INTERVAL);
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_authorization);
        // Get token and uuid from intent
        token = getIntent().getStringExtra("TOKEN");
        uuid = getIntent().getStringExtra("UUID");
        requestContainer = findViewById(R.id.requestContainer);
        pollHandler.post(pollRunnable); // Start polling
    }

    private void fetchRequestsFromServer() {
        ExecutorService executor = Executors.newSingleThreadExecutor();
        Handler handler = new Handler(Looper.getMainLooper());

        executor.execute(() -> {
            List<DeviceRequest> list = new ArrayList<>();
            try {
                // Build the URL with query parameter
                String requestUrl = "http://owlguard.org:5069/api/devices/check-device-auth-req?uuid=" + uuid;
                URL url = new URL(requestUrl);

                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("GET");
                conn.setRequestProperty("Authorization", "Bearer " + token); // Include auth token

                int responseCode = conn.getResponseCode();
                if (responseCode == 200) {
                    Scanner scanner = new Scanner(conn.getInputStream());
                    StringBuilder json = new StringBuilder();
                    while (scanner.hasNext()) json.append(scanner.nextLine());
                    scanner.close();

                    JSONObject response = new JSONObject(json.toString());
                    JSONArray arr = response.getJSONArray("data");

                    for (int i = 0; i < arr.length(); i++) {
                        JSONObject obj = arr.getJSONObject(i);
                        list.add(new DeviceRequest(
                                obj.getString("device_name"),
                                obj.getString("ip_address"),
                                obj.getString("device_id"),
                                obj.getString("uuid")
                        ));
                    }
                }
            } catch (Exception e) {
                e.printStackTrace();
            }

            handler.post(() -> {
                requestContainer.removeAllViews();
                for (DeviceRequest req : list) {
                    addRequestView(req);
                }
            });
        });
    }

    private void addRequestView(DeviceRequest request) {
        LinearLayout card = new LinearLayout(this);
        card.setOrientation(LinearLayout.VERTICAL);
        card.setPadding(24, 24, 24, 24);
        card.setBackgroundColor(0xFFEFEFEF);

        TextView name = new TextView(this);
        name.setText("Device: " + request.getDeviceName());
        card.addView(name);

        TextView ip = new TextView(this);
        ip.setText("IP: " + request.getIpAddress());
        card.addView(ip);

        TextView mac = new TextView(this);
        mac.setText("Device ID: " + request.getMacAddress());
        card.addView(mac);

        LinearLayout buttons = new LinearLayout(this);
        buttons.setGravity(Gravity.END);

        Button allow = new Button(this);
        allow.setText("Allow");
        allow.setOnClickListener(v -> {
            sendResponseToServer(request, true);
            showResultScreen(ActivityConnect.class);
        });

        Button deny = new Button(this);
        deny.setText("Deny");
        deny.setOnClickListener(v -> {
            sendResponseToServer(request, false);
            showResultScreen(ActivityDecline.class);
        });

        buttons.addView(allow);
        buttons.addView(deny);
        card.addView(buttons);
        requestContainer.addView(card);
    }

    private void sendResponseToServer(DeviceRequest req, boolean allow) {
        new Thread(() -> {
            try {
                URL url = new URL("http://owlguard.org:5069/api/devices/device-response");
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("POST");
                conn.setRequestProperty("Content-Type", "application/json");
                conn.setRequestProperty("Authorization", "Bearer " + token); // ✅ Add token here
                conn.setDoOutput(true);

                JSONObject body = new JSONObject();
                body.put("uuid", req.getUuid());
                body.put("device_id", req.getMacAddress());
                body.put("decision", allow ? "approved" : "denied");

                OutputStream os = conn.getOutputStream();
                os.write(body.toString().getBytes("UTF-8"));
                os.flush();
                os.close();

                int responseCode = conn.getResponseCode();
                if (responseCode == 200) {
                    runOnUiThread(() ->
                            Toast.makeText(this, "Response sent", Toast.LENGTH_SHORT).show());
                } else {
                    runOnUiThread(() ->
                            Toast.makeText(this, "Failed: " + responseCode, Toast.LENGTH_SHORT).show());
                }

                conn.disconnect();

            } catch (Exception e) {
                runOnUiThread(() ->
                        Toast.makeText(this, "Failed to respond", Toast.LENGTH_SHORT).show());
                e.printStackTrace();
            }
        }).start();
    }

    private void showResultScreen(Class<?> target) {
        Intent intent = new Intent(this, target);
        intent.putExtra("TOKEN", token);
        intent.putExtra("UUID", uuid);
        startActivity(intent);

        new Handler().postDelayed(() -> {
            Intent backIntent = new Intent(this, AuthorizationActivity.class);
            backIntent.putExtra("TOKEN", token);  // Pass them again
            backIntent.putExtra("UUID", uuid);
            startActivity(backIntent);
            finish();
        }, 10000);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        pollHandler.removeCallbacks(pollRunnable);
    }
}
