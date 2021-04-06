import os
from forms import  AddForm , DelForm
from flask import Flask, render_template, url_for, redirect,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

class Puppy(db.Model):

    __tablename__ = 'puppies'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.Text)

    def __init__(self,name):
        self.name = name

class Users(db.Model):

  __tablename__ = 'users'
  username = db.Column(db.Text,primary_key=True)
  password = db.Column(db.Text)
  def __init__(self,username, password):
      self.username = username
      self.password = password

db.create_all()
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/add', methods=['GET', 'POST'])
def add_pup():
    title = "Add new Puppy"
    puppyID = request.args.get("id")
    if puppyID is not None:
        puppy = Puppy.query.get(puppyID)
        title="Edit Puppy Name"
    form = AddForm()
    if form.validate_on_submit():
        name = form.name.data
        if puppyID is None:
            new_pup = Puppy(name)
            title = "Add new Puppy"
        else:
            new_pup = puppy
            new_pup.name = name
        db.session.add(new_pup)
        db.session.commit()
        return redirect(url_for('list_pup'))
    else:
        if puppyID is not None:
            form.name.data = puppy.name
    return render_template('add.html', form=form, title=title)

@app.route('/list')
def list_pup():
    puppy = Puppy.query.all()
    return render_template('list.html', puppies=puppy)

@app.route('/delete', methods=['GET', 'POST'])
def del_pup():
    puppyID=request.args.get("id")
    print(puppyID)
    form = DelForm()

    #if form.validate_on_submit():
    id = puppyID
    pup = Puppy.query.get(id)
    db.session.delete(pup)
    db.session.commit()

    return redirect(url_for('list_pup'))
    #return render_template('delete.html',form=form)

@app.route('/register', methods=['GET'])
def sign_up():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def sign_up_post():
    email=request.form.get("email")
    pwd=request.form.get("pwd")
    user=Users(email,pwd)
    emailUser=Users.query.get(email)
    fail=False
    if emailUser is None:
        db.session.add(user)
        db.session.commit()
        return render_template('login.html',fail=fail)
    else:
        fail=True
        error="User exists"
        return render_template('register.html',error=error,fail=fail)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email=request.form.get("email")
    pwd=request.form.get("pwd")
    user = Users.query.get(email)
    if(user is not None and user.password == pwd):
        fail=False
        return redirect(url_for('list_pup'))
    else:
        fail=True
        return render_template('login.html',fail=fail)


if __name__ == '__main__':
    app.run(debug=True)
