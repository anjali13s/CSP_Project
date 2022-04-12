import socket, sys
from random import randint


clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP = '127.0.0.1'
PORT = 5545

# connect to the server
clientsocket.connect( (IP, PORT) )


# ---------------------------------SEQUENCE BEGINS-------------------------------------------

# wait for intro message
print(clientsocket.recv(1024).decode())   # --> returns a string

# send back an OK response to proceed with the sequence
clientsocket.send('OK'.encode())

number = clientsocket.recv(1024) #recieve n
print(number)
strings = str(number, 'utf8')
#get the n
n = int(strings)
print("n = ", n)

x = randint(1, n-1)
print("\nx = ", x)

a = (x**2)%n
print("\na =", a )
clientsocket.send(bytes(str(a), 'utf8'))  # send a to server


print('\n\nEnter your key: ',end='')
    # ask user for the key to be used in cipher
key = input()
clientsocket.send(key.encode()) #send key to server

print()

print("Your encrypted message is : ")
print(clientsocket.recv(1024).decode()) #recieve encrypted message
print("Thank you for using Caesar cipher")

