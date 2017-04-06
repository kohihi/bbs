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
    role = current_user().role
    if role != 1:
        return redirect(url_for('index.index'))
    else:
        bs = Board.all()
        return render_template('board/admin.html', bs=bs)


@main.route("/add", methods=["POST"])
def add():
    role = current_user().role
    if role != 1:
        return redirect(url_for('index.index'))
    else:
        form = request.form
        topic = Board.new(form)
        topic.save()
    return redirect(url_for('.admin'))


@main.route("/delete/<int:board_id>")
def delete(board_id):
    role = current_user().role
    if role != 1:
        return redirect(url_for('index.index'))
    else:
        Board.delete(board_id)
        return redirect(url_for('.admin'))
