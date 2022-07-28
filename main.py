


from flask import Flask, render_template,redirect,url_for,request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
#
# TEMPLATE_DIR = os.path.abspath('../templates')
# STATIC_DIR = os.path.abspath('../static')
app = Flask(__name__)


app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///to_do.db"
db = SQLAlchemy(app)
Base = declarative_base()
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(250), unique=True, nullable=False)
class Done(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    done = db.Column(db.String(250), unique=True, nullable=False)
db.create_all()
class TaskForm(FlaskForm):
    task = StringField('Task: ', validators=[DataRequired()])
    submit = SubmitField('Submit')
db.session.commit()
# all Flask routes below

@app.route('/')
def tasks():

    task =Task.query.all()
    done=Done.query.all()
    return render_template('index.html', tasks=task,done = done)


@app.route('/add',methods=["POST", "GET"])
def add():

    task_form=TaskForm()
    if task_form.validate_on_submit():
        task = Task(task=task_form.task.data)
        db.session.add(task)
        db.session.commit()

        return redirect(url_for('tasks'))
    return render_template('add.html',form=task_form)


@app.route('/delete/<num>',methods=["POST", "GET"])
def delete(num):
    id = num
    task_delete= Task.query.get(id)
    db.session.delete(task_delete)
    db.session.commit()
    return redirect(url_for('tasks'))

@app.route('/add/<num>',methods=["POST", "GET"])
def done(num):
    id = num
    task_done = Task.query.get(id)

    task = Done(done=task_done.task)
    db.session.add(task)
    db.session.commit()
    task_delete = Task.query.get(id)
    db.session.delete(task_delete)
    db.session.commit()
    return redirect(url_for('tasks'))





@app.route('/delete_task/<num>',methods=["POST", "GET"])
def delete_done(num):
    id = num
    task_deleted= Done.query.get(id)
    db.session.delete(task_deleted)
    db.session.commit()
    return redirect(url_for('tasks'))

if __name__ == '__main__':
    app.run(debug=True)
