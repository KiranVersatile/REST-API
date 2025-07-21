# pip install flask pymongo python-dotenv flask-jwt-extended bcrypt dnspython

from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os
import bcrypt

# Load .env
load_dotenv()

# Flask app setup
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET")

# JWT
jwt = JWTManager(app)

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
STUDENT_COLLECTION = os.getenv("STUDENT_COLLECTION")
USER_COLLECTION = os.getenv("USER_COLLECTION")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
students = db[STUDENT_COLLECTION]
users = db[USER_COLLECTION]

# Helper to convert ObjectId


def fix_id(data):
    data["_id"] = str(data["_id"])
    return data

# 🔐 Register (signup)


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if users.find_one({"email": data['email']}):
        return jsonify({"message": "User already exists"}), 409

    hashed = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    users.insert_one({
        "email": data['email'],
        "password": hashed
    })
    return jsonify({"message": "User registered successfully"}), 201

# 🔐 Login


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = users.find_one({"email": data['email']})
    if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
        return jsonify({"message": "Invalid email or password"}), 401

    token = create_access_token(identity=user['email'])
    return jsonify({"access_token": token})

# ✅ Protected route: Get all students


@app.route('/students', methods=['GET'])
@jwt_required()
def get_students():
    all_students = list(students.find())
    return jsonify([fix_id(s) for s in all_students])

# ✅ Protected: Add student


@app.route('/students', methods=['POST'])
@jwt_required()
def add_student():
    data = request.get_json()
    result = students.insert_one(data)
    return jsonify({"message": "Student added", "id": str(result.inserted_id)}), 201

# ✅ Protected: Update student


@app.route('/students/<id>', methods=['PUT'])
@jwt_required()
def update_student(id):
    data = request.get_json()
    result = students.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.modified_count:
        return jsonify({"message": "Student updated"})
    return jsonify({"message": "Not found or no changes"}), 404

# ✅ Protected: Delete student


@app.route('/students/<id>', methods=['DELETE'])
@jwt_required()
def delete_student(id):
    result = students.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        return jsonify({"message": "Student deleted"})
    return jsonify({"message": "Student not found"}), 404

# Home


@app.route('/')
def home():
    return "🎓 JWT-Secured Student API"


if __name__ == '__main__':
    app.run(debug=True)
