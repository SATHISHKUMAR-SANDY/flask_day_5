from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class VoteForm(FlaskForm):
    voter_name = StringField('Your Name', validators=[DataRequired()])
    candidate = SelectField('Select Candidate', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Cast Vote')
