from flask import render_template, Flask, url_for, redirect, request, Blueprint, flash, session
from flask_login import login_required, current_user, login_user, logout_user
from app_config import db, bcrypt
from models import User, Post


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/index', methods=['GET', 'POST'])
def index():

    posts = Post.query.order_by(Post.date_posted.desc()).all()

    


    latest_fashion_post = next((post for post in posts if post.category == 'Fashion and Beauty'), None)
    latest_tech = next((post for post in posts if post.category == 'Technology'), None)

    alert = session.pop('alert', None)
    bg_color = session.pop('bg_color', None)

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        print(username, email, password, confirm_password)

        user = User.query.filter_by(username=username).first()  or User.query.filter_by(email=email).first()
        if user:
            print('Username  or Email already exists')
            # session['alert'] = 'Username  or Email already exists'
            # session['bg_color'] = 'danger'
        elif password != confirm_password:
            session['alert'] = 'Passwords do not match'
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user = User(username=username, email=email, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            session['alert'] = 'Registeration successfully'
            session['bg_color'] = 'success'

            return redirect(url_for('main.index'))
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for('main.index'))
        else:
            session['alert'] = 'Invalid username or password'

    return render_template('index.html', alert=alert, bg_color=bg_color, posts=posts, fashion_post=latest_fashion_post, tech=latest_tech)




# Login
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True)
            print('Logged in successfully')
            session['alert'] = 'Login successful'
            session['bg_color'] = 'success'
        else:
            print('Invalid username or password')
            session['alert'] = 'Invalid username or password'
            session['bg_color'] = 'danger'
    return redirect (url_for('main.index'))




@main.route('/logout')
@login_required
def logout():
    logout_user()
    session['alert'] = 'Logged out successfully'
    session['bg_color'] = 'info'
    return redirect(url_for('main.index'))





@main.route('/category', methods=['GET', 'POST'])
def category():
    category = request.args.get('category', 'Sports')
    # Get all sports news
    posts = Post.query.filter_by(category=category).order_by(Post.date_posted.desc()).limit(8).all()
    print(posts, 'ppppppp')
    return render_template('category.html', posts=posts)