from models.comment import Comment
from models.user import User
from models.weibo import Weibo
from routes import (
    redirect,
    html_response,
    current_user,
    login_required,
    request_data)
from utils import template, log


def index(request):
    user = current_user(request)

    author_id = int(request.query.get('user_id', -1))
    if author_id == -1:
        author_id = user.id

    weibos = Weibo.find_all(user_id=author_id)
    body = template('routes_weibo/weibo_index.html', weibos=weibos)
    return html_response(body)


def new(request):
    body = template('routes_weibo/weibo_new.html')
    return html_response(body)


def add(request):
    u = current_user(request)
    form = request.form()
    Weibo.add(form, u.id)
    return redirect('/weibo/index?user_id={}'.format(u.id))


def delete(request):
    u = current_user(request)
    weibo_id = int(request.query.get('id', None))
    Weibo.delete_with_comments(weibo_id)
    return redirect('/weibo/index?user_id={}'.format(u.id))


def edit(request):
    weibo_id = int(request.query.get('id', -1))
    w = Weibo.find(weibo_id)
    body = template('routes_weibo/weibo_edit.html', weibo=w)
    return html_response(body)


def update(request):
    u = current_user(request)
    form = request.form()
    Weibo.update(form)
    return redirect('/weibo/index?user_id={}'.format(u.id))


def comment_add(request):
    u = current_user(request)
    form = request.form()
    Comment.add(form, u.id)
    return redirect('/weibo/index?user_id={}'.format(form['weibo_user_id']))


def comment_edit(request):
    comment_id = int(request.query.get('id', -1))
    c = Comment.find(comment_id)
    body = template('routes_weibo/comment_edit.html', comment=c)
    return html_response(body)


def comment_update(request):
    form = request.form()
    Comment.update(form)
    return redirect('/weibo/index?user_id={}'.format(form['weibo_user_id']))


def comment_delete(request):
    # 评论user或者微博user可以删除
    u = current_user(request)
    comment_id = int(request.query.get('id', None))
    c = Comment.find(comment_id)
    w_user_id = int(request.query.get('w_id', None))
    a = (u.id == c.user_id)
    b = (u.id == w_user_id)
    if a or b:
        Comment.delete(comment_id)
    return redirect('/weibo/index?user_id={}'.format(w_user_id))


def weibo_login_required(route_function):
    def f(request):
        data, u = request_data(request)
        weibo_id = int(data.get('id'))
        w = Weibo.find(weibo_id)
        if u.id == w.user_id:
            return route_function(request)
        else:
            log('错误用户 404')
            return redirect('/weibo/index?user_id={}'.format(w.user_id))
    return f


def comment_login_required(route_function):
    def f(request):
        data, u = request_data(request)
        comment_id = int(data.get('id'))
        c = Comment.find(comment_id)
        if u.id == c.user_id:
            return route_function(request)
        else:
            log('错误用户 404')
            weibo = Weibo.find(c.weibo_id)
            return redirect('/weibo/index?user_id={}'.format(weibo.user_id))
    return f


def route_dict():
    r = {
        '/weibo/index': login_required(index),
        '/weibo/new': login_required(new),
        '/weibo/edit': login_required(weibo_login_required(edit)),
        '/weibo/add': login_required(add),
        '/weibo/update': login_required(weibo_login_required(update)),
        '/weibo/delete': login_required(weibo_login_required(delete)),
        # 评论功能
        '/comment/add': login_required(comment_add),
        '/comment/edit': login_required(comment_login_required(comment_edit)),
        '/comment/update': login_required(comment_login_required(comment_update)),
        '/comment/delete': login_required(comment_delete),

    }
    return r
