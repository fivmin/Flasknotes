from flask import Flask, render_template,request
import sqlite3
from datetime import *

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('notes.db')
    return (conn)

def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, date_posted TEXT, author TEXT);
    ''')
    conn.commit()
    conn.close()
    return


def add_note(note):
    conn = get_db_connection()
    cur = conn.cursor()
    l = cur.execute("SELECT title FROM notes WHERE title = ?",(note[0],)).fetchall()
    if not l:
        cur.execute('''
        INSERT INTO notes(title, date_posted, author) VALUES (?,?,?);
        ''', note)
    conn.commit()
    conn.close()
    return

def get_all_notes():   
    conn = get_db_connection()
    cur = conn.cursor()
    l = cur.execute("SELECT title, date_posted, author FROM notes").fetchall()
    conn.close()
    return l

def get_note(conn,title):
    cur = conn.cursor()
    l = cur.execute("SELECT title, date_posted, author FROM notes WHERE title = ?",(title,)).fetchall()
    return l

def delete_entry(title):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
    DELETE FROM notes WHERE title = ?
    ''',(title,))
    conn.commit()
    conn.close()
    return




@app.route("/add" , methods = ['POST','GET'])
def add():
	if request.method == 'POST':
		note = dict(request.form)
		today = datetime.now().strftime('%B %d,%Y %H:%:M:%S')
		note['date_posted'] = str(today)
		add_note((note['title'],note['author'],note['date_posted']))
	return render_template('add.html')	

@app.route("/delete" , methods = ['POST','GET'])
def delete():
    if request.method == "GET":
        return render_template("delete.html", post = False)
    elif request.method == "POST":
        note = dict(request.form)
        delete_entry((note['title']))
        return render_template("delete.html", post = True)





@app.route("/")
@app.route("/home")
def home():
	posts = get_all_notes()
	return render_template('home.html',posts = posts)

@app.route("/about")
def about():
	return render_template('about.html', title = 'About')




if __name__ == '__main__':
	app.run(debug=True)
