from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    consumer_key = StringField(label="Consumer Key", validators=[DataRequired()])
    consumer_secret = StringField(label="Consumer Secret", validators=[DataRequired()])
    bearer_token = StringField(label="Bearer Token", validators=[DataRequired()])
    access_token = StringField(label="Access Token", validators=[DataRequired()])
    access_token_secret = StringField(label="Access Token Secret", validators=[DataRequired()])
    submit = SubmitField(label="Login")
