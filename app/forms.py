from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, PasswordField, SelectField, ValidationError, FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email
import config.default as config

class EmailForm(FlaskForm):
    email_name = StringField('EmailName', validators=[DataRequired()])
    email = EmailField('Email', validators=[Email()])

class UserLoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])

class UserCreateForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email()])

    nickname = StringField('nickname', validators=[DataRequired(), Length(min=3, max=15)])
    password1 = PasswordField('password', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다.')
    ])
    password2 = PasswordField('confirm password', validators=[DataRequired()])

    student_name = StringField('name', validators=[DataRequired(), Length(min=3, max=25)])
    student_number = StringField('student number', validators=[DataRequired()])

class ModelSubmitForm(FlaskForm):
    teamname = StringField('teamname', validators=[DataRequired(), Length(min=2, max=10)])
    method = StringField('method_name', validators=[DataRequired(), Length(min=2, max=25)])
    code = StringField('code_url', validators=[])

    task = SelectField('task', choices=[(i,i) for i in ['None']+config.TASKS])

    def validate_task(self, field):
        if field.data == 'None':
            raise ValidationError('Please select Task filed.')
