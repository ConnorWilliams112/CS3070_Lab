#
# Semaphore.py
# CS3070 
#
# Authors: Montes - Papakostas - Sami - Williams
# created: Spring '16
# updated: 07 Mar 2026
#

'''This is the Semaphore implementaion class.'''
class Semaphore(object):


##########################################
#Constructor


    def __init__(self, n, simKernel):
        ''' use as provided.
            - n is the number to set the Semaphore counter to initially
            - simKernel provides the access to the simulated kernel a real OS
                 would have when constructing a Semaphore
            This constructor will run once when the OS invokes it.
        '''
        
        # Reference to the simulated OS kernel so we can use its services
        # such as queues, locks, and waking sleeping processes.
        self.OS = simKernel

        # Semaphore counter. This represents how many processes
        # are allowed to enter the critical section. In our lab the
        # semaphore is initialized to 1.
        self.count = n

        # Queue used to store the names of processes that must wait
        # because the semaphore counter became negative.
        self.queue = self.OS.getQueue()

        # Atomic lock used to guarantee that updates to the semaphore
        # counter and queue happen atomically (preventing race conditions
        # between concurrent wait() and signal() calls).
        self.lock = self.OS.getAtomicLock()


##########################################
#Instance Methods



    def wait(self, caller):
        ''' semaphore wait functionality.
            - caller is the process asking "wait?"
              (you will need caller because this is a simulated system,
               a production OS has this info available as part of the PCB)'''
        
        # Acquire the atomic lock to safely update the counter.
        self.lock.acquire(caller)

        # Decrement the semaphore counter
        self.count -= 1

        # If the counter becomes negative, this means the critical
        # section is already occupied and the calling process must wait.
        if self.count < 0:

            # Place the process name in the semaphore waiting queue.
            # This simulates the OS placing the process in a wait list.
            self.queue.put(caller.getName())

            # Release the lock before blocking so other processes
            # can access the semaphore.
            self.lock.release(caller)

            # Put the calling process to sleep until another process
            # performs a signal() and wakes it.
            caller.sleep()
        else:

            # If the counter is still >= 0, the process can continue
            # into the critical section, so we release the lock.
            self.lock.release(caller)




    def signal(self, caller):
        ''' semaphore signal functionality.
            - caller is the process providing the "signal"
              (you will need caller because this is a simulated system,
               a production OS has this info available as part of the PCB)'''
        
        # Acquire the atomic lock to safely update the counter.
        self.lock.acquire(caller)

        # Increment the semaphore counter to indicate that the
        # critical section has been released.
        self.count += 1

        # If the counter is <= 0, there are processes waiting
        # in the semaphore queue.
        if self.count <= 0:

            # Remove one waiting process from the queue.
            process_name = self.queue.get()

            # Wake that process so it can continue execution.
            self.OS.wake(process_name)

        # Release the lock so other processes can access the semaphore.
        self.lock.release(caller)










