#!/usr/bin/python
from bitarray import bitarray
import binascii,math

T = [int(2**32 * abs(math.sin(i))) for i in range(64)]



rotate_r1 = [7, 12, 17, 22]
rotate_r2 = [5,  9, 14, 20]
rotate_r3 = [4, 11, 16, 23]
rotate_r4 = [6, 10, 15, 21]

init_buffer = [0x01234567,0x89abcdef,0xfedcba98,0x76543210]

BITS = 32




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

def modulo_addition(a, b):
    return ((a + b) % pow(2,32))

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

    M = [int.from_bytes(word.tobytes(), byteorder="little") for word in M]
    a, b, c, d = init_buffer
    for r1 in range(16):
        aux = modulo_addition(a,F(b,c,d))
        aux = modulo_addition(aux,M[r1 % 16])
        aux = modulo_addition(aux,T[r1])
        aux = left_rotate(aux,rotate_r1[r1 % 4])
        aux = modulo_addition(aux,b)
        a = d
        d = c
        c = b
        b = aux

    for r2 in range(16,32):
        aux = modulo_addition(a,G(b,c,d))
        aux = modulo_addition(aux,M[r2 % 16])
        aux = modulo_addition(aux,T[r2])
        aux = left_rotate(aux,rotate_r2[r2 % 4])
        aux = modulo_addition(aux,b)
        a = d
        d = c
        c = b
        b = aux
 
    for r3 in range(32,48):
        aux = modulo_addition(a,H(b,c,d))
        aux = modulo_addition(aux,M[r3 % 16])
        aux = modulo_addition(aux,T[r3])
        aux = left_rotate(aux,rotate_r3[r3 % 4])
        aux = modulo_addition(aux,b)
        a = d
        d = c
        c = b
        b = aux
     
    for r4 in range(48,64):
        aux = modulo_addition(a,I(b,c,d))
        aux = modulo_addition(aux,M[r4 % 16])
        aux = modulo_addition(aux,T[r4])
        aux = left_rotate(aux,rotate_r4[r4 % 4])
        aux = modulo_addition(aux,b)
        a = d
        d = c
        c = b
        b = aux

    return format(a,'0x') + format(b, '0x') + format(c, '0x') + format(d, '0x')
   


message = 'fox'
print(md5(message))



