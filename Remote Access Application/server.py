from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from utils.essentials import get_current_machine_id,getIP

from utils.device_posture_check import run_device_posture_check
from utils.device_data import get_device_data


"""

To do : on login get some details like uuid and device data 



"""


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('landing.html',userlogged = {"name" :"gr3edydevel0per","public_ip": getIP(),"device_id": get_current_machine_id()})


@app.route('/connection')
def connection():
    return render_template('connection.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username and password:
        return redirect(url_for('dashboard'))  # Redirect to dashboard on success
    else:
        return render_template('login.html', error="Invalid username/email or password")



def check_deviceIsAuthorized():
    device_Data = get_device_data() // currentDevice 
    # Request to server to check if device is authorized
    

@app.route('/api/device_posture')
def device_posture():
    posture_status = run_device_posture_check()
    print(posture_status)
    return jsonify( posture_status)


def startApp():
    app.run(debug=False, use_reloader=False)
