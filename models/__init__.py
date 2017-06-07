import json
from utils import log
from pymongo import MongoClient
from bson.objectid import ObjectId
import time

client = MongoClient()
db = client.BBS

# txt-data 时期的 save()
'''
save 函数替换为 insert
def save(data, path):
    """
    将数据保存到文件，调试中代替数据库
    :param data: dict | list
    :param path: 数据文件路径
    :return: 
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        f.editor(s)
'''


# save, 原名 insert
'''
def save(cls):
    """
    接受一个类的桑实例作为参数，获取类名，插入到对应的数据表中
    :param cls:
    """
    name = cls.__class__.__name__
    log('(models) class name:', name)
    data_dict = cls.__dict__
    log('(models)data_dict:\n', data_dict)
    log('(models) db:', db)
    db[name].insert(data_dict)
'''

# txt-data 时期的 load()
'''
完成实际数据库迁移，load 函数不需要了 
def load(path):
    """
    载入文件内容
    :param path: 数据文件路径 
    :return: json
    """
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        return json.loads(s)
'''


# class Model(object):
#     """
#     所有 model 的基类
#     """
#
#     def __repr__(self):
#         classname = self.__class__.__name__
#         properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
#         s = '\n'.join(properties)
#         return '< {}\n{}\n>\n'.format(classname, s)
#
#     @classmethod
#     def db_path(cls):
#         """
#         得到 model 的数据文件路径
#         :return: path
#         """
#         classname = cls.__name__
#         path = 'data/{}.txt'.format(classname)
#         return path
#
#     @classmethod
#     def _new_from_dict(cls, d):
#         """
#         使用 dict 生成新的 model 对象
#         :param d: class 参数字典
#         :return:
#         """
#         # 使用空字典实例化一个对象
#         m = cls({})
#         # 从 d 中将 class 属性取出
#         for k, v in d.items():
#             # 使用 setattr 函数设置 m 的属性
#             setattr(m, k, v)
#         return m
#
#     @classmethod
#     def new(cls, form, **kwargs):
#         m = cls(form)
#         for k, v in kwargs.items():
#             setattr(m, k, v)
#         return m
#
#     @classmethod
#     def all(cls):
#         log('models, l-73 is all')
#         """
#         得到所有 models
#         :return:
#         """
#         path = cls.db_path()
#         models = load(path)
#         ms = [cls._new_from_dict(m) for m in models]
#         return ms
#
#     @classmethod
#     def find_by(cls, **kwargs):
#         k, v = '', ''
#         for key, value in kwargs.items():
#             k, v = key, value
#         all_m = cls.all()
#         for m in all_m:
#             if v == m.__dict__[k]:
#                 return m
#         return None
#
#     @classmethod
#     def find_all(cls, **kwargs):
#         k, v = '', ''
#         ms = []
#         for key, value in kwargs.items():
#             k, v = key, value
#         all_m = cls.all()
#         for m in all_m:
#             if v == m.__dict__[k]:
#                 ms.append(m)
#         return ms
#
#     def save(self):
#         models = self.all()
#         if self.id is None:
#             if len(models) == 0:
#                 self.id = 1
#             else:
#                 m = models[-1]
#                 self.id = m.id + 1
#             models.append(self)
#         else:
#             index = -1
#             for i, m in enumerate(models):
#                 if m.id == self.id:
#                     index = i
#                     break
#             models[index] = self
#         l = [m.__dict__ for m in models]
#         path = self.db_path()
#         save(l, path)
#
#     @classmethod
#     def delete(cls, id):
#         models = cls.all()
#         index = -1
#         for i, e in enumerate(models):
#             if e.id == id:
#                 index = i
#                 break
#         # 判断是否找到了这个 id 的数据
#         if index == -1:
#             # 没找到
#             pass
#         else:
#             obj = models.pop(index)
#             l = [m.__dict__ for m in models]
#             path = cls.db_path()
#             save(l, path)
#             # 返回被删除的元素
#             return obj


class Model(object):
    """
    所有 model 的基类
     """
    __fields__ = [
        '_id',
        ('type', str, ''),
        ('deleted', bool, False),
        ('ct', int, 0),
        ('ut', int, 0),
    ]

    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{}\n>\n'.format(classname, s)

    # txt-data 时期获取 data path 的函数
    # @classmethod
    # def db_path(cls):
    #     """
    #     得到 model 的数据文件路径
    #     :return: path
    #     """
    #     classname = cls.__name__
    #     path = 'data/{}.txt'.format(classname)
    #     return path

    @classmethod
    def _new_from_dict(cls, d):
        """
        使用 dict 生成新的 model 对象
        :param d: class 参数字典
        :return: 
        """
        # 使用空字典实例化一个对象
        m = cls()
        fields = cls.__fields__.copy()
        fields.remove('_id')
        # 从 d 中将 class 属性取出
        for f in fields:
            log('** f', f)
            # key，type，value
            k, t, v = f
            if k in d:
                log('** k', k)
                log('** d[k]', d[k])
                setattr(m, k, d[k])
                log('*** m', m)
            else:
                setattr(m, k, v)
        m.type = cls.__name__.lower()
        return m

    @classmethod
    def _new_with_db(cls, dbs):
        """
        给内部 all() 使用
        从 mongo 数据中恢复一个 model
        :param dbs: 一个 mongo 数据
        :return: m: 一个 cls 的实例
        """
        m = cls()
        fields = cls.__fields__.copy()
        fields.remove('_id')
        for f in fields:
            # key，type，value
            k, t, v = f
            if k in dbs:
                setattr(m, k, dbs[k])
            else:
                setattr(m, k, v)
        setattr(m, '_id', dbs['_id'])
        m.type = cls.__name__.lower()
        return m

    @classmethod
    def _find(cls, **kwargs):
        log('** is _find', kwargs)
        name = cls.__name__
        flag_sort = '__sort'
        sort = kwargs.pop(flag_sort, None)
        ds = db[name].find(kwargs)
        # log('** len(ds)', len(ds))
        if sort is not None:
            ds = ds.sort(sort)
        l = [cls._new_with_db(d) for d in ds]
        return l

    # 使用了基类 model 的 _new_from_dict(), 尝试停用所有 Model 子类的此函数
    # def from_form(self, form):
    #     log('init pass')
    #     pass

    @classmethod
    def new(cls, form, **kwargs):
        m = cls()
        log('***models-init-new-m:', m.__fields__)
        m = m._new_from_dict(form)
        t = int(time.time())
        setattr(m, 'ct', t)
        setattr(m, 'ut', t)
        for k, v in kwargs.items():
            setattr(m, k, v)
        return m

    @classmethod
    def all(cls, **kwargs):
        log('models, l-73 is all')
        """
        得到所有 models
        :return: 
        """
        return cls._find(**kwargs)

    @classmethod
    def find_one(cls, **kwargs):
        l = cls._find(**kwargs)
        if len(l) > 0:
            return l[0]
        else:
            return None

    @classmethod
    def find_by(cls, **kwargs):
        return cls.find_one(**kwargs)

    @classmethod
    def find_all(cls, **kwargs):
        return cls._find(**kwargs)

    def save(self):
        name = self.__class__.__name__
        log('****', self.__dict__)
        db[name].save(self.__dict__)

    @classmethod
    def delete(cls, m_id):
        name = cls.__name__
        query = {
            '_id': ObjectId(m_id),
        }
        values = {
            'deleted': True
        }
        db[name].update_one(query, {"$set": values})
