from models import (
    Model,
)
from config import password_salt
import hashlib


class User(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.role = 11

    def salted_password(self, password, salt=password_salt):
        salt_psw = password + salt
        ascii_str = salt_psw.encode('ascii')
        hash_psw = hashlib.sha256(ascii_str).hexdigest()
        return hash_psw

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')
        if User.find_by(username=name) is None:
            u = User.new(form)
            u.password = u.salted_password(pwd)
            u.save()
            return u

    @classmethod
    def validate_login(cls, form):
        u = User(form)
        user = User.find_by(username=u.username)
        if user is not None and user.password == u.salted_password(u.password):
            return user
        else:
            return None
