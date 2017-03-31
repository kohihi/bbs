from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
)
from models.user import User
from routes import current_user

main = Blueprint('index', __name__)


@main.route("/")
def index():
    u = current_user()
    return render_template('login.html', user=u)


@main.route("/register", methods=['POST'])
def register():
    form = request.form
    u = User.register(form)
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


@main.route('/profile')
def profile():
    u = current_user()
    if u in None:
        return redirect(url_for('.index'))
    else:
        return render_template('profile.html', user=u)
