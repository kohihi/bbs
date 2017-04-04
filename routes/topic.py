from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import current_user
from models.topic import Topic
from models.board import Board

main = Blueprint('topic', __name__)


@main.route("/")
def index():
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.find_all(board_id=board_id)
    bs = Board.all()
    return render_template("topic/index.html", ms=ms, bs=bs)


@main.route("/<int:topic_id>")
def detail(topic_id):
    m = Topic.get(topic_id)
    return render_template("topic/detail.html", topic=m)


@main.route("/new")
def new():
    bs = Board.all()
    return render_template("topic/new.html", bs=bs)


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    topic = Topic.new(form, user_id=u.id, user=u.username)
    topic.save()
    return redirect(url_for('.detail', topic_id=topic.id))


@main.route("/delete/<int:topic_id>")
def delete(topic_id):
    Topic.delete(topic_id)
    return redirect(url_for('.index'))
