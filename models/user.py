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
        ('user_image', str, 'default.png'),
        ('role', int, 11),
    ]

    # # 使用了基类 model 的 _new_from_dict(), 尝试停用所有 Model 子类的此函数
    # def from_form(self, form):
    #     self.username = form.get('username', '')
    #     self.password = form.get('password', '')
    #     self.user_image = form.get('user_image', 'default.png')
    #     self.role = int(form.get('role', 11))

    @classmethod
    def salted_password(cls, password, salt=password_salt):
        salt_psw = password + salt
        ascii_str = salt_psw.encode('ascii')
        hash_psw = hashlib.sha256(ascii_str).hexdigest()
        return hash_psw

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')
        # state_code
        sc = 200
        if len(name) < 2:
            sc = 203
            return sc
        if len(pwd) < 6:
            sc = 202
            return sc
        if User.find_by(username=name) is not None:
            sc = 201
            return sc
        u = User()
        u = u.new(form)
        u.password = u.salted_password(pwd)
        u.save()
        return sc

    @classmethod
    def validate_login(cls, form):
        name = form.get('username', None)
        password = form.get('password', None)
        user = User.find_by(username=name)
        if user is not None and user.password == User.salted_password(password):
            log('login--', name)
            return user
        else:
            log('login fail--', name)
            return None
