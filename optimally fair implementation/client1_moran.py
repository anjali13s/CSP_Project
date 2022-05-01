import socket
from random import randint

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233

def Convert(string):
    list1=[]
    list1[:0]=string
    return list1

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

Response = ClientSocket.recv(1024)
print(Response.decode('utf-8'))

ClientSocket.send(str.encode('Hello from Party 1'))
Response = ClientSocket.recv(1024)
print(Response.decode('utf-8'))
data1 = ClientSocket.recv(4096)
ClientSocket.send('OK'.encode())
data2 = ClientSocket.recv(4096)
ClientSocket.send('OK'.encode())
num1 = ClientSocket.recv(1024)
ClientSocket.send('OK'.encode())
data3 = ClientSocket.recv(4096)

x1 = []
y1 = []
x2 = []

data1 = data1.decode('utf-8')
for i in range(len(data1)):
    if(data1[i]!= ' ' and data1[i]!= ',' and data1[i]!= '[' and data1[i]!= ']' ):
        x1.append(int(data1[i]))
print(x1)
 


# Convert decoded data into list

data2 = data2.decode('utf-8')
for i in range(len(data2)):
    if(data2[i]!= ' ' and data2[i]!= ',' and data2[i]!= '[' and data2[i]!= ']' ):
        y1.append(int(data2[i]))
print(y1)


data3 = data3.decode('utf-8')
for i in range(len(data3)):
    if(data3[i]!= ' ' and data3[i]!= ',' and data3[i]!= '[' and data3[i]!= ']' ):
        x2.append(int(data3[i]))
print(x2)

strings1 = num1.decode('utf8')
#get the num
r = int(strings1)

print("x1 = ", x1, "y1 = ", y1, "x2 = ", x2, "r = ",r)

print(len(x1), len(x2), len(y1))
a = []


for i in range(r):
    x = x1[i]^x2[i]
    a.append(x)

print("a = ", a)

ClientSocket.close()

