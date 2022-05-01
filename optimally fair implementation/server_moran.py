import socket
import os
from _thread import *
from random import randint

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
ServerSocket.listen(5)

n = 20
r = randint(2, n-1)
i_i = randint(3, r)
w = randint(0, 1)
print("r = ", r, "i* = ", i_i, "w = ", w)
a = []
b = []
x1 = []
y1 = []
x2 = []
y2 = []
for i in range(0, i_i - 1):
    a.append(randint(0,1))
    b.append(randint(0,1))

for i in range(i_i, r+1):
    a.append(w)
    b.append(w)

print("a = ", a, "b = ", b)
print(len(a), len(b))

for i in range(0, r):
    x1.append(randint(0,1))
    y1.append(randint(0,1))

for i in range(0, r):
    x = x1[i]^a[i]
    x2.append(x)
    y = y1[i]^b[i]
    y2.append(y)

print("x = ", x1, "\ny = ", y1, "\nx' = ", x2, "\ny' = ", y2 )
    

def threaded_client(connection):
    connection.send(str.encode('Welcome to optimally fair coin tossing!'))
    
    data = connection.recv(2048)
    print(data.decode('utf-8'))

    
    while True:
        connection.sendall(str.encode('Let us start'))

        if ThreadCount == 1:

            connection.send(str(x1).encode('utf8'))
            if connection.recv(1024).decode() == 'OK':
                connection.send(str(y1).encode('utf8'))
                if connection.recv(1024).decode() == 'OK':
                    connection.send(str(r).encode('utf8'))
                    if connection.recv(1024).decode() == 'OK':
                        connection.send(str(x2).encode('utf8'))

        if ThreadCount == 2:
            connection.send(str(x2).encode('utf8'))
            if connection.recv(1024).decode() == 'OK':
                connection.send(str(y2).encode('utf8'))
                if connection.recv(1024).decode() == 'OK':
                    connection.send(str(r).encode('utf8'))   
                    if connection.recv(1024).decode() == 'OK':
                        connection.send(str(y1).encode('utf8'))

         
        
    connection.close()

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()

