#
# kernelThreadTest.py
# CS3070 
#
# created: Spring '16
# updated: 09 Jan 2026
#

from multiprocessing import Queue   #https://docs.python.org/3.11/library/multiprocessing.html
import os
import time
import sys

from support import SL_Process


class SL_Program(object):


    def __init__(self, name, q, args):
        self.name = name
        self.queue = q
        self.word = args

    

    def execute(self):
        self.queue.put(self.word)
        print("in", self.name, "execute(), pid = " + str(os.getpid()) + '\n')




####################################
####################################
####################################
#script starts here
##


if __name__ == '__main__':

    if not sys._is_gil_enabled():
        raise RuntimeError('not running under Python free-threading mode')
    print('\n\nif we see this we are running correctly in Python free-threading mode\n\n')


    q = Queue()
    
    program1 = SL_Program('program1', q, 42)
    program2 = SL_Program('program2', q,'testing')
    program3 = SL_Program('program3', q,'hello')

    p1 = SL_Process.SL_Process(program1)
    p2 = SL_Process.SL_Process(program2)
    p3 = SL_Process.SL_Process(program3)


    start = time.time()
    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()
    finish = time.time()
    print("joined")

    while not q.empty():
        print(q.get(), ' ', end = '')
    print()
    
    print('processing took', (finish - start), 'sec')