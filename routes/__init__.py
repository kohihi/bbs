from flask import session
from models.user import User
from utils import log


def current_user():
    uname = session.get('username', '')
    u = User.find_by(username=uname)
    return u
