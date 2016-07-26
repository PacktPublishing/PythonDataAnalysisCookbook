from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

app = Flask(__name__)


@app.route('/')
def home():
    return "Test Site"


@app.route('/secure', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or\
                request.form['password'] != 'admin':
            error = 'Invalid password or user name.'
        else:
            return redirect(url_for('home'))
    return render_template('admin.html', error=error)


if __name__ == '__main__':
    app.run(debug=True)
