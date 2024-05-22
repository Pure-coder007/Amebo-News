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

app = Flask(__name__)
app.secret_key = "wrweerrhttjytjtdjydtytytytdytdhghmftytdmtty,mtdmyty,mytftdjrtereyrsjtrjmtdy"

app.config['UPLOADED_PHOTOS_DEST'] = 'static/assets/img'



@posts.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    if not current_user.admin:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        content = request.form.get('content')
        date_posted = datetime.now()
        image = request.files.get('image')
        user_id = current_user.id

        if image:
            filename = secure_filename(image.filename)
            response = cloudinary.uploader.upload(image, public_id=f"posts/{filename}")
            image = response['secure_url']
        
        post = Post(title=title, category=category, content=content, date_posted=date_posted, image=image, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('new_post.html')