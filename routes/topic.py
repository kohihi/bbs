from utils import log
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    Response,
)

from routes import current_user
from models.topic import Topic
from models.board import Board

main = Blueprint('topic', __name__)


@main.route("/")
def index():
    if current_user() is None:
        return redirect(url_for('index.index'))
    board = request.args.get('board', 'all')
    u = current_user()
    if board == 'all':
        ms = Topic.all(deleted=False)
    else:
        ms = Topic.find_all(board=board)
        log('routes-topic-l27-title:', board)
    bs = Board.all(deleted=False)
    return render_template("topic/index.html", ms=ms, bs=bs, user=u)


@main.route("/<topic_id>")
def detail(topic_id):
    topic_id = str(topic_id)
    m = Topic.get(topic_id)
    if m.deleted is False:
        board = m.board
        return render_template("topic/detail.html", topic=m, board=board)
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
    t_id = str(topic_id)
    Topic.delete(t_id)
    return redirect(url_for('.index'))
