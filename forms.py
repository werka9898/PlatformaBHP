from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class FormularzRejestracji(FlaskForm):
    imie = StringField('Wprowadź imię',
                       validators=[DataRequired(), Length(min=1, max=20)])
    nazwisko = StringField('Wprowadź nazwisko',
                       validators=[DataRequired(), Length(min=1, max=20)])
    email = StringField('Wprowadź adres e-mail',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Wprowadź hasło',
                        validators=[DataRequired()])
    repeat_password = PasswordField('Potwierdź haslo',
                        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Zarejestruj się')


class FormularzLogowania(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Haslo',
                        validators=[DataRequired()])
    submit = SubmitField('Zaloguj się')