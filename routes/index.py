from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    send_from_directory,
)
from werkzeug.utils import secure_filename
from models.user import User
from routes import current_user
from config import (
    accept_user_file_type,
    user_file_director,
)
from utils import log
import os

main = Blueprint('index', __name__)


@main.route("/")
def index():
    u = current_user()
    return render_template('signin.html', user=u)


@main.route("/register", methods=['POST'])
def register():
    form = request.form
    User.register(form)
    return redirect(url_for('.index'))


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    # validate_login 返回 None 或 一个 User 对象
    # None 为登录失败
    u = User.validate_login(form)
    if u is None:
        return redirect(url_for('topic.index'))
    else:
        session['user_id'] = u.id
        session.permanent = True
        return redirect(url_for('topic.index'))

@main.route("/signin")
def signin():
    return render_template('signin.html')

@main.route("/signup")
def signup():
    return render_template('signup.html')


@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('profile.html', user=u)


def allow_file(filename):
    suffix = filename.split('.')[-1]
    return suffix in accept_user_file_type


# @main.route('/add_img', methods=["POST"])
# def add_img():
#     log('index l65 into add_img')
#     u = current_user()
#     log('index l67 current_user', u.username)
#     if u is None:
#         log('u is none')
#         return redirect(url_for('.profile'))
#
#     if 'file' not in request.files:
#         log('files', len(request.files))
#         return redirect(request.url)
#
#     file = request.files['file']
#     if file.filename == '':
#         log('filename is ''')
#         return redirect(request.url)
#
#     log('index l77 filename check ok')
#     if allow_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.sava(os.path.join(user_file_director, filename))
#         u.user_image = filename
#         u.save()
@main.route('/add_img', methods=["POST"])
def add_img():
    u = current_user()

    if u is None:
        return redirect(url_for(".profile"))

    if 'file' not in request.files:
        log('file on in files')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if allow_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(user_file_director, filename))
        u.user_image = filename
        u.save()

    return redirect(url_for(".profile"))


@main.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(user_file_director, filename)


