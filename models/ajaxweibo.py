from models import Model
from models.ajaxcomment import Ajaxcomment
from models.comment import Comment
from models.user import User


class AjaxWeibo(Model):
    """
    微博类
    """
    def __init__(self, form, user_id=-1):
        super().__init__(form)
        self.content = form.get('content', '')
        self.user_id = form.get('user_id', user_id)

    @classmethod
    def add(cls, form, user_id):
        form['user_id'] = user_id
        w = cls.new(form)
        return w

    @classmethod
    def delete_with_comments(cls, user_id):
        cs = Ajaxcomment.find_all(weibo_id=user_id)
        for c in cs:
            Ajaxcomment.delete(c.id)
        return cls.delete(user_id)

    @classmethod
    def update(cls, form):
        weibo_id = int(form.get('id'))
        w = cls.find(weibo_id)

        valid_names = [
            'content',
        ]
        for key in form:
            if key in valid_names:
                setattr(w, key, form[key])
        w.save()
        return w
