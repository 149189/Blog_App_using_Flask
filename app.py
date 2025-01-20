import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from models import db, BlogPost

# Configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    posts = BlogPost.query.all()
    return render_template('index.html', posts=posts)

@app.route('/post/new', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image_file = request.files['image']

        if image_file:
            image_filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
        else:
            image_filename = None

        new_post = BlogPost(title=title, content=content, image=image_filename)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/post/<int:id>/edit', methods=['GET', 'POST'])
def edit_post(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        image_file = request.files['image']

        if image_file:
            image_filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
            post.image = image_filename

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/post/<int:id>/delete', methods=['POST'])
def delete_post(id):
    post = BlogPost.query.get_or_404(id)
    if post.image:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], post.image))
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
