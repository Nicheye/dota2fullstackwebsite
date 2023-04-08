from flask import Blueprint, render_template, request, flash, redirect, url_for,Response,send_from_directory
    
from flask_login import login_required, current_user
from .models import Post, User,Bookmarks
from . import db
from werkzeug.utils import secure_filename
import base64
import os
views = Blueprint("views", __name__)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
@views.route("/")
@views.route("/home")

def home():
    return render_template("index.html",user=current_user,book=Bookmarks)



@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        
        pic = request.files['pic']
        if not pic:
            return 'No pic uploaded!', 400
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            return 'Bad upload!', 400
        text = request.form.get('text')


        if not text:
            flash('Post cannot be empty', category='error')
            
        else:
            post = Post(text=text, author=current_user.id,img=pic.read(), name=filename, mimetype=mimetype)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            
            return redirect(url_for('views.Forum'))
    return render_template('create_post.html', user=current_user)



@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.id:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('views.home'))


@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))
    

    posts = Post.query.filter_by(author=user.id).all()
    return render_template("posts.html", user=current_user, posts=posts, username=username)
@login_required
@views.route("/forum")
def Forum():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)

@views.route("/posts/<int:id>")
def see_wardmap(id):
    img = Post.query.filter_by(id=id).first()
    if not img:
        return 'Img Not Found!', 404

    return  Response(img.img, mimetype=img.mimetype)

@views.route("/miposhka")
def Miposhka():
    return render_template("miposhka.html",user=current_user)


@login_required
@views.route("/rename/<username>", methods=['GET', 'POST'])
def rename(username):
    if request.method == "POST":

        text = request.form.get('name')
        if not text:
            flash('name cannot be empty', category='error')
            
        else:
            
            user=current_user
            user.username=text
            db.session.commit()
            flash('name has changed!', category='success')
            
            return redirect(url_for('views.Forum'))
        
    return render_template("rename.html",user=current_user)