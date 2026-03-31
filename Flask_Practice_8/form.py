from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class RegistrationForm(FlaskForm):
    name=StringField("Full Name", validators=[DataRequired()])
    email=StringField("Email",validators=[DataRequired(),Email()])
    password=PasswordField("Password",validators=[DataRequired(),Length(min=8)])
    submit=SubmitField("Register")