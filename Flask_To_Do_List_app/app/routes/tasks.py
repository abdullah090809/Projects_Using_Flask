from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models.Tasks import Task
from .forms import TaskForm

task_bp=Blueprint('tasks',__name__)

@task_bp.route('/')
def view_task():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    tasks=Task.query.all()
    return render_template("tasks.html",tasks=tasks)

@task_bp.route("/add",methods=["GET", "POST"])
def add_task():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    form=TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data, status=form.status.data, user_id=session['user_id'])
        db.session.add(task)
        db.session.commit()
        flash('Task added!', 'success')
        return redirect(url_for('tasks.view_task'))
    return render_template("add_task.html", form=form)

@task_bp.route("/delete/<int:task_id>",methods=["POST"])
def delete_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted!', 'success')
    return redirect(url_for('tasks.view_task'))

@task_bp.route("/clear",methods=["POST"])
def clear_tasks():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    Task.query.filter_by(user_id=session['user_id']).delete()
    db.session.commit()
    flash('All tasks cleared!', 'success')
    return redirect(url_for('tasks.view_task'))