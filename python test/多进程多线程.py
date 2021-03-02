import multiprocessing
import os
from multiprocessing import Queue
from time import sleep
from concurrent.futures import ThreadPoolExecutor, wait
from threading import current_thread


def func(d):

    print('mp on:\t', os.getpid())
    p = ThreadPoolExecutor(3)
    ps = [p.submit(funt,d,i) for i in range(10) ]
    wait(ps)
    print('mp off:\t', os.getpid())

def funt(d,i):
    d.put(i)
    sleep(2)
    print(i,current_thread())




if __name__=='__main__':
    print('main on:\t', os.getpid())
    qq=Queue()
    p=multiprocessing.Process(target=func,args=(qq,))
    p.start()
    while True:
        try:
            print(qq.get(timeout=5))
        except multiprocessing.queues.Empty:
            print('ERROR EMPTY')
            break
    p.join()
    print('main off:\t', os.getpid())


