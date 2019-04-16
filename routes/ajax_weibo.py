from models.ajaxcomment import Ajaxcomment
from utils import log, template
from routes import json_response, current_user, html_response, login_required
from models.ajaxweibo import AjaxWeibo


def index(request):
    u = current_user(request)
    author_id = int(request.query.get('user_id', -1))

    if author_id == u.id:
        body = template('ajax_weibo_index.html', u=u, author_id=author_id)
    else:
        body = template('ajax_weibo_index1.html', u=u, author_id=author_id)
    return html_response(body)


def all(request):
    author_id = int(request.query.get('author_id', -1))
    weibos = AjaxWeibo.find_all_json(user_id=author_id)
    return json_response(weibos)


def add(request):
    u = current_user(request)
    form = request.json()
    t = AjaxWeibo.add(form, u.id)
    return json_response(t.json())


def delete(request):
    weibo_id = int(request.query.get('id'))
    t = AjaxWeibo.delete_with_comments(weibo_id)
    return json_response(t.json())


def update(request):
    form = request.json()
    t = AjaxWeibo.update(form)
    return json_response(t.json())


def comment_all(request):
    author_id = int(request.query.get('author_id', -1))
    weibos = AjaxWeibo.find_all(user_id=author_id)

    l = []
    for w in weibos:
        l += Ajaxcomment.find_all_json_add_user(weibo_id=w.id)
    return json_response(l)


def comment_add(request):
    u = current_user(request)
    form = request.json()
    form['weibo_id'] = int(form['weibo_id'])
    t = Ajaxcomment.add(form, u.id)
    t.user = t.user()
    return json_response(t.json())


def comment_delete(request):
    comment_id = int(request.query.get('id'))
    t = Ajaxcomment.delete(comment_id)
    return json_response(t.json())


def comment_update(request):
    form = request.json()
    c = Ajaxcomment.update(form)
    c.user = c.user()
    return json_response(c.json())


def route_dict():
    d = {
        '/ajax/weibo/index': login_required(index),
        '/ajax/weibo/all': all,
        '/ajax/weibo/add': add,
        '/ajax/weibo/delete': delete,
        '/ajax/weibo/update': update,

        '/ajax/comment/all': comment_all,
        '/ajax/comment/add': comment_add,
        '/ajax/comment/delete': comment_delete,
        '/ajax/comment/update': comment_update,

    }
    return d
