import socket, sys, threading, string
from Crypto.Util import number
import random


# instantiate server's socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# define address params
IP = '127.0.0.1'
PORT = 5545
ThreadCount = 0

# bind server
try:
    serversocket.bind( (IP, PORT) )
except socket.error as e:
    print(str(e))


# start listening
serversocket.listen()

print('The server is up! Listening at:',IP,PORT)
print()

# ---------------------------------ENCRYPTION BEGINS-------------------------------------------

def new_encryption(clientsocket, address):

    print('-------------------------------------------')
    print('New connection made! Client address:',address)


    # interact with client
    # --------------------------------------------------------------

    # send intro message
    intro = '\nWelcome to coin flipping. Let\'s begin\n'

    clientsocket.send(intro.encode())

    # wait for OK response
    if clientsocket.recv(1024).decode() != 'OK':
        print('Something went wrong! Disconnecting')
        clientsocket.close()

   
    #n_length = 3

    #while(True):
     #   primeNum = number.getPrime(n_length, randFunc)
      #  if(primeNum%3 == 4):
       #     p = primeNum
        #    break

   # while(True):
    #    primeNum = number.getPrime(n_length, randFunc)
     #   if(primeNum%3 == 4 and primeNum!=p):
      #      q = primeNum
       #     break    

    p = 3
    q = 7
    print("p = ", p ," and q = ", q)

    n = p*q

    print("n = ", n)

    clientsocket.send(bytes(str(n), 'utf8'))

    number = clientsocket.recv(1024) #recieve n
    print(number)
    strings = str(number, 'utf8')
    #get the a
    a = int(strings)
    print("a = ",a)
    r1 = a%p
    r2 = a%q
    print ("r1 = ", r1, "and r2 = ", r2)

    array1 = []
    array2 = []
    for i in range (1, n):
        if((i**2)%p == r1):
           array1.append(i)

        if((i**2)%q == r2):
           array2.append(i)  

    print("array1 = ",array1, " and array2 = ",array2)


    
    key = int(clientsocket.recv(1024).decode())
    
    encrypted = cipher_encrypt(input_message, key)
    print(encrypted)
    clientsocket.send(encrypted.encode())
  
  



   

while True:

    # wait until a client connects
    (clientsocket, address) = serversocket.accept() #--> returns (clientsocket, address)

    # we won't reach this point until a client connects
    
    # call the "handle_new_client" function to interact with the client
    new_encryption(clientsocket,address)

    clientsocket.close()    # close the connection and start the next iteration of the loop to wait for the next client





print('The server is going down!')
serversocket.close()    # close down the server
