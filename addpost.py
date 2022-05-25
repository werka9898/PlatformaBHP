from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.widgets import  TextArea
from flask_ckeditor import CKEditorField


class FormularzDodawaniaPosta(FlaskForm):
    title = StringField("Tytuł", validators=[DataRequired()])
    author = StringField("Autor", validators=[DataRequired()])
    slug = StringField("Słowa kluczowe", validators=[DataRequired()])
    #content = StringField("Treść", validators=[DataRequired()], widget= TextArea())
    content = CKEditorField("Treść", validators=[DataRequired()], widget= TextArea())
    #content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField ("Zapisz")


