from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import json

app = Flask(__name__, template_folder='templates')

# Function to initialize database
def create_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Route to display the form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission and insert data
@app.route('/insert', methods=['POST'])
def insert_data():
    name = request.form['name']
    email = request.form['email']

    if name.strip() != "" and email.strip() != "":
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
        conn.commit()
        conn.close()

    return redirect(url_for('index'))  # Redirect to the form after insertion or if fields were empty

# Route to handle JSON file upload and insert data
@app.route('/upload_json', methods=['POST'])
def upload_json():
    file = request.files['file']
    if file.filename.endswith('.json'):
        data = json.load(file)

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        for entry in data:
            name = entry.get('name')
            email = entry.get('email')

            if name and email:
                cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))

        conn.commit()
        conn.close()

    return redirect(url_for('index'))  # Redirect to the form after processing the JSON file

# Route to fetch data from the database
@app.route('/get_data')
def get_data():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    data = cursor.fetchall()
    conn.close()

    # Prepare data in a format suitable for JSON response
    response_data = []
    for row in data:
        response_data.append({
            'id': row[0],
            'name': row[1],
            'email': row[2]
        })

    return jsonify(response_data)  # Return data as JSON

if __name__ == '__main__':
    create_table()  # Ensure table exists before running the app
    app.run(debug=True,port= 2223)
