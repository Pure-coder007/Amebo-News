from flask import render_template, Flask, url_for, redirect, request, Blueprint, flash, session
from flask_login import login_required, current_user, login_user, logout_user
from app_config import db, bcrypt
from models import User, Post


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/index', methods=['GET', 'POST'])
def index():

    posts = Post.query.order_by(Post.date_posted.desc()).all()
    all_sports = Post.query.filter_by(category='Sports').order_by(Post.date_posted.desc()).limit(5).all()
    all_crime = Post.query.filter_by(category='Crime').order_by(Post.date_posted.desc()).limit(5).all()
    all_entertainment = Post.query.filter_by(category='Entertainment').order_by(Post.date_posted.desc()).limit(5).all()
    all_sex_relationship = Post.query.filter_by(category='Sex and Relationship').order_by(Post.date_posted.desc()).limit(5).all()
    


    latest_fashion_post = next((post for post in posts if post.category == 'Fashion and Beauty'), None)
    latest_tech = next((post for post in posts if post.category == 'Technology'), None)
    latest_sports = next((post for post in posts if post.category == 'Sports'), None)
    latest_crime = next((post for post in posts if post.category == 'Crime'), None)
    latest_entertainment = next((post for post in posts if post.category == 'Entertainment'), None)
    latest_sex_relationship = next((post for post in posts if post.category == 'Sex and Relationship'), None)

    print(latest_entertainment, 'TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT')

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

    return render_template('index.html', alert=alert, bg_color=bg_color, posts=posts, fashion_post=latest_fashion_post, tech=latest_tech, latest_sports=latest_sports, latest_crime=latest_crime, latest_sex_relationship=latest_sex_relationship, latest_entertainment=latest_entertainment, all_sports=all_sports, all_crime=all_crime, all_entertainment=all_entertainment, all_sex_relationship=all_sex_relationship)




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
    category = request.args.get('category', 'Sports')  # Default to 'Sports' if no category is specified
    posts = Post.query.filter_by(category=category).order_by(Post.date_posted.desc()).limit(8).all()

    latest_posts = {}
    for cat in ['Sports', 'Fashion and Beauty', 'Technology', 'Religion', 'Education and Career', 'Health', 'Science', 'Entertainment', 'Sex and Relationship', 'Crime', 'Politics', 'Education and Carrer']:
        latest_post = next((post for post in posts if post.category == cat), None)
        latest_posts[cat] = latest_post

    # Now, latest_posts dictionary contains the latest post for each category, or None if no post was found
    return render_template('category.html', posts=posts, **latest_posts)
    