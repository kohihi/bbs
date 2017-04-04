from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import current_user
from models.board import Board

main = Blueprint('board', __name__)


@main.route("/admin")
def admin():
    return render_template('board/admin.html')


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    topic = Board.new(form)
    topic.save()
    return redirect(url_for('topic.index'))
