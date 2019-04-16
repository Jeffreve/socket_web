import json

from utils import log


def save(data, path):
    # 序列化
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        log('save', path, s, data)
        f.write(s)


def load(path):
    # 反序列化
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        log('load', s)
        return json.loads(s)


class Model(object):
    def __init__(self, form):
        self.id = form.get('id', None)

    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = 'db/{}.txt'.format(classname)
        return path

    @classmethod
    def _new_from_dict(cls, d):
        # dict to 实例
        m = cls({})
        for k, v in d.items():
            setattr(m, k, v)
        return m

    @classmethod
    def new(cls, form):
        # save，直接生成实例没有save
        m = cls(form)
        m.save()
        return m

    @classmethod
    def delete(cls, id):
        models = cls.all()
        index = -1
        for i, e in enumerate(models):
            if e.id == id:
                index = i
                break
        # 判断是否找到了这个 id 的数据
        if index != -1:
            o = models.pop(index)
            l = [m.__dict__ for m in models]
            path = cls.db_path()
            save(l, path)
            # 返回被删除的元素
            return o

    @classmethod
    def all(cls):
        path = cls.db_path()
        models = load(path)
        ms = [cls(m) for m in models]
        # 返回实例
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        log('kwargs, ', kwargs, type(kwargs))
        for m in cls.all():
            exist = False
            for key, value in kwargs.items():
                k, v = key, value
                if v == getattr(m, k):
                    exist = True
                else:
                    exist = False
            if exist:
                return m
        return None

    @classmethod
    def find(cls, id):
        return cls.find_by(id=id)

    @classmethod
    def find_all(cls, **kwargs):
        log('kwargs, ', kwargs, type(kwargs))
        models = []
        for m in cls.all():
            exist = False
            for key, value in kwargs.items():
                k, v = key, value
                if v == getattr(m, k):
                    exist = True
                else:
                    exist = False
            if exist:
                models.append(m)
        return models

    def save(self):
        models = self.all()
        log('models', models)

        first_index = 0
        if self.id is None:
            log('id is None')
            if len(models) == 0:
                log('first index', first_index)
                self.id = first_index
            else:
                self.id = models[-1].id + 1
            models.append(self)
        else:
            log('id is not None')
            # 有 id 说明已经是存在于数据文件中的数据
            # 那么就找到这条数据并替换
            for i, m in enumerate(models):
                if m.id == self.id:
                    models[i] = self

        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)

    def json(self):
        # 返回当前 model 的字典表示
        d = self.__dict__
        return d

    def find_by_json(self):
        pass

    @classmethod
    def find_all_json(cls, **kwargs):
        models = cls.find_all(**kwargs)
        models = [m.json() for m in models]
        return models

    @classmethod
    def find_all_json_add_user(cls, **kwargs):
        models = cls.find_all(**kwargs)
        js = []
        for m in models:
            d = m.json()
            d['user'] = m.user()
            js.append(d)
        return js
