from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

import numpy as np

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.app_context().push()
db = SQLAlchemy(app)

class task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    fltnum = db.Column(db.String(50))
    empname = db.Column(db.String(50))
    taskdesc = db.Column(db.String(250))
    priority = db.Column(db.String(50))


@app.route("/")
def main():
    tasks = task.query.all()
    return render_template('tracker.html', tasks = tasks)

@app.route("/new")
def createNew():
    title = request.args.get('title')
    fltnum = request.args.get('fleetNo')
    empname = request.args.get('employee')
    taskdesc = request.args.get('description')
    priority = request.args.get('priority')

    newtask = task()
    newtask.title = title
    newtask.fltnum = fltnum
    newtask.empname = empname
    newtask.taskdesc = taskdesc
    newtask.priority = priority

    db.session.add(newtask)
    db.session.commit()
    
    return redirect(url_for('main'))

@app.route("/del")
def deleteCard():
    task_id = request.args.get('id')
    del_task = task.query.filter_by(id = task_id).first()
    db.session.delete(del_task)
    db.session.commit()
    return redirect(url_for('main'))

@app.route("/complete")
def completeTask():
    task_id = request.args.get('id')
    cmp_task = task.query.filter_by(id = task_id).first()
    cmp_task.priority = 'Completed'
    db.session.commit()
    return redirect(url_for('main'))

@app.route('/completedtasks')
def completedTasks():
    tasks = task.query.all()
    return render_template('completed.html', tasks = tasks)



with app.app_context():
    db.create_all()



if __name__ == '__main__':
    app.run(debug=True)