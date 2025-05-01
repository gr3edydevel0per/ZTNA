#!/bin/sh

SESSION_TOKEN=$UV_TOKEN
DEVICE_ID=$UV_DEVICE_ID
UUID=$UV_UID
DEVICE_NAME=$UV_DEVICE_NAME 
IP_ADDRESS=$UV_IP_ADDRESS   
AUTH_REQ_URL="http://<ENDPOINT:PORT>/api/devices/isAuthorized"
NOTI_REQ_URL="http://<ENDPOINT:PORT>/api/devices/device-auth-req"
CHECK_REQ_URL="http://<ENDPOINT:PORT>/api/devices/check-device-auth-res?uuid=$UUID"

echo "${SESSION_TOKEN}" >> /var/scripts/extras.log

# Check if device_id and uuid exist
if [ -z "$DEVICE_ID" ] || [ -z "$UUID" ]; then
    echo "Missing device_id or uuid for ${UUID}" >&2
    exit 1
fi

# Step 1: Check authorization
API_RESPONSE=$(curl -s -X POST "$AUTH_REQ_URL" \
    -H "Authorization: Bearer $SESSION_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"device_id\": \"$DEVICE_ID\", \"uuid\": \"$UUID\"}")

echo "API Response: $API_RESPONSE"

STATUS=$(echo "$API_RESPONSE" | jq -r '.status')

# Step 2: If authorized, send auth request
if [ "$STATUS" = "success" ]; then
    echo "Device authorization successful for ${UUID}"

    SEND_NOTI=$(curl -s -X POST "$NOTI_REQ_URL" \
        -H "Authorization: Bearer $SESSION_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{
              \"uuid\": \"$UUID\",
              \"device_id\": \"$DEVICE_ID\",
              \"device_name\": \"$DEVICE_NAME\",
              \"ip_address\": \"$IP_ADDRESS\"
            }")

    echo "Device Auth Request Sent: $SEND_NOTI"

    # Step 3: Poll for approval/denial for up to 1 minute (6 checks, 10s apart)
    echo "Waiting for user response..."
    for i in $(seq 1 6); do
        RESPONSE=$(curl -s -X GET "$CHECK_REQ_URL" \
            -H "Authorization: Bearer $SESSION_TOKEN")

        DECISION=$(echo "$RESPONSE" | jq -r '.decision')

        echo "Check $i - Decision: $DECISION"

        if [ "$DECISION" = "approved" ]; then
            echo "Device access approved."
            exit 0
        elif [ "$DECISION" = "denied" ]; then
            echo "Device access denied." >&2
            exit 1
        fi

        sleep 6
    done

    echo "Timed out waiting for user decision." >&2
    exit 1
else
    echo "Unauthorized device: ${UUID}" >&2
    exit 1
fi