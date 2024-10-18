from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure key

app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_PORT"] = 9090
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "flask"

mysql = MySQL(app)


@app.route('/api/test')
def api_test():
    conn = mysql.connection.cursor()
    conn.execute("SELECT * FROM users")
    data = conn.fetchall()
    conn.close()
    return jsonify(data)
    
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
    
    conn = mysql.connection.cursor()
    conn.execute("SELECT * FROM users WHERE username = %s and password= %s", (username, password))
    usr = conn.fetchall()
    conn.close()
    
    if len(usr) == 0:
        return jsonify({"success": False, "message": "Invalid username or password"})
    else:
        username = usr[0][1]
        session['username'] = username
        return jsonify({"success": True})
    

    # # Check if the user exists and the password matches
    # if username in users and users[username] == password:
    #     session['username'] = username  # Store username in session
    #     return jsonify({"success": True})
    # else:
    #     return jsonify({"success": False, "message": "Invalid username or password"})

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        # conn = mysql.connection.cursor()
        # conn.execute("SELECT * FROM users WHERE username = %s", (username))
        # usr = conn.fetchall()
        # conn.close()
        
        # if len(usr) > 0:
        #     return jsonify({"success": False, "message": "Username already exists"})
        
        if username and password:
            conn = mysql.connection.cursor()
            conn.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            mysql.connection.commit()
            conn.close()
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
