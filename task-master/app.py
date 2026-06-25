from flask import Flask,render_template,request,redirect          #import the flask library
from db import db                #import database client
from models import Todo          #import Todo tabe from models file

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"  #All the database data stored in test.db

db.init_app(app)     #initialize app flask application object with db database.

with app.app_context():
    db.create_all()                 #Giving all the context of app to db


@app.route("/", methods=["GET","POST"])
def index():
    # if statement for POST -> adding the todo
    if request.method == "POST":
        task_content = request.form["content"]
        new_task = Todo(content=task_content)
        db.session.add(new_task)
        db.session.commit()
        return redirect("/")
    else:
        #Show tasks
        tasks = Todo.query.all()
        return render_template("index.html",tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):

    task = Todo.query.get_or_404(id)

    if request.method == "POST":

        task.content = request.form["content"]

        db.session.commit()

        return redirect("/")

    else:

        return render_template(
            "update.html",
            task=task
        )


if __name__ == "__main__":
    app.run(debug=True)


