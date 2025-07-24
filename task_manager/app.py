from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from models import db, Task
from forms import TaskForm
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    tasks = Task.query.order_by(Task.due_date).all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(
            title=form.title.data,
            due_date=form.due_date.data,
            is_done=form.is_done.data or False
        )
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully!", "success")
        return redirect(url_for('index'))
    return render_template('task_form.html', form=form, title="Add Task")

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.due_date = form.due_date.data
        task.is_done = form.is_done.data or False
        db.session.commit()
        flash("Task updated successfully!", "info")
        return redirect(url_for('index'))
    return render_template('task_form.html', form=form, title="Edit Task")

@app.route('/toggle/<int:task_id>')
def toggle_done(task_id):
    task = Task.query.get_or_404(task_id)
    task.is_done = not task.is_done
    db.session.commit()
    flash(f"Task marked {'done' if task.is_done else 'undone'}!", "info")
    return redirect(url_for('index'))

@app.route('/delete_completed')
def delete_completed():
    completed_tasks = Task.query.filter_by(is_done=True).all()
    for task in completed_tasks:
        db.session.delete(task)
    db.session.commit()
    flash("All completed tasks deleted.", "danger")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
