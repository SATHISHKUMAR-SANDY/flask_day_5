from flask import Flask, render_template, redirect, url_for, flash
from config import Config
from models import db, Student
from forms import StudentForm

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    students = Student.query.order_by(Student.id).all()
    return render_template('index.html', students=students)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(
            name=form.name.data,
            roll_no=form.roll_no.data,
            email=form.email.data,
            age=form.age.data
        )
        db.session.add(student)
        db.session.commit()
        flash("Student registered successfully!", "success")
        return redirect(url_for('index'))
    return render_template('student_form.html', form=form, is_edit=False)

@app.route('/edit/<int:student_id>', methods=['GET', 'POST'])
def edit(student_id):
    student = Student.query.get_or_404(student_id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        student.name = form.name.data
        student.roll_no = form.roll_no.data
        student.email = form.email.data
        student.age = form.age.data
        db.session.commit()
        flash("Student updated!", "info")
        return redirect(url_for('index'))
    return render_template('student_form.html', form=form, is_edit=True)

@app.route('/delete/<int:student_id>')
def delete(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash("Student deleted.", "danger")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
