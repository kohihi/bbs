from models import Model
import time
from .user import User


class Reply(Model):
    def __init__(self, form):
        self.id = None
        self.content = form.get('content', '')
        self.ct = time.time()
        self.ut = self.ct
        self.topic_id = int(form.get('topic_id', -1))
        self.user_id = None

    def user(self):
        u = User.find_by(id=self.user_id)
        return u
