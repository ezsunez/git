import multiprocessing
import os
from multiprocessing import Queue
from time import sleep

def func(d):
    print('mp on:\t', os.getpid())
    while True:
        try:
            n=d.get(timeout=5)
            print('mp--',n)
        except multiprocessing.queues.Empty:
            print('ERROR EMPTY')
            break
    print('mp off:\t', os.getpid())


if __name__=='__main__':
    print('main on:\t', os.getpid())
    qq=Queue()
    p=multiprocessing.Process(target=func,args=(qq,))
    p.start()
    for i in range(5):
        qq.put(i)
        print('put',i)
        sleep(2)
    p.join()
    print('main off:\t', os.getpid())



