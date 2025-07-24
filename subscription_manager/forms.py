from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email

class SubscriberForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    plan = SelectField('Subscription Plan', choices=[('Basic', 'Basic'), ('Premium', 'Premium'), ('Pro', 'Pro')])
    submit = SubmitField('Submit')
