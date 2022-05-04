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


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/szkolenie")
def szkolenie():
    return render_template('szkolenie.html', title='szkolenie')

@app.route("/materialy")
def materialy():
    return render_template('materialy.html', title='materialy')


if __name__ == '__main__':
    app.run(debug=True)