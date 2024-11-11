# app.py
from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# MongoDB Configuration
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/taskmanager")
mongo = PyMongo(app)

# Helper function to convert MongoDB ObjectId to string
def parse_json(data):
    return {
        "_id": str(data["_id"]),
        "title": data["title"],
        "description": data.get("description", ""),
        "created_at": data["created_at"],
        "completed": data["completed"]
    }

# Route to serve the frontend
@app.route("/")
def home():
    return render_template("index.html")

# API Routes
@app.route("/tasks", methods=["GET"])
def get_tasks():
    try:
        tasks = mongo.db.tasks.find()
        return jsonify([parse_json(task) for task in tasks])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/tasks", methods=["POST"])
def create_task():
    try:
        data = request.get_json()
        
        if not data or "title" not in data:
            return jsonify({"error": "Title is required"}), 400
            
        new_task = {
            "title": data["title"],
            "description": data.get("description", ""),
            "created_at": datetime.utcnow().isoformat(),
            "completed": False
        }
        
        result = mongo.db.tasks.insert_one(new_task)
        new_task["_id"] = str(result.inserted_id)
        
        return jsonify(parse_json(new_task)), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    try:
        task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
        
        if not task:
            return jsonify({"error": "Task not found"}), 404
            
        return jsonify(parse_json(task))
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    try:
        data = request.get_json()
        
        # Prepare update data
        update_data = {}
        if "title" in data:
            update_data["title"] = data["title"]
        if "description" in data:
            update_data["description"] = data["description"]
        if "completed" in data:
            update_data["completed"] = data["completed"]
            
        # Update the task
        result = mongo.db.tasks.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            return jsonify({"error": "Task not found"}), 404
            
        # Get updated task
        updated_task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
        return jsonify(parse_json(updated_task))
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    try:
        result = mongo.db.tasks.delete_one({"_id": ObjectId(task_id)})
        
        if result.deleted_count == 0:
            return jsonify({"error": "Task not found"}), 404
            
        return "", 204
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)