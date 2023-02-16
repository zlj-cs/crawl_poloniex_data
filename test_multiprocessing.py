# -*- coding:utf-8 -*-
from multiprocessing import Process
import os
import time
from multiprocessing import Pool

from matplotlib.pyplot import polar
 
def run_proc(name):
    time.sleep(2)
    print('Run child process %s (%s)...' % (name, os.getpid()))
 
 
def hello_world():
    # time.sleep(5)
    time.sleep(5)
    print('hello world!')
    print('Run child process (%s)...' % (os.getpid()))


 
def long_time_task(name, x):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(1)
    print(x)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))


def test_case(case_id=0):
    if case_id == 0:
        names = ["aa", "bb", "cc"]
        for n in names:
            p = Process(target=run_proc, args=(n,))
            p.start() # 每次都会阻塞，并行无效
            p.join()
        print("task over")
    elif case_id == 1:
        print ('Parent process %s.' % os.getpid())
        p1 = Process(target=run_proc, args=('test',))
        p2 = Process(target=hello_world)
        print('Process will start.')
        p1.start()
        p2.start()
        p1.join() # 等p1结束了之后，主程序可以继续执行下去。
        print('Process end.')
    elif case_id == 2:
        p = Pool(5)
        for i in range(10):
            p.apply_async(long_time_task, args=(i, i*2))
        print('Waiting for all subprocesses done...')
        p.close()# 必须在join前使用close
        p.join()# 等待p中进程全部完成
        print('All subprocesses done.')
    elif case_id == 3:
        t = [0, 1, 2, 3, 4, 5]
        def cube(x):
            print(1)
            t[x] = x**3
        pool = Pool(processes=4)
        for i in range(6):
            pool.apply_async(cube, args=(i, ))
        pool.close()
        pool.join()
        print(t)
    else:
        raise ValueError()
 
if __name__ == '__main__':
    test_case(case_id=2)
