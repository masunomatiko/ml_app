import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing

#configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

#create application
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
  return sqlite3.connect(app.config['DATABASE'])

def init_db():
  with closing(connect_db()) as db:
    with app.open_resource('schema.sql') as f:
      db.cursor().executescript(f.read().decode('utf-8'))
    db.commit()

#view    
@app.before_request
def before_request():
  g.db = connect_db()

@app.after_request
def after_request(response):
  g.db.close()
  return response

@app.route('/')
def show_entries():
  cur = g.db.execute('select title, text from entries order by id desc')
  entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
  return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
  g.db.execute('insert into entries (title, text) values (?, ?)', [request.form['title'], request.form['text']])
  g.db.commit()
  flash('New entry was successfully posted!')
  return redirect(url_for('show_entries'))

if __name__ == '__main__':
  app.run()
