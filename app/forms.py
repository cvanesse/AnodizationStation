from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class CycleUploadForm(FlaskForm):
    cyclefile = FileField('.cycle File', validators=[FileRequired()])
    submit = SubmitField('Upload')


class LogDownloadForm(FlaskForm):
    date = DateField('Sample Creation Date', validators=[DataRequired()])
    name = StringField('Sample Name', validators=[DataRequired()])
    submit = SubmitField('Download')
