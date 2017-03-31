import time
from models import Model
from .reply import Reply


class Topic(Model):
    def __init__(self, form):
        self.id = None
        self.content = form.get('content', '')
        self.title = form.get('title', '')
        self.user_id = form.get('user_id', '')
        self.views = 0
        self.ct = int(time.time())
        self.ut = self.ct

    @classmethod
    def get(cls, id):
        m = cls.find_by(id=id)
        m.views += 1
        m.save()
        return m

    def replies(self):
        ms = Reply.find_all(topic_id=self.id)
        return ms
