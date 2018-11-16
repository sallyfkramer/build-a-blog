
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

blog=[]

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(2000))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route("/")
def index():
    #TODO build query for database
    blog = Blog.query.all()
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
    
    if title.isspace():
        title_error = "Title cannot be blank."
    
    if body.isspace():
        body_error = "Body cannot be blank."

    if not title_error and not body_error:
        print("starting new blog with {0}, {1}".format(title, body))
        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.commit()
        return render_template('post.html', title=title, body=body, title_error=title_error, body_error=body_error)
    else: 
        return render_template('new-post.html', title=title, body=body, title_error=title_error, body_error=body_error)



@app.route("/blog", methods=['POST'])
def post():
    title = request.form.get('title')
    body = request.form.get('body')
    return render_template('post.html', title=title, body=body)

@app.route('/blog', methods=['GET'])
def view_post():
    #TODO build query for database
    blog = Blog.query.all()
    id_number = request.args.get('id') 
    veiw_blog = Blog.query.get(id_number)
    
    title = veiw_blog.title
    body = veiw_blog.body
    
    
    return render_template('post.html', id=id , title = title, body=body)




if __name__=='__main__':
    app.run()