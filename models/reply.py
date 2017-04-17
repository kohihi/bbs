from models import Model
import time
from .user import User


class Reply(Model):
    __fields__ = Model.__fields__ + [
            ('content', str, ''),
            ('topic_id', str, ''),
            ('username', str, ''),
        ]

    def from_form(self, form):
        self.content = form.get('content', '')
        self.topic_id = str(form.get('topic_id', ''))
        self.username = form.get('username', '')

    def user(self):
        u = User.find_by(username=self.username)
        return u
