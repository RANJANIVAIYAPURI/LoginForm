from flask import Flask, render_template, request, jsonify, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key' 


#user credentials for demo purposes
users = {
    "admin": "password123",
    "user1": "mypassword",
    "mithra": "mithra#123"
}

@app.route('/')
def index():
    # if already logged in, redirect to dashboard
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # check if user exists and password matches
    if username in users and users[username] == password:
        session['username'] = username  # store username in session
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "Invalid username or password"})

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))  # if not logged in, redirect to login page
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # remove username from session
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
