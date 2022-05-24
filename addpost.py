from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.widgets import  TextArea


class FormularzDodawaniaPosta(FlaskForm):
    title = StringField("Tytuł", validators=[DataRequired()])
    author = StringField("Autor", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget= TextArea())
    #content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField ("Submit")


