import socket

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

ClientSocket.send(str.encode('Hello from Party 2'))
Response = ClientSocket.recv(1024)
print(Response.decode('utf-8'))
data1 = ClientSocket.recv(4096)
ClientSocket.send('OK'.encode())
data2 = ClientSocket.recv(4096)
ClientSocket.send('OK'.encode())
num1 = ClientSocket.recv(1024)
ClientSocket.send('OK'.encode())
data3 = ClientSocket.recv(4096)

x2 = []
y2 = []
y1 = []

data1 = data1.decode('utf-8')
for i in range(len(data1)):
    if(data1[i]!= ' ' and data1[i]!= ',' and data1[i]!= '[' and data1[i]!= ']' ):
        x2.append(int(data1[i]))
print(x2)
 


# Convert decoded data into list

data2 = data2.decode('utf-8')
for i in range(len(data2)):
    if(data2[i]!= ' ' and data2[i]!= ',' and data2[i]!= '[' and data2[i]!= ']' ):
        y2.append(int(data2[i]))
print(y2)


data3 = data3.decode('utf-8')
for i in range(len(data3)):
    if(data3[i]!= ' ' and data3[i]!= ',' and data3[i]!= '[' and data3[i]!= ']' ):
        y1.append(int(data3[i]))
print(y1)

strings1 = num1.decode('utf8')
#get the num
r = int(strings1)

print("x2 = ", x2, "y2 = ", y2, "y1 = ", y1, "r = ",r)

#print(len(x2), len(x1), len(y2))
b = []


for i in range(r):
    y = y1[i]^y2[i]
    b.append(y)

print("b = ", b)

ClientSocket.close()

