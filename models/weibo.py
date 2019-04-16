from models import Model
from models.comment import Comment
from models.user import User
from utils import log


class Weibo(Model):
    def __init__(self, form, user_id=-1):
        super().__init__(form)
        self.content = form.get('content', '')
        self.user_id = form.get('user_id', user_id)

    def comments(self):
        return Comment.find_all(weibo_id=self.id)

    def author(self):
        user_id = self.user_id
        u = User.find(user_id)
        return u.username

    @classmethod
    def add(cls, form, user_id):
        form['user_id'] = user_id
        Weibo.new(form)

    @classmethod
    def delete_with_comments(cls, user_id):
        cs = Comment.find_all(weibo_id=user_id)
        for c in cs:
            Comment.delete(c.id)
        cls.delete(user_id)

    @classmethod
    def update(cls, form):
        weibo_id = int(form['id'])
        w = cls.find(weibo_id)

        valid_names = [
            'content',
        ]
        for key in form:
            if key in valid_names:
                setattr(w, key, form[key])
        w.save()


