from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    fee = db.Column(db.Float, nullable=False)
    enrollments = db.relationship('Enrollment', backref='course', cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f'<Course {self.name}>'

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    enrollments = db.relationship('Enrollment', backref='student', cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f'<Student {self.name}>'

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

    def __repr__(self):
        return f'<Enrollment Student:{self.student_id} Course:{self.course_id}>'
