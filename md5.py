#!/usr/bin/python
from bitarray import bitarray
import binascii,math

T = [int(2**32 * abs(math.sin(i))) for i in range(64)]


rotate_amounts = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                  5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
                  4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                  6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

init_buffer = [0x01234567,0x89abcdef,0xfedcba98,0x76543210]

BITS = 32
message = 'fox'



def F(x, y, z):
    return x & y | (~x & z)

def G(x, y, z):
    return x & z | (y & ~z)

def H(x, y, z):
    return x ^ y ^ z

def I(x, y, z):
    return y ^ (x | ~z)

def left_rotate(value,amount):
    return (value << amount) | (value >> (BITS - amount))

def padding(msg):  
    msg_array = bitarray(endian='big')
    msg_array.frombytes(msg.encode('ascii'))

    msg_array.append(1)
    while len(msg_array) % 512 != 448:
        msg_array.append(0)

    bitarray(msg_array,endian='little')
    message_length = '{:064b}'.format(len(msg) % pow(2,64))
    msg_array.extend(message_length)

    return msg_array
    




def md5(msg):
    step  = 32
    M = [None] * 16

    for i in range(0,len(padding(msg)),step):
        M[int(i/step)] = padding(msg)[i:i+step]
    
    a, b, c, d = init_buffer
    for r1 in range(16):
        print(M[r1])
        #print(left_rotate((a + F(b,c,d) + M[r1] + T[r1]),rotate_amounts[r1]))
       # a = b + (left_rotate((a + F(b,c,d) + M[r1] + T[r1]),rotate_amounts[r1]))  
    for r2 in range(16,32):
        pass
      #  a = b + (left_rotate((a + G(b,c,d) + M[r2] + T[r2]),rotate_amounts[r2]))  
    for r3 in range(32,48):
        pass
      #  a = b + (left_rotate((a + H(b,c,d) + M[r3] + T[r3]),rotate_amounts[r3]))  
    for r4 in range(48,64):
        pass
       # a = b + (left_rotate((a + I(b,c,d) + M[r4] + T[r4]),rotate_amounts[r4])) 
 



md5(message)



