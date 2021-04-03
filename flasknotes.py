from flask import Flask, render_template,request,redirect
import sqlite3
from datetime import *
import os
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'something'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    ENV="development"
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
app.config.from_object(DevelopmentConfig)


# database 
db = SQLAlchemy(app)



def create_db():
    db.create_all()

def drop_db():
    db.drop_all()

def create_table():
    Note.__table__.create(db.engine)


# Database model
class Note(db.Model):
    __tablename__ = "notes"
    id      = db.Column(db.Integer, primary_key = True)
    note   = db.Column(db.String(450), unique = True)
    date   = db.Column(db.String(250))
    body  = db.Column(db.String(700))
    op_1 = db.Column(db.String(700))
    deadline = db.Column(db.String(700))
    op_2 = db.Column(db.String(120))
    op_3 = db.Column(db.String(100))

    def __init__(self, note):
        self.note = note['note']
        self.date = note['date']
        self.body = note['body']
        # self.summary = note.summary
        # self.op_1 = note['op_1']
        # self.op_2 = note['op_2']
        # self.op_3 = note['op_3']
        self.op_1 = note['link']
        self.deadline = note['deadline']


@app.route("/add" , methods = ['POST','GET'])
def add():
    if request.method == "GET":
        return render_template('add.html')
    if request.method == 'POST':
        note = dict(request.form)
        today = datetime.now().strftime('%B %d, %Y %H:%M:%S')
        note['date'] = str(today)
        note = Note(note)
        db.session.add(note)
        db.session.commit()
        return redirect("/home")

@app.route("/delete/<id>")
def delete(id):
    id = id
    obj = Note.query.filter_by(id = id).one()
    db.session.delete(obj)
    db.session.commit()
    return render_template("home.html")





@app.route("/")
@app.route("/home")
def home():
    posts = Note.query.all()
    # print(posts)
    return render_template('home.html',posts = posts)

@app.route("/about")
def about():
	return render_template('about.html', title = 'About')




if __name__ == '__main__':
	app.run(debug=True)
