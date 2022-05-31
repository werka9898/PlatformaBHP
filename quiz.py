from flask_wtf import FlaskForm as Form
from wtforms import RadioField
from wtforms.validators import ValidationError
from random import randrange


class CorrectAnswer(object):
    def __init__(self, answer):
        self.answer = answer

    def __call__(self, form, field):
        message = 'Incorrect answer.'

        if field.data != self.answer:
            raise ValidationError(message)

class PopQuiz(Form):
    class Meta:
        csrf = False
    q1 = RadioField(
        "Czy to jest szkolenie z BHP?",
        choices=[('opcja1', 'Tak'), ('opcja2', 'Nie')],
        validators=[CorrectAnswer('opcja1')]
        )
    # q2 = RadioField(
    #     "Czy to jest szkolenie z ONBOARDINGU?",
    #     choices=[('opcja1', 'Tak'), ('opcja2', 'Nie')],
    #     validators=[CorrectAnswer('opcja2')]
    # )