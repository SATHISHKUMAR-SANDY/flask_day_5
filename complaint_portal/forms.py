from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class ComplaintForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=150)])
    message = TextAreaField('Complaint Message', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Submit Complaint')
