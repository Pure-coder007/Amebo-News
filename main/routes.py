from flask import render_template, Flask, url_for, redirect, request, Blueprint, flash, session
from flask_login import login_required, current_user, login_user, logout_user
from app_config import db, bcrypt
from models import User, Post


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')