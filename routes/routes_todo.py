from models.todo import Todo
from routes import (
    redirect,
    current_user,
    login_required,
    html_response
)

from utils import template, log


def index(request):
    u = current_user(request)
    todos = Todo.find_all(user_id=u.id)
    body = template(
        'routes_todo/todo_index.html',
        todos=todos,
    )
    return html_response(body)


def add(request):
    u = current_user(request)
    form = request.form()
    Todo.add(form, u.id)
    return redirect('/todo/all')


def delete(request):
    todo_id = int(request.query['id'])
    Todo.delete(todo_id)
    return redirect('/todo/all')


def edit(request):
    todo_id = int(request.query['id'])
    t = Todo.find(todo_id)
    body = template('routes_todo/todo_edit.html', todo=t)
    return html_response(body)


def update(request):
    form = request.form()
    Todo.update(form)
    return redirect('/todo/all')


def todo_login_required(route_function):
    def f(request):
        if request.method == 'POST':
            data = request.form()
        else:
            data = request.query
        u = current_user(request)
        todo_id = int(data.get('id'))
        t = Todo.find(todo_id)
        if u.id == t.user_id:
            return route_function(request)
        else:
            log('错误用户 404')
            return redirect('/todo/all')
    return f


def route_dict():
    d = {
        '/todo/add': login_required(add),
        '/todo/delete': login_required(todo_login_required(delete)),
        '/todo/edit': login_required(todo_login_required(edit)),
        '/todo/update': login_required(todo_login_required(update)),
        '/todo/all': login_required(index),
    }
    return d
