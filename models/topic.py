import time
import json
from utils import log
from models import Model
from .reply import Reply
from .cache import RedisCache
from bson.objectid import ObjectId


class Topic(Model):
    __fields__ = Model.__fields__ + [
        ('title', str, ''),
        ('content', str, ''),
        ('user', str, ''),
        ('views', int, 0),
        ('board', str, 'no-board'),
    ]

# 使用了基类 model 的 _new_from_dict(), 尝试停用所有 Model 子类的此函数
# def from_form(self, form):
#     self.content = form.get('content', '')
#     self.title = form.get('title', '')
#     self.user = form.get('username', '')
#     self.views = 0
#     self.board = form.get('board_title', 'no-title')

    should_update_cache = True
    cache = RedisCache()

    def to_json(self):
        d = dict()
        for k in Topic.__fields__:
            key = k[0]
            if not key.startswith('_'):
                d[key] = getattr(self, key)
            else:
                key = '_id'
                d[key] = str(getattr(self, key))
        return json.dumps(d)

    @classmethod
    def from_json(cls, j):
        d = json.loads(j)
        t = cls()
        for k, v in d.items():
            setattr(t, k, v)
        return t

    @classmethod
    def get(cls, id):
        m = cls.find_by(_id=ObjectId(id))
        m.views += 1
        m.save()
        return m

    def replies(self):
        ms = Reply.find_all(topic_id=str(self._id))
        return ms

    @classmethod
    def cache_all(cls, **kwargs):
        if Topic.should_update_cache is True:
            log('update cache')
            Topic.cache.set('all_topic', json.dumps([i.to_json() for i in cls.all(**kwargs)]))
            Topic.should_update_cache = False
        j = json.loads(str(Topic.cache.get('all_topic'),encoding='utf-8'))
        j = [Topic.from_json(i) for i in j]
        return j