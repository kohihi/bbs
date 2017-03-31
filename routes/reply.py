from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
)
from models.reply import Reply
from routes import current_user

main = Blueprint('reply', __name__)


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    u = current_user()
    r = Reply.new(form, user_id=u.id)
    r.save()
    return redirect(url_for('topic.detail', id=r.topic_id))
