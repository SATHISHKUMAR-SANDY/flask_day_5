from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from models import db, Course, Student, Enrollment
from forms import CourseForm, StudentForm, EnrollmentForm, EnrollmentEditForm

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.before_first_request
def setup():
    db.create_all()

# Courses
@app.route('/courses')
def courses():
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)

@app.route('/courses/add', methods=['GET', 'POST'])
def add_course():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(name=form.name.data.strip(), fee=form.fee.data)
        db.session.add(course)
        db.session.commit()
        flash('Course added successfully!', 'success')
        return redirect(url_for('courses'))
    return render_template('add_course.html', form=form)

# Students
@app.route('/students')
def students():
    students = Student.query.all()
    return render_template('students.html', students=students)

@app.route('/students/add', methods=['GET', 'POST'])
def add_student():
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(name=form.name.data.strip())
        db.session.add(student)
        db.session.commit()
        flash('Student added successfully!', 'success')
        return redirect(url_for('students'))
    return render_template('add_student.html', form=form)

# Enrollments
@app.route('/enrollments')
def enrollments():
    enrollments = Enrollment.query.all()
    return render_template('enrollments.html', enrollments=enrollments)

@app.route('/enrollments/add', methods=['GET', 'POST'])
def add_enrollment():
    form = EnrollmentForm()
    form.student_id.choices = [(s.id, s.name) for s in Student.query.all()]
    form.course_id.choices = [(c.id, c.name) for c in Course.query.all()]
    if form.validate_on_submit():
        existing = Enrollment.query.filter_by(student_id=form.student_id.data, course_id=form.course_id.data).first()
        if existing:
            flash('Student already enrolled in this course.', 'danger')
            return redirect(url_for('enrollments'))
        enrollment = Enrollment(student_id=form.student_id.data, course_id=form.course_id.data)
        db.session.add(enrollment)
        db.session.commit()
        flash('Enrollment added successfully!', 'success')
        return redirect(url_for('enrollments'))
    return render_template('add_enrollment.html', form=form)

@app.route('/enrollments/<int:id>/edit', methods=['GET', 'POST'])
def edit_enrollment(id):
    enrollment = Enrollment.query.get_or_404(id)
    form = EnrollmentEditForm(obj=enrollment)
    form.student_id.choices = [(s.id, s.name) for s in Student.query.all()]
    form.course_id.choices = [(c.id, c.name) for c in Course.query.all()]
    if form.validate_on_submit():
        enrollment.student_id = form.student_id.data
        enrollment.course_id = form.course_id.data
        db.session.commit()
        flash('Enrollment updated successfully!', 'success')
        return redirect(url_for('enrollments'))
    return render_template('edit_enrollment.html', form=form)

@app.route('/enrollments/<int:id>/delete', methods=['POST'])
def delete_enrollment(id):
    enrollment = Enrollment.query.get_or_404(id)
    db.session.delete(enrollment)
    db.session.commit()
    flash('Enrollment deleted successfully!', 'success')
    return redirect(url_for('enrollments'))

if __name__ == '__main__':
    app.run(debug=True)
