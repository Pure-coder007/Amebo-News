from flask import render_template, request, Flask, redirect, Blueprint, url_for, flash, session
from app_config import db, bcrypt
from flask_login import login_required, current_user, login_user, logout_user
from models import User, Post
from datetime import datetime
import cloudinary
import cloudinary.uploader
from werkzeug.utils import secure_filename



posts = Blueprint('posts', __name__)


cloudinary.config(
    cloud_name = "duyoxldib",
    api_key = "778871683257166",
  api_secret = "NM2WHVuvMytyfnVziuzRScXrrNk"
)