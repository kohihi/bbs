from models import Model
import time
from utils import log


class Board(Model):
    __fields__ = Model.__fields__ + [
        ('title', str, ''),
    ]

    def from_form(self, form):
        self.title = form.get('title', None)

    # self.id = None
    # self.title = form.get('title', '')
    # self.ct = int(time.time())
    # self.ut = self.ct
