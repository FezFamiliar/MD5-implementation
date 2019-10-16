#!/usr/bin/python
from bitarray import bitarray




def F(x, y, z):
    return x & y | (~x & z)

def G(x, y, z):
    return x & z | (y & ~z)

def H(x, y, z):
    return x ^ y ^ z

def I(x, y, z):
    return y ^ (x | ~z)

'''

P = [  Message   |     Padding     |  Message length ]
    |<- b  bits->|<-- ??? bits --->|<--- 64 bits --->|

'''
def padding(msg):  
    msg_array = bitarray(endian='big')
    msg_array.frombytes(msg.encode('ascii'))

    msg_array.append(1)
    while len(msg_array) % 512 != 448:
        msg_array.append(0)

    bitarray(msg_array,endian='little')
    message_length = '{:064b}'.format(len(msg) % pow(2,64))
    msg_array.extend(message_length)

    return len(msg_array)
    

message = 'fox'
print(padding(message))