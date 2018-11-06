
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

blog=['test']

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(2000))

    def __init__(self, title, body):
        self.title = title
        self.body = body


def not_empty(x):
    if len(x) == 0:
        return False
    else:
        return True

@app.route("/")
def index():
    return render_template('home.html', blog=blog)

@app.route("/newpost")
def newpost():
    return render_template('new-post.html')

@app.route("/newpost", methods=['POST'])
def validate_input():
    title = request.form.get('title')
    body = request.form.get('body')

    title_error = ''
    body_error = ''
    
    if not not_empty(title):
        title_error = "Title cannot be blank."
    
    if not not_empty(body):
        body_error = "Body cannot be blank."

    if not title_error and not body_error:
        return render_template('post.html', title=title, body=body, title_error=title_error, body_error=body_error)
    else: 
        return render_template('new-post.html', title=title, body=body, title_error=title_error, body_error=body_error)


@app.route("/blog")
def blog_home():
    return render_template('home.html', blog=blog)

@app.route("/post", methods=['POST'])
def post():
    title = request.form.get('title')
    body = request.form.get('body')
    return render_template('post.html', title=title, body=body)

app.run()