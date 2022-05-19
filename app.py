from flask import Flask, render_template, url_for, flash, redirect
from forms import FormularzRejestracji, FormularzLogowania



app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'



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