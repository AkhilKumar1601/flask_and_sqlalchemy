from db import db
from flask import Flask,render_template
from models import Todo

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db.init_app(app)


with app.app_context():
  new_task = Todo(content="Learn Flask")
  db.session.add(new_task)
  db.session.commit()

