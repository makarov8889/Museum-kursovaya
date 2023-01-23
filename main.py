import sqlite3

from flask import Flask, flash, session, redirect, url_for
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#vb,nb,mb
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '23874237948239487293487'
conn = sqlite3.connect('./blog.db')

users = [{'user': 'admin', 'psw': 'admin'}]

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text(300), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, title, text):
        self.title = title
        self.text = text



@app.route('/')
def index():
    return render_template("index.html")


@app.route('/create-article', methods=['POST','GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']
        article = Article(title=title, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            flash("Статья добавлена", category='succes')
        except:
            flash("Ошибка добавления статьи", category='error')
    return render_template("create-article.html")

@app.route('/news')
def news():
    items = Article.query.order_by(Article.id).all()
    return render_template("news.html", data=items)

@app.route('/contacts')
def contacts():
     return render_template("contacts.html")


@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST' and {'user': request.form['username'], 'psw': request.form['psw']} in users:
        session['userlogged'] = request.form['username']
        return redirect(url_for('profile'))
    else:
        flash("Ошибка входа", category='error')
    return render_template('login.html')

@app.route('/profile', methods=['POST', 'GET'])
def profile():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Добавить статью':
            return redirect(url_for('create_article'))
        elif request.form['submit_button'] == 'Выйти':
            session.clear()
            return redirect(url_for('login'))
    return render_template('profile.html')

if __name__ == "__main__":
    #with app.app_context():
        #db.session.add(Article('Тест', 'Тестовая новость', 1))
        #db.session.commit()
    app.run(debug=True)
