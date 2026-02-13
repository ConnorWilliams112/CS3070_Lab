#
# userThreadTest.py
# CS3070 Synchronization Lab series
#
# created: Spring '16
# updated: 09 Jan 2026
#

from multiprocessing import Queue  #https://docs.python.org/3.11/library/multiprocessing.html
import threading
import os
import time
import sys

from support import SL_Thread


def f(q, word):
    ''' An example function to call.
        -q is a multiprocessing.Queue object
        -word is a string '''
    q.put(word)
    print("in f(), pid =" + str( os.getpid() ) + ", threadID =" + str( threading.get_ident() ) +'\n')




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
    
    t1 = SL_Thread.SL_Thread(f, (q,42))
    t2 = SL_Thread.SL_Thread(f, (q,'testing'))
    t3 = SL_Thread.SL_Thread(f, (q,'hello'))

    start = time.time()
    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()
    finish = time.time()
    print("joined")

    while not q.empty():
        print(q.get(), ' ', end = '')
    print()
    
    print('processing took', (finish - start), 'sec')