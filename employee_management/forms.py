from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class EmployeeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=150)])
    position = StringField('Position', validators=[DataRequired(), Length(max=100)])
    department = StringField('Department', validators=[DataRequired(), Length(max=100)])
    salary = FloatField('Salary', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Submit')
