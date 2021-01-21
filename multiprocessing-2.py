import multiprocessing
import os
from multiprocessing import Queue
from time import sleep

def func(d):
    print('mp on:\t', os.getpid())
    # print(d)
    for i in range(0, 5):
        d.put(i)
        sleep(2)
    print('mp off:\t', os.getpid())


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
