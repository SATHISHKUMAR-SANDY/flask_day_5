from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Regexp, Length

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[
        DataRequired(),
        Regexp(r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address')
    submit = SubmitField('Submit')
