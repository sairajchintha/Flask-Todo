from flask import Flask , render_template , request, redirect, url_for , session
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Todo(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100))
    duedate=db.Column(db.String(10))
    complete=db.Column(db.Boolean)

@app.route('/')
def index():
    #show all to do's
    todo_list=Todo.query.all()
    return render_template('base.html', todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add():
    title=request.form.get("title")
    duedate=request.form.get("duedate")
    new_todo=Todo(title=title,duedate=duedate, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete= not todo.complete
    todo.duedate= "N.A"
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))





@app.route('/about')
def about():
    return "About Awaited"


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True,host='0.0.0.0',port='5000')
