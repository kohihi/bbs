from utils import log
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)
import mistune

from routes import current_user
from models.topic import Topic
from models.board import Board
from models.user import User
from bson.objectid import ObjectId

main = Blueprint('topic', __name__)


@main.route("/")
def index():
    log('** into topic.index')
    if current_user() is None:
        return redirect(url_for('index.index'))
    board = request.args.get('board', None)
    u = current_user()
    if board is None:
        ms = Topic.all(deleted=False)
    else:
        ms = Topic.find_all(deleted=False, board=board)
    bs = Board.all(deleted=False)
    return render_template("topic/index.html", ms=ms, bs=bs, user=u)


@main.route("/<topic_id>")
def detail(topic_id):
    topic_id = str(topic_id)
    m = Topic.get(topic_id)
    a = User.find_by(username=m.user)
    content = mistune.markdown(m.content)
    if m.deleted is False:
        board = m.board
        return render_template("topic/detail.html",content=content, topic=m, board=board, author=a)
    else:
        return redirect(url_for('topic.index'), 404)


@main.route("/new")
def new():
    bs = Board.all(deleted=False)
    return render_template("topic/new.html", bs=bs)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    topic = Topic.new(form, user=u.username)
    topic.save()
    return redirect(url_for('.detail', topic_id=str(topic._id)))


@main.route("/delete/<topic_id>")
def delete(topic_id):
    role = current_user().role
    if role == 1:
        t = Topic.find_by(_id=ObjectId(topic_id))
        if t is not None:
            t.deleted = True
            t.board = 'deleted'
            t.save()
            return redirect(url_for('index.admin'))
