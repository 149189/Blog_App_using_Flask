from flask import Flask, render_template, request, redirect, url_for
from models import db, BlogPost

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    with app.app_context():
        db.create_all()  # Ensure tables are created
    posts = BlogPost.query.all()
    return render_template('index.html', posts=posts)

@app.route('/post/new', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = BlogPost(title=title, content=content)
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
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', post=post)

@app.route('/post/<int:id>/delete', methods=['POST'])
def delete_post(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
