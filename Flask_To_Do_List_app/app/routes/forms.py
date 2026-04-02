from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegisterForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=8)])
    confirm=PasswordField('Confirm Passowrd',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    status = SelectField('Status', default='pending', choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Done')
    ])
    submit = SubmitField('Add Task')
