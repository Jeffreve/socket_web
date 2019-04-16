import json

from models.session import Session
from models.user import User
from utils import log


def current_user(request):
    session_id = request.cookies.get('session_id')
    if session_id is not None:
        s = Session.find_by(session_id=session_id)
        if s is not None and not s.expired():
            user_id = s.user_id
            log('current user id <{}>'.format(user_id))
            u = User.find_by(id=user_id)
            return u
        else:
            return User.guest()
    else:
        return User.guest()


def login_required(route_function):
    def f(request):
        u = current_user(request)
        if u.id == User.guest().id:
            log('非登陆用户 redirect')
            return redirect('/user/login/view')
        else:
            return route_function(request)

    return f


def error(request, code=404):
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def redirect(url, headers=None):
    h = {
        'Location': url,
    }
    if headers is None:
        headers = h
    else:
        headers.update(h)
    header = formatted_with_headers(headers, 302)
    r = header + '\r\n'
    return r.encode()


def formatted_with_headers(headers, code=200):
    """
    Content-Type: text/html
    Set-Cookie: user=hhh
    """
    header = 'HTTP/1.1 {} OK \r\n'.format(code)
    header += ''.join([
        '{}: {}\r\n'.format(k, v) for k, v in headers.items()
    ])
    return header


def html_response(body, headers=None):
    if headers is None:
        headers = {
            'Content-Type': 'text/html',
        }
    header = formatted_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode()


def request_data(request):
    u = current_user(request)
    if request.method == 'POST':
        data = request.form()
    else:
        data = request.query
    return data, u


def json_response(data):
    header = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n'
    body = json.dumps(data, ensure_ascii=False, indent=2)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')
