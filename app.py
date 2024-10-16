from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize MongoDB connection
client = MongoClient('mongodb://localhost:27017/')

def get_today_db():
    """
    Get the database based on today's date.
    This ensures we store user data in a different database each day.
    """
    today_date = datetime.now().strftime("%Y_%m_%d")
    return client[today_date]  # Returns today's database


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

    # Use today's date to access the correct database
    db = get_today_db()
    users_collection = db['users']

    # Find the user in the MongoDB database
    user = users_collection.find_one({'username': username})

    # Check if user exists and if the plain password matches
    if user and user['password'] == password:  # Plain-text password comparison
        session['username'] = username  # Store username in session
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "Invalid username or password"})


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')  # Storing plain text password
        email = data.get('email')
        phone = data.get('phone')

        # Use today's date to access the correct database
        db = get_today_db()
        users_collection = db['users']

        # Check if username already exists in MongoDB
        if users_collection.find_one({'username': username}):
            return jsonify({"success": False, "message": "Username already exists"})

        # Insert new user with plain password into MongoDB
        user_data = {
            'username': username,
            'password': password,  # Plain text password (NOT RECOMMENDED in production)
            'email': email,
            'phone': phone
        }
        users_collection.insert_one(user_data)
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
