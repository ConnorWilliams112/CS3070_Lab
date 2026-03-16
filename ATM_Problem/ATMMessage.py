#
# ATMMessage.py
# CS3070 
#
# Authors: Montes - Papakostas - Sami - Williams
# created: Spring '16
# updated: 16 Mar 2022


TRANSACTION = 'transaction'
BALANCE = 'balance'
SHUTDOWN = 'shutdown'


''' ATM messages are just strings formatted as an "operation amount" pair
this class provides utility functions to generate and parse these messages
'''
class ATMMessage(object):

    @staticmethod
    def wrap(operation, amount):
        '''takes an operation & amount, then makes the message string'''
        return str(operation) + ' ' + str(amount)
                
        

    @staticmethod
    def unwrap(message):
        '''parses the message string into a 2-tuple of properly type
           converted components: (string, integer) '''
        pair = message.split()
        operation = pair[0]
        amount = int(pair[1])
        return(operation, amount)




