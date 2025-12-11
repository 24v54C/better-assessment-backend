from app import create_app, db
from app.models import Task

app = create_app()

with app.app_context():
    title = input("Enter task title: ").strip()
    if title:
        task = Task(title=title)
        db.session.add(task)
        db.session.commit()
        print(f"Task created with ID: {task.id}")
    else:
        print("Task title cannot be empty.")
