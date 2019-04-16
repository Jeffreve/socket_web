from models import Model
from models.session import Session
from models.todo import Todo
from utils import random_string, salted_password


class User(Model):
    def __init__(self, form):
        super().__init__(form)
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    @staticmethod
    def validate_login(username, password):
        u = User.find_by(username=username)
        return u is not None and u.password == salted_password(password)

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2

    @classmethod
    def login(cls, form):
        username = form.get('username')
        password = form.get('password')
        if User.validate_login(username, password):
            u = User.find_by(username=username)

            # session 会话
            session_id = random_string()
            form = dict(
                session_id=session_id,
                user_id=u.id,
            )
            s = Session.new(form)
            s.save()
            headers = {
                'Set-Cookie': 'session_id={}; path=/'.format(
                    session_id
                )
            }
            return u, None, headers
        else:
            message = '用户名或者密码错误'
            u = User.guest()
            return u, message, None

    @classmethod
    def register(cls, form):
        p = form['password']
        u = cls(form)
        if u.validate_register():
            u.password = salted_password(p)
            u.save()
            message = '注册成功<br> <pre>{}</pre>'.format(User.all())
        else:
            u = cls.guest()
            message = '用户名或者密码长度必须大于2'

        return u, message

    @staticmethod
    def guest():
        form = dict(
            id=-1,
            username='【游客】',
        )
        u = User.new(form)
        return u

    # todo add is_guest
    def is_guest(self):
        return self.id == User.guest().id
