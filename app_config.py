from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import create_engine
import pymysql, mysql.connector




secret_key = 'sdfghjkdsfghjsretyrew6786543ertyhjnfde5467uijhgfdszxhjuytrewsdfghjgfdr'
app = Flask(__name__)


app.config['SECRET_KEY'] = secret_key
bcrypt = Bcrypt(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/amebo_news?charset=utf8mb4'
# configuring my sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from models import User, Post


from main.routes import main
app.register_blueprint(main)

from posts.routes import posts
app.register_blueprint(posts)