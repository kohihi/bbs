from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import current_user
from models.topic import Topic

main = Blueprint('topic', __name__)


@main.route("/")
def index():
    ms = Topic.all()
    return render_template("topic/index.html", ms=ms)


@main.route("/<int:id>")
def detail(id):
    m = Topic.get(id)
    return render_template("topic/detail.html", topic=m)


@main.route("/new")
def new():
    return render_template("topic/new.html")


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    topic = Topic.new(form, user_id=u.id, user=u.username)
    topic.save()
    return redirect(url_for('.detail', id=topic.id))
