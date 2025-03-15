from flask import Flask, request, jsonify, session, render_template, redirect, url_for, make_response
import requests
from utils.essentials import get_current_machine_id, getIP
from utils.device_posture_check import run_device_posture_check
from utils.device_data import get_device_data
from utils.api_server import API_URL, USER_URL, DEVICE_URL

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Change this to a secure secret key




@app.route('/')
def home():
    return render_template('login.html')




@app.route('/dashboard')
def dashboard():
    device_data = session.get('device_data')
    user_data = session.get('user_data')
    uuid = user_data['uuid']
    device_id = device_data['device_id']
    device_fingerprint = device_data['device_fingerprint']
    device_os = device_data['device_os']
    device_name = device_data['device_name']
    device_type = device_data['device_type']
    hardware_fingerprint = device_data['hardware_fingerprint']

    print(uuid,device_id)
    response = requests.post(
        f'{DEVICE_URL}/isTrusted',
        headers={
            'Authorization': f'Bearer {session["token"]}',
            'Content-Type': 'application/json'
        },
        json={
            'device_id': device_id, 
            'device_fingerprint': device_fingerprint,
            'device_os': device_os,
            'device_name': device_name,
            'device_type': device_type,
            'hardware_fingerprint': hardware_fingerprint
        }
    )
    print(response.json())
    return render_template('landing.html',userlogged=session.get('user_data'),device_data=session.get('device_data'),device_trusted=response.json().get('message')) 





@app.route('/connection', methods=['POST'])
def connection():
    if 'token' not in session:
        return jsonify({"status": "error", "message": "Not authenticated"}), 401

    device_data = session.get('device_data')
    user_data = session.get('user_data')
    
    if not device_data or not user_data:
        return jsonify({"status": "error", "message": "Missing device or user data"}), 400

    # First check if device is trusted
    trust_response = requests.post(
        f'{DEVICE_URL}/isTrusted',
        headers={
            'Authorization': f'Bearer {session["token"]}',
            'Content-Type': 'application/json'
        },
        json=device_data
    )

    if trust_response.status_code != 200:
        return jsonify({"status": "error", "message": "Device not trusted"}), 403

    # Then check if device is authorized for this user
    auth_response = requests.post(
        f'{DEVICE_URL}/isAuthorized',
        headers={
            'Authorization': f'Bearer {session["token"]}',
            'Content-Type': 'application/json'
        },
        json={
            'device_id': device_data['device_id'],
            'uuid': user_data['uuid']
        }
    )

    if auth_response.status_code != 200:
        return jsonify({"status": "error", "message": "Device not authorized for this user"}), 403

    # If both checks pass, run device posture check
    posture_status = run_device_posture_check()
    
    if not posture_status.get('compliant', False):
        return jsonify({
            "status": "error",
            "message": "Device failed posture check",
            "details": posture_status
        }), 403

    # All checks passed, allow connection
    return jsonify({
        "status": "success",
        "message": "Connection authorized",
        "connection_details": {
            "user": user_data['email'],
            "device": device_data['device_name'],
            "ip": getIP()
        }
    })

@app.route('/connectVPN')
def connectVPN():
    return render_template('connection.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return render_template('login.html', error="Email and password are required")

    try:
        # Call the API for authentication
        response = requests.post(
            f'{USER_URL}/login',
            json={'email': email, 'password': password}
        )
        
        data = response.json()
        
        if data.get('status') == 'success':
            # Store token and user data in session
            session['token'] = data['data']['token']
            session['user_data'] = data['data']['user']
            session['device_data'] = get_device_data()
            print(session)
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error=data.get('message', 'Login failed'))
            
    except requests.RequestException as e:
        return render_template('login.html', error="Connection error. Please try again.")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/api/device_posture')
def device_posture():
    if 'token' not in session:
        return jsonify({"error": "Unauthorized"}), 401
        
    posture_status = run_device_posture_check()
    return jsonify(posture_status)

def startApp():
    app.run(debug=False, use_reloader=False)



