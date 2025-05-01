from flask import Flask, render_template

app = Flask(__name__)




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/home')
def test():
    return render_template('altapagina.html')

@app.route('/loginstaffmuntm')
def loginstaff():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)