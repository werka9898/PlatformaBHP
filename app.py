from datetime import datetime
import os
import tempfile

from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import FormularzRejestracji, FormularzLogowania



app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///' + os.path.join(
    tempfile.gettempdir(), 'onboarding.db')#nazwa pliku, który będzie zawierał bazę danych

db = SQLAlchemy(app) #obiekt aplikacji, za pomocą którego prowadzimy interakcje z bazą danych

# model - klasa reprezentująca tabele w bazie danych, db.Model specjalna klasa od SQLAlchemy
class Pracownik(db.Model):
    id = db.Column(db.Integer, primary_key=True) # klucz główny tabeli
    imie = db.Column(db.String(20), unique=True, nullable=False)
    nazwisko = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    haslo = db.Column(db.String(60), unique=True, nullable=False)
    powtorz_haslo = db.Column(db.String(60), nullable=False)
    # posts = db.relationship('Post', backref ='author', lazy=True)

    def __repr(self):
        return f"User('{self.imie}', '{self.nazwisko}', '{self.email}', '{self.haslo}', '{self.powtorz_haslo}')"


posts = [
    {
        'temat': 'BHP',
        'title': 'Szkolenie',
        'content': 'treść',
        'date': '04.05.2022'
    },
    {
        'temat': 'BHP',
        'title': 'Materiały do szkolenia',
        'content': 'treść',
        'date': '04.05.2022'
    }
]



@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/Terminarz")
def about():
    return render_template('about.html', title='terminarz')

@app.route("/Szkolenie")
def szkolenie():
    return render_template('szkolenie.html', title='szkolenie')

@app.route("/Materialy")
def materialy():
    return render_template('materialy.html', title='materialy')

@app.route("/")
@app.route("/Logowanie", methods=['GET','POST'])
def logowanie():
    form = FormularzLogowania()
    if form.validate_on_submit():
        if form.email.data == 'test@gmail.com' and form.password.data == 'aa':
            flash(f'Zalogowano!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Logowanie niepoprawne', 'danger')
    return render_template('login.html', title='logowanie', form=form)


@app.route("/Rejestracja", methods=['GET','POST'])
def rejestracja():
    form = FormularzRejestracji()
    if form.validate_on_submit():
        flash(f'Rejestracja pomyślna!', 'success')
        return redirect(url_for('logowanie'))
    return render_template('rejestracja.html', title='rejestracja', form=form)


@app.route("/Logout")
def logout():
    return render_template('wyloguj.html', title='wyloguj')

if __name__ == '__main__':
    app.run(debug=True)