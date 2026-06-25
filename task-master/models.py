from db import db
from datetime import datetime

class Todo(db.Model):               #Initialize a Database Table.
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(200),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.now)

    def __repr__(self):               #if after object creation, user prints the object then it shows what should be shown.
        return f"<Task {self.id}>"
