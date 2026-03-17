#
# ATM.py
# CS3070 Synchronization Lab series 
#
# Authors: Montes - Papakostas - Sami - Williams
# created: Spring '16
# updated: 16 Mar 2022



import random
import time
import multiprocessing as mp

import SL_Kernel as Kernel
from ATMMessage import *


'''The ATM client objects '''
class ATM(mp.Process):


##########################################
#Constructor

    def __init__(self, cName, pName, seed, atm_connection):

        super().__init__(target=self.execute, args='' )
        
        self.atm_connection = atm_connection

        self.transactionTotal = 0
        
        self.clientName = cName
        self.name = pName
        self.again = True
        #random.seed(seed)




##########################################
#Instance Methods


    def execute(self):
        '''this is the function which serves as the processes "Run loop" '''
        

        while self.again:

            if self.__delayToNextTransaction__() == SHUTDOWN:
                break

            #select deposit or withdrawal amount
            transactionAmount = int( random.random() * 300)

            # Protocol (delta legend):
            #  - transactionAmount > 0 : deposit
            #  - transactionAmount < 0 : withdrawal
            #  - transactionAmount == 0: balance inquiry
            # Client sends one `TRANSACTION` message carrying this delta.
            # The server applies the delta inside a semaphore-protected
            # critical section and replies once with `BALANCE`.

            pull = random.random()
            if pull < 0.2:     #check balance
                transactionAmount = 0

            else:
                if pull < 0.6:   #withdrawal
                    transactionAmount = -transactionAmount
                else:            #deposit
                    pass

            # send a single transaction request (delta) and receive the new balance
            self.atm_connection.send( ATMMessage.wrap(TRANSACTION, transactionAmount) )
            balance = self.__recieveBalance__()

            self.transactionTotal += transactionAmount

            if balance == SHUTDOWN :
                break

            if transactionAmount != 0:
                print ( self.clientName + ' transaction for: ' + str(transactionAmount) + ', balance of: ' + str(balance) + '\n', end = ''  )
            else:
                print ( self.clientName + ' balance inquiry: ' + str(balance) + '\n', end = ''  )

        print('   ATM machine', self.clientName, 'shutting down; transaction total was:', self.transactionTotal )
        
        
 
    def __recieveBalance__(self):
        '''returns EXIT to indicate a shutdown was recieved, returns the balance otherwise'''
        message = self.atm_connection.recv()

        if message == SHUTDOWN:
            self.__stop__()
            return SHUTDOWN
        
        else:
            (operation, amount) = ATMMessage.unwrap(message)
            if operation == BALANCE:
                balance = amount
                return balance
                
            else:
                raise RuntimeError(operation + 'is not a return balance account operation')                    




    def __stop__(self):
        self.again = False




    def __didWeRecieveShutdownMsg__(self):
        '''return True if we did, False if not.'''
        msg = False
        if self.atm_connection.poll():
            msg = self.atm_connection.recv()
            if msg == SHUTDOWN:
                return True
            else:
                raise RuntimeError(msg + 'is not a shutdown so it is recvieved out of order')                    
                
        return False




    def __delayToNextTransaction__(self):
        ''' simulated queuing delays to allow the user take care of other business, process sleeps during delay.

            Interactions with SHUTDOWN messages that are affected by or affect the delay state are handled,
            returns ATM.EXIT if a SHUTDOWN is ordered prior to completing the delay for other business. '''

        if self.__didWeRecieveShutdownMsg__():
            return SHUTDOWN
        else:
            time.sleep( random.random() * 0.2 )   #0 to 2-tenths of a second

        if self.__didWeRecieveShutdownMsg__():
            return SHUTDOWN
        
        return None




