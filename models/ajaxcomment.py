from models import Model
from models.user import User


class Ajaxcomment(Model):
    def __init__(self, form, user_id=-1):
        super().__init__(form)
        self.content = form.get('content', '')
        self.user_id = form.get('user_id', -1)
        self.weibo_id = int(form.get('weibo_id', -1))
        self.weibo_user_id = int(form.get('weibo_user_id', -1))

    def user(self):
        u = User.find_by(id=self.user_id)
        return u.username

    @classmethod
    def add(cls, form, user_id):
        form['user_id'] = user_id
        return cls.new(form)

    @classmethod
    def update(cls, form):
        comment_id = int(form.get('id'))
        c = cls.find(comment_id)

        valid_names = [
            'content',
        ]
        for key in form:
            if key in valid_names:
                setattr(c, key, form[key])
        c.save()
        return c
