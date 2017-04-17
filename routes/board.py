from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import current_user
from models.board import Board
from utils import log

main = Blueprint('board', __name__)


@main.route("/admin")
def admin():
    role = current_user().role
    if role != 1:
        return redirect(url_for('index.index'))
    else:
        bs = Board.all(deleted=False)
        return render_template('board/admin.html', bs=bs)


@main.route("/add", methods=["POST"])
def add():
    role = current_user().role
    if role != 1:
        return redirect(url_for('index.index'))
    else:
        form = request.form
        board = Board.new(form)
        log('route-board-l34-b_fields:', board.__fields__)
        board.save()
    return redirect(url_for('.admin'))


@main.route("/delete/<board>")
def delete(board):
    role = current_user().role
    if role != 1:
        return redirect(url_for('index.index'))
    else:
        b = Board.find_by(title=board)
        b_id = b._id
        Board.delete(b_id)
        return redirect(url_for('.admin'))
