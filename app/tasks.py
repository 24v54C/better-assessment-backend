from flask import Blueprint, request, jsonify, abort
from app import db
from app.models import Task

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route("/tasks", methods=["GET"])
def list_tasks():
    tasks = Task.query.all()
    return jsonify([t.to_dict() for t in tasks]), 200


@tasks_bp.route("/tasks", methods=["POST"])
def create_task_route():
    data = request.get_json() or {}
    title = data.get("title")

    if not title or not title.strip():
        return jsonify({"error": "title is required"}), 400

    task = Task(title=title.strip())
    db.session.add(task)
    db.session.commit()

    return jsonify(task.to_dict()), 201


@tasks_bp.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        abort(404, description=f"Task {task_id} not found")
    return jsonify(task.to_dict()), 200
