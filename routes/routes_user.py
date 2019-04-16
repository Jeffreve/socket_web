from routes import (
    formatted_with_headers,
    redirect,
    current_user,
    html_response,
    login_required)

from utils import (
    log,
    template,
    salted_password)
from models.user import User


def login(request):
    form = request.form()
    u, message, headers = User.login(form)
    if u.is_guest():
        body = template('routes_user/user_login.html', username=u.username, message=message)
        return html_response(body)
    else:
        return redirect('/', headers)


def login_view(request):
    u = current_user(request)
    body = template('routes_user/user_login.html', username=u.username, message='')
    return html_response(body)


def register(request):
    form = request.form()
    u, message = User.register(form)
    if u.is_guest():
        body = template('routes_user/user_register.html', message=message)
        return html_response(body)
    else:
        return redirect('/user/login/view')


def register_view(request):
    body = template('routes_user/user_register.html', message='')
    return html_response(body)


def user_profile(request):
    u = current_user(request)
    body = template('routes_user/user_profile.html', username=u.username, id=u.id)
    return html_response(body)


def user_admin_users(request):
    u = current_user(request)
    if u.id == 0:
        users = User.all()
        body = template('routes_user/user_admin.html', users=users)
        return html_response(body)
    else:
        return redirect('/user/login/view')


def user_admin_update(request):
    u = current_user(request)
    if u.id == 0:
        form = request.form()
        u_id = int(form.get('id', None))
        u = User.find(u_id)
        p = form.get('password', None)
        u.password = salted_password(p)
        u.save()
        return redirect('/user/admin')
    else:
        return redirect('/user/login/view')


def route_dict():
    r = {
        '/user/login': login,
        '/user/login/view': login_view,
        '/user/register': register,
        '/user/register/view': register_view,
        '/user/profile/view': login_required(user_profile),
        '/user/admin': user_admin_users,
        '/user/admin/update': user_admin_update,
    }
    return r
