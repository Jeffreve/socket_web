from utils import log, template
from routes import json_response, current_user, html_response, login_required
from models.ajaxtodo import Ajaxtodo


# 本文件只返回 json 格式的数据,而不是 html 格式的数据
def index(request):
    u = current_user(request)
    body = template('ajax_todo_index.html', u=u)
    return html_response(body)


def all(request):
    u = current_user(request)
    todos = Ajaxtodo.find_all_json(user_id=u.id)
    return json_response(todos)


def add(request):
    form = request.json()
    u = current_user(request)
    t = Ajaxtodo.add(form, u.id)
    return json_response(t.json())


def delete(request):
    todo_id = int(request.query.get('id'))
    t = Ajaxtodo.delete(todo_id)
    return json_response(t.json())


def update(request):
    form = request.json()
    t = Ajaxtodo.update(form)
    return json_response(t.json())


def route_dict():
    d = {
        '/ajax/todo/index': login_required(index),
        '/ajax/todo/all': all,
        '/ajax/todo/add': add,
        '/ajax/todo/delete': delete,
        '/ajax/todo/update': update,
    }
    return d
