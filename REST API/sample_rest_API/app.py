from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Environment variables
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# Flask app
app = Flask(__name__)

# MongoDB setup
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Helper to convert ObjectId


def fix_id(data):
    data["_id"] = str(data["_id"])
    return data

# Home route


@app.route('/')
def home():
    return "🎓 Welcome to the MongoDB Student API!"

# GET all students


@app.route('/students', methods=['GET'])
def get_students():
    students = list(collection.find())
    return jsonify([fix_id(s) for s in students])

# POST a new student


@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    result = collection.insert_one(data)
    return jsonify({"message": "Student added", "id": str(result.inserted_id)}), 201

# PUT update student by ID


@app.route('/students/<id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()
    result = collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.modified_count:
        return jsonify({"message": "Student updated successfully"})
    return jsonify({"message": "Student not found or no changes made"}), 404

# DELETE student by ID


@app.route('/students/<id>', methods=['DELETE'])
def delete_student(id):
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        return jsonify({"message": "Student deleted successfully"})
    return jsonify({"message": "Student not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
