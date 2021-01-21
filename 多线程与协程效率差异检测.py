import time
import gevent
import requests
from concurrent.futures import ThreadPoolExecutor, wait
from gevent import monkey
monkey.patch_all()


def func(url):
    """
    线程/协程运行函数，往返测试网站，打印返回数据中的网站地址
    """
    r = requests.get(url)
    print(r.json()['url'])


def async_func():
    """
    协程运行函数，计算并打印每轮调用所用时间，并统计总时间
    """
    global time_async
    print('async:\tON')
    t = time.time()
    gevent.joinall([gevent.spawn(func, u) for u in urls])
    tt = time.time() - t
    time_async += tt
    print('async:\t', tt)


def threads_func():
    """
    线程运行函数，计算并打印每轮调用所用时间，并统计总时间
    """
    global time_threads
    print('threads:\tON')
    t = time.time()
    p = ThreadPoolExecutor(100)
    ps = [p.submit(func, u) for u in urls]
    wait(ps)
    tt = time.time() - t
    time_threads += tt
    print('threads:\t', tt)

urls = ['http://httpbin.org/anything/{i}'.format(i=i) for i in range(100)]
time_async = 0
time_threads = 0

for i in range(5):
    async_func()
    time.sleep(3)
    threads_func()
    time.sleep(3)

print('async:\t', time_async)
print('threads\t', time_threads)