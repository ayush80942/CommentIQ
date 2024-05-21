from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    url = request.form.values
    return render_template("dashboard.html")

if __name__ == '__main__':
    app.run(debug=True)