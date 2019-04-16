import time

from models import Model
from utils import formatted_time


class Todo(Model):
    def __init__(self, form):
        super().__init__(form)
        self.task = form.get('task', '')
        self.user_id = form.get('user_id', -1)
        self.created_time = form.get('created_time', 0)
        self.updated_time = form.get('updated_time', 0)

    @classmethod
    def add(cls, form, user_id):
        form['user_id'] = user_id
        t = int(time.time())
        form['created_time'] = t
        form['updated_time'] = t
        return cls.new(form)

    @classmethod
    def update(cls, form):
        todo_id = int(form['id'])
        t = cls.find(todo_id)

        # 这里只应该更新我们想要更新的东西
        valid_names = [
            'task',
        ]
        for key in form:
            if key in valid_names:
                setattr(t, key, form[key])
        t.updated_time = int(time.time())
        t.save()

    def created_time_formatted(self):
        return formatted_time(self.created_time)

    def updated_time_formatted(self):
        return formatted_time(self.updated_time)
