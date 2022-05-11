from flask import Flask, render_template, url_for
app = Flask(__name__)

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
@app.route("/Logowanie")
def logowanie():
    return render_template('login.html', title='logowanie')


@app.route("/Rejestracja")
def rejestracja():
    return render_template('rejestracja.html', title='rejestracja')


@app.route("/Logout")
def logout():
    return render_template('wyloguj.html', title='wyloguj')

if __name__ == '__main__':
    app.run(debug=True)