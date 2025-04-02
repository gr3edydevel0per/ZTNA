from flask import render_template, request, session, jsonify, redirect, url_for, Flask
from core.utils.api_helper import api_request
from core.utils.device_posture import DevicePostureChecker
from core.utils.device_data import get_device_data
from core.utils.vpn_manager import VPNManager
from core.utils.api_server import API_URL, USER_URL, DEVICE_URL
import os

app = Flask(__name__)
app.secret_key = "YOUR-SECRET-LEY"

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_data' not in session or 'device_data' not in session:
        return redirect(url_for('home'))

    device_data = session.get('device_data')

    response = api_request(
        f'{DEVICE_URL}/isTrusted',
        json={
            'device_id': device_data.get('device_id'),
            'device_fingerprint': device_data.get('device_fingerprint'),
            'device_os': device_data.get('device_os'),
            'device_name': device_data.get('device_name'),
            'device_type': device_data.get('device_type'),
            'hardware_fingerprint': device_data.get('hardware_fingerprint')
        },
        headers={'Authorization': f'Bearer {session["token"]}', 'Content-Type': 'application/json'}
    )

    return render_template(
        'landing.html', 
        userlogged=session.get('user_data'),
        device_data=session.get('device_data'),
        device_trusted=response.get('message', 'Device trust check failed')
    )

@app.route('/vpn')
def vpn():
    if 'token' not in session:
        return redirect(url_for('home'))

    vpn_manager = VPNManager(uuid=session.get('user_data')['uuid'], session_token=session)
    vpn_result = vpn_manager.start_vpn()
    private_ip = vpn_manager.get_private_ip()

    return render_template(
        'vpn.html', 
        success='success', 
        userlogged=session.get('user_data'), 
        device_data=session.get('device_data'), 
        device_trusted="Device is trusted", 
        private_ip=private_ip
    )

@app.route('/connectVPN')
def connect_vpn():
    return render_template('connection.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return render_template('login.html', error="Email and password are required")

    response = api_request(f'{USER_URL}/login', method='POST', json={'email': email, 'password': password})

    if response.get('status') == 'success':
        session['token'] = response['data']['token']
        session['user_data'] = response['data']['user']
        session['device_data'] = get_device_data()
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', error=response.get('message', 'Login failed'))

@app.route('/logout')
def logout():
    if 'user_data' in session:
        vpn_manager = VPNManager(uuid=session.get('user_data')['uuid'], session_token=session)
        vpn_manager.stop_vpn()
    session.clear()
    return jsonify({"status": "success", "redirect": url_for('home')})

@app.route('/api/device_posture')
def device_posture():
    if 'token' not in session:
        return jsonify({"error": "Unauthorized"}), 401
        
    health_checker = DevicePostureChecker()
    posture_data = health_checker.run_device_posture_check()
    return jsonify(posture_data)

@app.route('/api/window_state')
def window_state():
    return jsonify({
        "is_minimized": False,
        "is_visible": True
    })

def start_app():
    app.run(host="127.0.0.1",debug=False, use_reloader=False)
