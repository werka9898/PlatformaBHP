from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from forms import FormularzRejestracji, FormularzLogowania
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user





app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baza_pracownikow.db' #nazwa pliku, który będzie zawierał bazę danych

db = SQLAlchemy(app) #obiekt aplikacji, za pomocą którego prowadzimy interakcje z bazą danych
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category= 'info'


# model - klasa reprezentująca tabele w bazie danych, db.Model specjalna klasa od SQLAlchemy
class Uzytkownicy(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # klucz główny tabeli
    imie = db.Column(db.String(20))
    nazwisko = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True)
    haslo = db.Column(db.String(60))
    powtorz_haslo = db.Column(db.String(60))

    def __init__(self, imie, nazwisko, email, haslo, powtorz_haslo):
        self.imie = imie
        self.nazwisko = nazwisko
        self.email = email
        self.haslo = haslo
        self.powtorz_haslo = powtorz_haslo

    def __repr__(self):
        return f"Uzytkownicy('{self.imie}', '{self.nazwisko}', '{self.email}', '{self.haslo}', '{self.powtorz_haslo}')"
    
    
    def save(self):
        db.session.add(self)
        db.session.commit()



@login_manager.user_loader
def load_user(user_id):
    return Uzytkownicy.query.get(int(user_id))



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

@app.route("/", methods=['GET','POST'])
def logowanie():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = FormularzLogowania()
    if form.validate_on_submit():
        user = Uzytkownicy.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.haslo, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Logowanie niepoprawne. Wpisano błędy email lub hasło', 'danger')
    return render_template('login.html', title='logowanie', form=form)




@app.route("/Rejestracja", methods=['GET','POST'])
def rejestracja():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = FormularzRejestracji()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        hashed_password2 = bcrypt.generate_password_hash(form.repeat_password.data).decode('utf-8')
        nowy_uzytkownik = Uzytkownicy(imie=form.imie.data, nazwisko=form.nazwisko.data, email=form.email.data, haslo=hashed_password, powtorz_haslo=hashed_password2)
        db.session.add(nowy_uzytkownik)
        db.session.commit()
        flash(f'Rejestracja pomyślna!', 'success')
        return redirect(url_for('logowanie'))
    return render_template('rejestracja.html', title='rejestracja', form=form)



@app.route("/Logout")
def logout():
    logout_user()
    return render_template('wyloguj.html', title='wyloguj')

if __name__ == '__main__':
    app.run(debug=True)
