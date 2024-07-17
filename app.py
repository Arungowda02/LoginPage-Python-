from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import bcrypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_kry'

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def checkPassword(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

with app.app_context():
    db.create_all()        

@app.route('/')
def start():
    return render_template('registration.html')
  

@app.route('/login',  methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email = email).first()

        if user and user.checkPassword(password):
            session['email'] = user.email
            session['password'] = user.password
            return redirect('/index')
        else:
            return render_template('login.html', error = 'Invalid user')

        
    return render_template('login.html')

@app.route('/registration', methods=['POST','GET'])
def registration():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name = name, email = email, password = password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('registration.html')

@app.route('/index')
def index():
    if session['email']:
        user = User.query.filter_by(email = session['email']).first()
        return render_template('index.html', user = user)
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)