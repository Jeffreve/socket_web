import _thread
import socket

from utils import log
from request import Request

from routes import error
from routes.routes_static import route_dict as routes_static
from routes.routes_user import route_dict as routes_user

from routes.routes_todo import route_dict as routes_todo
from routes.routes_weibo import route_dict as routes_weibo

from routes.ajax_todo import route_dict as ajax_todo
from routes.ajax_weibo import route_dict as ajax_weibo


def response_for_path(request):
    r = {}
    r.update(routes_static())
    r.update(routes_user())

    r.update(routes_todo())
    r.update(routes_weibo())

    r.update(ajax_todo())
    r.update(ajax_weibo())

    response = r.get(request.path, error)
    return response(request)


def process_request(connection):
    with connection:
        r = connection.recv(1024)
        r = r.decode()
        log('request log:\n{}'.format(r))
        # 把原始请求数据传给 Request 对象
        request = Request(r)
        # 用 response_for_path 函数来得到 path 对应的响应内容
        response = response_for_path(request)
        log("response log:\n{}".format(response))
        # 把响应发送给客户端
        connection.sendall(response)


def run(host, port):
    """
    启动服务器
    """
    # 使用 with 可以保证程序中断的时候正确关闭 socket 释放占用的端口
    log('开始运行于', '{}:{}'.format(host, port))
    with socket.socket() as s:
        # 使用 下面这句 可以保证程序重启后使用原有端口, 原因忽略
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        # 无限循环来处理请求
        while True:
            connection, address = s.accept()
            log('ip {}'.format(address))
            _thread.start_new_thread(process_request, (connection,))


if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        host='127.0.0.1',
        port=3000,
    )
    run(**config)



