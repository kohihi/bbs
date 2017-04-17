from models import (
    Model,
)
from config import password_salt
from utils import log
import hashlib


class User(Model):
    __fields__ = Model.__fields__ + [
        ('username', str, ''),
        ('password', str, ''),
        ('user_image', str, ''),
        ('role', int, 11),
    ]

    def from_form(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.user_image = form.get('user_image', 'default.png')
        self.role = int(form.get('role', 11))

    def salted_password(self, password, salt=password_salt):
        salt_psw = password + salt
        ascii_str = salt_psw.encode('ascii')
        hash_psw = hashlib.sha256(ascii_str).hexdigest()
        return hash_psw

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')
        if len(name) > 2 and len(pwd) >= 6 and User.find_by(username=name) is None:
            u = User()
            u.from_form(form)
            u.password = u.salted_password(pwd)
            u.save()
            return True
        else:
            return False

    @classmethod
    def validate_login(cls, form):
        u = User()
        u.from_form(form)
        user = User.find_by(username=u.username)
        if user is not None and user.password == u.salted_password(u.password):
            log('login--', u.username)
            return user
        else:
            log('login fail--', u.username)
            return None
