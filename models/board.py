from models import Model
import time
from utils import log


class Board(Model):
    __fields__ = Model.__fields__ + [
        ('title', str, ''),
    ]

    # # 使用了基类 model 的 _new_from_dict(), 尝试停用所有 Model 子类的此函数
    # def from_form(self, form):
    #     self.title = form.get('title', None)

    # self.id = None
    # self.title = form.get('title', '')
    # self.ct = int(time.time())
    # self.ut = self.ct
