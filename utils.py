import hashlib
import random

from jinja2 import Environment, FileSystemLoader
import os.path
import time


def log(*args, **kwargs):
    time_format = '%H:%M:%S'
    localtime = time.localtime(int(time.time()))
    formatted = time.strftime(time_format, localtime)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(formatted, *args, **kwargs)
        print(formatted, *args, file=f, **kwargs)


def configured_environment():
    path = '{}/templates/'.format(os.path.dirname(__file__))
    loader = FileSystemLoader(path)
    return Environment(loader=loader)


def template(path, **kwargs):
    t = configured_environment().get_template(path)
    return t.render(**kwargs)


def random_string():
    """
    生成一个随机的字符串
    """
    seed = 'bdjsdlkgjsklgelgjelgjsegker234252542342525g'
    s = ''
    for i in range(16):
        # 这里 len(seed) - 2 是因为我懒得去翻文档来确定边界了
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def salted_password(password, salt='$!@><?>HUI&DWQa`'):
    salted = password + salt
    h = hashlib.sha256(salted.encode('ascii')).hexdigest()
    return h


def formatted_time(t):
    time_format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(t))
    r = time.strftime(time_format, value)
    return r
