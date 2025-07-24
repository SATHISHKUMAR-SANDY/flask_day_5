from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class CourseForm(FlaskForm):
    name = StringField('Course Name', validators=[DataRequired()])
    fee = FloatField('Course Fee', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Add Course')

class StudentForm(FlaskForm):
    name = StringField('Student Name', validators=[DataRequired()])
    submit = SubmitField('Add Student')

class EnrollmentForm(FlaskForm):
    student_id = SelectField('Student', coerce=int, validators=[DataRequired()])
    course_id = SelectField('Course', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Enroll')

class EnrollmentEditForm(FlaskForm):
    student_id = SelectField('Student', coerce=int, validators=[DataRequired()])
    course_id = SelectField('Course', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Update Enrollment')
