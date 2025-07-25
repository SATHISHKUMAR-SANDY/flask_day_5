from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Create Post')

class CommentForm(FlaskForm):
    content = TextAreaField('Add a comment', validators=[DataRequired()])
    submit = SubmitField('Submit Comment')
