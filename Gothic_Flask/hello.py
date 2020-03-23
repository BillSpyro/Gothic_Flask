from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/Intro')
def intro():
    return 'Hello, World!'

@app.route('/Game/<area>')
def area(area=None):
    return render_template('hello.html', area=area)
