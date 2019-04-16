import time

from models import Model
from utils import formatted_time


class Ajaxtodo(Model):
    def __init__(self, form):
        super().__init__(form)
        self.task = form.get('task', '')
        self.user_id = form.get('user_id', -1)
        self.created_time = form.get('created_time')
        self.updated_time = form.get('updated_time')
        self.ct = self.formatted_created_time()
        self.ut = self.formatted_updated_time()

    @classmethod
    def add(cls, form, user_id):
        form['user_id'] = user_id
        t = int(time.time())
        form['created_time'] = t
        form['updated_time'] = t
        t = cls.new(form)
        return t

    @classmethod
    def update(cls, form):
        todo_id = int(form['id'])
        t = cls.find(todo_id)

        valid_names = [
            'task',
        ]
        for key in form:
            # 这里只应该更新我们想要更新的东西
            if key in valid_names:
                setattr(t, key, form[key])
        t.updated_time = int(time.time())
        t.ut = t.formatted_updated_time()
        t.save()
        return t

    def formatted_created_time(self):
        return formatted_time(self.created_time)

    def formatted_updated_time(self):
        return formatted_time(self.updated_time)
