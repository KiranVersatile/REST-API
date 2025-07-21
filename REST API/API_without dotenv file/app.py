from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import os

app = Flask(__name__)

# MongoDB setup (change this to local if needed)
client = MongoClient("mongodb://localhost:27017")  # or use MongoDB Atlas URI
db = client["collegeDB"]
students_collection = db["students"]

# Convert ObjectId to string
def fix_id(data):
    data["_id"] = str(data["_id"])
    return data

# Home
@app.route('/')
def home():
    return "🎓 Welcome to Student REST API with MongoDB!"

# GET all students
@app.route('/students', methods=['GET'])
def get_students():
    students = list(students_collection.find())
    return jsonify([fix_id(s) for s in students])

# POST a new student
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    inserted = students_collection.insert_one(data)
    return jsonify({"id": str(inserted.inserted_id)}), 201

# PUT - Update a student
@app.route('/students/<id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()
    result = students_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.modified_count > 0:
        return jsonify({"message": "Student updated"})
    return jsonify({"message": "No changes or student not found"}), 404

# DELETE - Remove a student
@app.route('/students/<id>', methods=['DELETE'])
def delete_student(id):
    result = students_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({"message": "Student deleted"})
    return jsonify({"message": "Student not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
