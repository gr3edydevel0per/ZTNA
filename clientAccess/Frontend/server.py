from flask import Flask, request, jsonify, session, render_template, redirect, url_for


from utils.database import get_connection


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

if __name__ == '__main__':
    app.run(debug=True)
