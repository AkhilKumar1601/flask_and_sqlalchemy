from flask import Flask,request
from db import db
from models import Todo

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///task.db"

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/tasks")
def get_tasks():
    tasks = Todo.query.all()
    result = [task.to_dict() for task in tasks]

    return {
            "tasks" : result
    }

@app.route("/tasks", methods=["POST"])
def create_tasks():
    data = request.get_json()
    new_task = Todo(content=data["content"])
    db.session.add(new_task)
    db.session.commit()

    return {
        "message" : "Task created successfully"
    },201

@app.route("/tasks/<int:id>")
def get_task(id):
    task = Todo.query.get_or_404(id)
    return task.to_dict()

@app.route("/tasks/<int:id>", methods=["PATCH"])
def update_task(id):
    task = Todo.query.get_or_404(id)
    data = request.get_json()
    task.content = data["content"]
    db.session.commit()

    return task.to_dict()

@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Todo.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()

    return {
        "message" : "Task deleted successfully"
    }
    

if __name__ == "__main__":
    app.run(debug=True)
