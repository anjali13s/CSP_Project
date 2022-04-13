import socket, sys, threading, string
from Crypto.Util import number
from Crypto.PublicKey import RSA
import os
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

   
    
    n_length = 10


    while(True):
        p = number.getPrime(n_length, os.urandom)
        print(p)
        if(p%4 != 3):
            p = number.getPrime(n_length, os.urandom)
        else:    
            break

    while(True):
        q = number.getPrime(n_length, os.urandom)
        print(q)
        if(q%4 != 3 or q == p):
            q = number.getPrime(n_length, os.urandom)

        else:    
            break    

    print("p = ",p,"q = ",q)

    #p = 79
    #q = 1
    #print("p = ", p ," and q = ", q)

    n = p*q

    print("n = ", n)

    clientsocket.send(bytes(str(n), 'utf8')) #send n to Bob

    number1 = clientsocket.recv(1024) #recieve a
    strings = str(number1, 'utf8')
    #get the a
    a = int(strings)
    print("a = ",a)
    #finding amodp and amodq to easier find roots of amodn
    r1 = a%p 
    r2 = a%q
    print ("r1 = ", r1, "and r2 = ", r2)

    array1 = [] #array for roots of amodp
    array2 = [] #array for roots of amodq
    for i in range (1, n):
        if((i**2)%p == r1):
           array1.append(i)

        if((i**2)%q == r2):
           array2.append(i)  

    print("array1 = ",array1, " and array2 = ",array2)

    roots = list(common_member(array1, array2)) #find four square roots which are common in amodp and amodq
    print("roots = ",roots)

    guess = random.choice(roots) #choose a random choice out of the four roots
    print("guess = ", guess)
    
    clientsocket.send(bytes(str(guess), 'utf8')) #send your guess
    
    result = clientsocket.recv(1024).decode() #receive result, if you won or lost
    print(result)

    if(result == 'You win'):
        clientsocket.send(bytes(str(p), 'utf8')) #send p for Bob to check
        if clientsocket.recv(1024).decode() == 'OK': #recieve ok to move to next code
            clientsocket.send(bytes(str(q), 'utf8')) #send q for Bob to check
       
    elif(result == 'You lost'):   
        number3 = clientsocket.recv(1024) #recieve Bob's answer of p
        strings3 = str(number3, 'utf8')
        #get p
        p1 = int(strings3)
        clientsocket.send('OK'.encode()) #send ok to move to next code
        number4 = clientsocket.recv(1024) #recieve Bob's answer of q
        strings4 = str(number4, 'utf8')
        #get p
        q1 = int(strings4)
        print("Bob tells that your p and q were",p1,"and",q1)


  
def common_member(a, b):   
        a_set = set(a)
        b_set = set(b)
        
     
        # check length
        if len(a_set.intersection(b_set)) > 0:
            return(a_set.intersection(b_set)) 
        else:
            return("no common elements")




   

while True:

    # wait until a client connects
    (clientsocket, address) = serversocket.accept() #--> returns (clientsocket, address)

    # we won't reach this point until a client connects
    
    # call the "handle_new_client" function to interact with the client
    new_encryption(clientsocket,address)

    clientsocket.close()    # close the connection and start the next iteration of the loop to wait for the next client





print('The server is going down!')
serversocket.close()    # close down the server

