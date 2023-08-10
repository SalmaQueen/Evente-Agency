from flask import Flask, request, jsonify
from pymongo import MongoClient, errors
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS  # Import the CORS module

app = Flask(__name__)

CORS(app)

# Replace this with your MongoDB Atlas connection string
mongo_uri = 'mongodb+srv://salma123:salma123@cluster0.a7vyz7x.mongodb.net/'

client = MongoClient(mongo_uri)
db = client['your_database_name']  # Replace with your actual database name
users_collection = db['users']  # Replace 'users' with your collection name

@app.route('/signup', methods=['POST'])
def sign_up():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Invalid data'}), 400

    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    role = data.get('role')
    phone_number = data.get('phone_number')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    hashed_password = generate_password_hash(password, method='sha256')

    new_user = {
        'email': email,
        'password': hashed_password,
        'first_name': first_name,
        'last_name': last_name,
        'role': role,
        'phone_number': phone_number
    }

    try:
        users_collection.insert_one(new_user)
        return jsonify({'message': 'User registered successfully'}), 201
    except errors.DuplicateKeyError:
        return jsonify({'error': 'Email already registered'}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Invalid data'}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = users_collection.find_one({'email': email})

    if user and check_password_hash(user['password'], password):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True)
