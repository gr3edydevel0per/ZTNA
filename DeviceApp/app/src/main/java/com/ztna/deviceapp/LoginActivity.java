package com.ztna.deviceapp;

import android.content.Intent;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.View;
import android.widget.*;
import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONObject;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;

public class LoginActivity extends AppCompatActivity {
    private EditText username, password;
    private TextView loginError;

    private static final String LOGIN_URL = "http://owlguard.org:5069/api/users/login"; // Replace with local IP if using a real device

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        // Only for quick testing — for production, use AsyncTask or coroutines
        StrictMode.setThreadPolicy(new StrictMode.ThreadPolicy.Builder().permitAll().build());

        username = findViewById(R.id.username);
        password = findViewById(R.id.password);
        loginError = findViewById(R.id.loginError);
        Button loginButton = findViewById(R.id.loginButton);
        TextView forgotPassword = findViewById(R.id.forgotPassword);

        loginButton.setOnClickListener(v -> {
            String email = username.getText().toString().trim();
            String pass = password.getText().toString().trim();

            if (email.isEmpty() || pass.isEmpty()) {
                loginError.setText("Email and password are required");
                loginError.setVisibility(View.VISIBLE);
                return;
            }

            try {
                // Build JSON
                JSONObject credentials = new JSONObject();
                credentials.put("email", email);
                credentials.put("password", pass);

                // Send POST request
                URL url = new URL(LOGIN_URL);
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("POST");
                conn.setRequestProperty("Content-Type", "application/json; charset=UTF-8");
                conn.setDoOutput(true);

                // Write JSON to output
                OutputStream os = conn.getOutputStream();
                BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(os, "UTF-8"));
                writer.write(credentials.toString());
                writer.flush();
                writer.close();
                os.close();

                // Get response
                int responseCode = conn.getResponseCode();
                InputStream is = (responseCode == 200) ? conn.getInputStream() : conn.getErrorStream();
                BufferedReader reader = new BufferedReader(new InputStreamReader(is));
                StringBuilder sb = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) {
                    sb.append(line);
                }
                reader.close();
                conn.disconnect();

                // Parse JSON response
                JSONObject response = new JSONObject(sb.toString());
                if (response.getString("status").equals("success")) {
                    JSONObject data = response.getJSONObject("data");
                    String token = data.getString("token");
                    JSONObject user = data.getJSONObject("user");

                    String uuid = user.getString("uuid");
                    int departmentId = user.getInt("department_id");

                    // Start next activity
                    Intent intent = new Intent(LoginActivity.this, AuthorizationActivity.class);
                    intent.putExtra("TOKEN", token);
                    intent.putExtra("UUID", uuid);
                    intent.putExtra("DEPARTMENT_ID", departmentId);
                    startActivity(intent);
                    finish();
                } else {
                    runOnUiThread(() -> {
                        loginError.setText("Invalid credentials");
                        loginError.setVisibility(View.VISIBLE);
                    });
                }

            } catch (Exception e) {
                e.printStackTrace();
                runOnUiThread(() -> {
                    loginError.setText("Server error: " + e.getMessage());
                    loginError.setVisibility(View.VISIBLE);
                });
            }
        });
        forgotPassword.setOnClickListener(v -> {
            Intent intent = new Intent(LoginActivity.this, ForgotPasswordActivity.class);
            startActivity(intent);
        });
    }
}
