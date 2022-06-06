from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from forms import FormularzRejestracji, FormularzLogowania
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from addpost import FormularzDodawaniaPosta
from flask_ckeditor import CKEditor
from quiz import PopQuiz

app = Flask(__name__)
ckeditor = CKEditor(app)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pracownicy.db' #nazwa pliku, który będzie zawierał bazę danych
app.config['SQLALCHEMY_BINDS'] = {'db2': 'sqlite:///materialy.db'}
db = SQLAlchemy(app) #obiekt aplikacji, za pomocą którego prowadzimy interakcje z bazą danych
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category= 'info'


# model - klasa reprezentująca tabele w bazie danych, db.Model specjalna klasa od SQLAlchemy
class Uzytkownicy(db.Model, UserMixin):
    __tablename__ = 'Uzytkownicy'
    id = db.Column(db.Integer, primary_key=True) # klucz główny tabeli
    imie = db.Column(db.String(20))
    nazwisko = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True)
    haslo = db.Column(db.String(60))
    powtorz_haslo = db.Column(db.String(60))
    wynik = db.Column(db.Integer)


    def __init__(self, imie, nazwisko, email, haslo, powtorz_haslo, wynik):
        self.imie = imie
        self.nazwisko = nazwisko
        self.email = email
        self.haslo = haslo
        self.powtorz_haslo = powtorz_haslo
        self.wynik = wynik

    def __repr__(self):
        return f"Uzytkownicy('{self.imie}', '{self.nazwisko}', '{self.email}', '{self.haslo}', '{self.powtorz_haslo}', '{self.wynik}')"






db.create_all()
db.session.commit()

class Posts(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = 'Posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
    slug = db.Column(db.String(255))
    content = db.Column(db.String(255))

    def __init__(self, title, content, author, slug):
            self.title = title
            self.author = author
            self.slug = slug
            self.content = content

    def __repr__(self):
            return f"Posts('{self.title}', '{self.author}', '{self.slug}','{self.content}')"

    db.create_all(bind='db2')

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
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        hashed_password2 = bcrypt.generate_password_hash(form.repeat_password.data)
        nowy_uzytkownik = Uzytkownicy(imie=form.imie.data, nazwisko=form.nazwisko.data, email=form.email.data, haslo=hashed_password, powtorz_haslo=hashed_password2, wynik = 0)
        db.session.add(nowy_uzytkownik)
        db.session.commit()
        flash(f'Rejestracja pomyślna!', 'success')
        return redirect(url_for('logowanie'))
    return render_template('rejestracja.html', title='rejestracja', form=form)


@app.route("/Logout")
def logout():
    logout_user()
    return render_template('wyloguj.html', title='wyloguj')


@app.route("/Dodaj_post", methods=['GET','POST'])
def dodajpost():
        form = FormularzDodawaniaPosta()
        if form.validate_on_submit():
            #przekazujemy tytuł, treść itp do zmiennej post
            post = Posts(title=form.title.data, content=form.content.data, author=form.author.data, slug = form.slug.data)

            #Czyścimy okienka
            form.title.data = ''
            form.author.data = ''
            form.slug.data = ''
            form.content.data = ''

            #dodaj post do bazy danych
            db.session.add(post)
            db.session.commit()
            flash(f'Post został dodany!', 'success')

        # przejdź do tej samej strony
        return render_template('dodaj_post.html', form= form)
#     return render_template("dodaj_post.html", form1= form1)


@app.route("/Materialy", methods=['GET','POST'] )
def materialy():
    #wez posty z bazy danych
    #posts = Posts.query.order_by(Posts.title)
    posts = Posts.query.all()
    return render_template('materialy.html', posts = posts)


@app.route("/Quiz", methods=['GET', 'POST'])
def quiz():
  form = PopQuiz()
  if form.on_submit():
      return redirect(url_for('wyniki'))
  return render_template('quiz.html', form=form)

@app.route('/Wyniki')
def wyniki():
 return render_template('wyniki.html')

if __name__ == '__main__':

    app.run(debug=True)

