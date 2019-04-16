from routes import (
    login_required,
    current_user,
    html_response)
from utils import template


def index(request):
    u = current_user(request)
    body = template('routes_user/index.html', u=u)
    return html_response(body)


def route_static(request):
    filename = request.query.get('file')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\n\r\n'
        binary = header + f.read()
        return binary


def route_dict():
    r = {
        # '/': index,
        '/': login_required(index),
        '/static': route_static,
    }
    return r
