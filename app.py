from flask import Flask, url_for, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/about')
def about():
    return """
        Your name: Sterling Michel
        CU ID: CU8072
        GitHub Username: sterlingmichel
        hours to complete lab: 3 hrs
    """

@app.route('/login')
def login():
    return 'login'

@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'


with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='Sterling Michel'))