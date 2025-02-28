from flask import Flask, request, jsonify, session, render_template, redirect, url_for


from utils.device_posture_check import run_device_posture_check

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('landing.html')


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

@app.route('/api/device_posture')
def device_posture():
    posture_status = run_device_posture_check()
    return jsonify({"status": posture_status})


def startApp():
    app.run(debug=False, use_reloader=False)

