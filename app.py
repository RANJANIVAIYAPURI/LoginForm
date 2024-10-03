from flask import Flask, render_template, request, jsonify, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure key

# User credentials stored for demo purposes (in-memory storage)
users = {
    "admin": "password123",
    "user1": "mypassword",
    "mithra": "mithra#123"
}

@app.route('/')
def index():
    # If user is already logged in, redirect to the dashboard
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if the user exists and the password matches
    if username in users and users[username] == password:
        session['username'] = username  # Store username in session
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "Invalid username or password"})

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Check if username already exists
        if username in users:
            return jsonify({"success": False, "message": "Username already exists"})
        
        # Add the new user
        users[username] = password
        return jsonify({"success": True})
    
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if 'username' not in session:
        return redirect(url_for('index'))  # Redirect to login if not logged in
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
