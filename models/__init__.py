import json


def save(data, path):
    """
    将数据保存到文件，调试中代替数据库
    :param data: dict | list
    :param path: 数据文件路径
    :return: 
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(s)


def load(path):
    """
    载入文件内容
    :param path: 数据文件路径 
    :return: json
    """
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        return json.loads(s)


class Model(object):
    """
    所有 model 的基类
    """

    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__]
        s = '\n'.join(properties)
        return '< {}\n{}\n>\n'.format(classname, s)

    @classmethod
    def db_path(cls):
        """
        得到 model 的数据文件路径
        :return: path
        """
        classname = cls.__name__
        path = 'data/{}.txt'.format(classname)
        return path

    @classmethod
    def _new_from_dict(cls, d):
        """
        使用 dict 生成新的 model 对象
        :param d: class 参数字典
        :return: 
        """
        # 使用空字典实例化一个对象
        m = cls({})
        # 从 d 中将 class 属性取出
        for k, v in d.items():
            # 使用 setattr 函数设置 m 的属性
            setattr(m, k, v)
        return m

    @classmethod
    def new(cls, form, **kwargs):
        m = cls(form)
        for k, v in kwargs.items():
            setattr(m, k, v)
        return m

    @classmethod
    def all(cls):
        """
        得到所有 models
        :return: 
        """
        path = cls.db_path()
        models = load(path)
        ms = [cls._new_from_dict(m) for m in models]
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all_m = cls.all()
        for m in all_m:
            if v == m.__dict__[k]:
                return m
        return None

    @classmethod
    def find_all(cls, **kwargs):
        k, v = '', ''
        ms = []
        for key, value in kwargs.items():
            k, v = key, value
        all_m = cls.all()
        for m in all_m:
            if v == m.__dict__[k]:
                ms.append(m)
        return ms

    def save(self):
        models = self.all()
        if self.id is None:
            if len(models) == 0:
                self.id = 1
            else:
                m = models[-1]
                self.id = m.id + 1
            models.append(self)
        else:
            index = -1
            for i, m in enumerate(models):
                if m.id == self.id:
                    index = i
                    break
            models[index] = self
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)
