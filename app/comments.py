from flask import Blueprint, request, jsonify, abort
from .models import Task, Comment
from . import db

comments_bp = Blueprint('comments', __name__)

def get_task_or_404(task_id):
    task = Task.query.get(task_id)
    if task is None:
        abort(404, description=f"Task {task_id} not found")
    return task

@comments_bp.route('/tasks/<int:task_id>/comments', methods=['POST'])
def add_comment(task_id):
    task = get_task_or_404(task_id)
    data = request.get_json() or {}

    content = data.get('content')
    if not content or not content.strip():
        return jsonify({"error": "content is required"}), 400

    author = data.get('author')

    comment = Comment(
        task_id=task.id,
        content=content.strip(),
        author=(author.strip() if author else None)
    )

    db.session.add(comment)
    db.session.commit()

    return jsonify(comment.to_dict()), 201


@comments_bp.route('/tasks/<int:task_id>/comments', methods=['GET'])
def list_comments(task_id):
    task = get_task_or_404(task_id)
    comments = [c.to_dict() for c in task.comments]
    return jsonify({"task": task.to_dict(), "comments": comments}), 200


@comments_bp.route('/comments/<int:comment_id>', methods=['PUT'])
def edit_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if comment is None:
        abort(404, description=f"Comment {comment_id} not found")

    data = request.get_json() or {}
    content = data.get('content')
    if not content or not content.strip():
        return jsonify({"error": "content is required"}), 400

    author = data.get('author')

    comment.content = content.strip()
    comment.author = author.strip() if author else None

    db.session.commit()

    return jsonify(comment.to_dict()), 200


@comments_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if comment is None:
        abort(404, description=f"Comment {comment_id} not found")

    db.session.delete(comment)
    db.session.commit()

    return jsonify({"message": f"Comment {comment_id} deleted"}), 200
