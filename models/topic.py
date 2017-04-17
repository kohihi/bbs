import time
from models import Model
from .reply import Reply
from bson.objectid import ObjectId


class Topic(Model):
    __fields__ = Model.__fields__ + [
        ('title', str, ''),
        ('content', str, ''),
        ('user', str, ''),
        ('views', int, 0),
        ('board', str, 'no-board'),
    ]

    def from_form(self, form):
        self.content = form.get('content', '')
        self.title = form.get('title', '')
        self.user = form.get('username', '')
        self.views = 0
        self.board = form.get('board_title', 'no-title')

    @classmethod
    def get(cls, id):
        m = cls.find_by(_id=ObjectId(id))
        m.views += 1
        m.save()
        return m

    def replies(self):
        ms = Reply.find_all(topic_id=str(self._id))
        return ms
