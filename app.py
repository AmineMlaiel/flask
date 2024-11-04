from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL database connection details
db_config = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': '',  # Replace with your MySQL password
    'database': 'mydb'
}

# Establish database connection
def db_connect():
    return mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )

# Route for login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Expecting JSON data in request body
    
    username = data.get('username')
    password = data.get('password')
    #return jsonify({'error': 'Username and password are required!'}), 200
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required!'}), 400
    
    try:
        # Connect to the database
        connection = db_connect()
        cursor = connection.cursor()

        # Query to check username and password
        query = "SELECT * FROM users WHERE login = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        # Check if user exists
        if user:
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        connection.close()

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
