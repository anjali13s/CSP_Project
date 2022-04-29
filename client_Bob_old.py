import socket, sys
from random import randint


clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP = '127.0.0.1'
PORT = 5545

# connect to the server
clientsocket.connect( (IP, PORT) )

def gcdExtended(a, b): 
    # Base Case 
    if a == 0 :  
        return b,0,1
             
    gcd,x1,y1 = gcdExtended(b%a, a) 
     
    # Update x and y using results of recursive 
    # call 
    x = y1 - (b//a) * x1 
    y = x1 
     
    return gcd,x,y


# ---------------------------------SEQUENCE BEGINS-------------------------------------------

# wait for intro message
print(clientsocket.recv(1024).decode())   # --> returns a string

# send back an OK response to proceed with the sequence
clientsocket.send('OK'.encode())

number = clientsocket.recv(1024) #recieve n
#print(number)
strings = str(number, 'utf8')
#get the n
n = int(strings)
print("n = ", n)

x = randint(1, n-1) #randomly choose x from 1 to n-1
while(True):
    if(x%n == 0):   #ensure x is relatively prime to n (otherwise Alice can get roots easily)
        x = randint(1, n-1) 

    else:    
        break
print("\nx = ", x)

a = (x**2)%n #create a = x^2modn
print("\na =", a )
clientsocket.send(bytes(str(a), 'utf8'))  # send a to Alice

number2 = clientsocket.recv(1024) #recieve Alice's guess
strings2 = str(number2, 'utf8')
#get the guess
guess = int(strings2)
print("\nAlice's guess = ", guess)

if(guess == x or guess == (n-x)): #if guess is equal to x or n-x
    print("\nAlice wins")
    clientsocket.send('You win'.encode()) #send result
    number3 = clientsocket.recv(1024) #recieve p
    strings3 = str(number3, 'utf8')
    #get p
    p = int(strings3)
    clientsocket.send('OK'.encode()) #send ok to move to next code
    number4 = clientsocket.recv(1024) #recieve q
    strings4 = str(number4, 'utf8')
    #get p
    q = int(strings4)
    print("Alice tells that p = ",p, "q = ",q)

else:
    print("\nAlice lost")    
    clientsocket.send('You lost'.encode()) #send result
    gcd_p = gcdExtended((guess-x),n) #using Alice's guess and your x and n find p
    gcd_q = gcdExtended((guess+x),n) #using Alice's guess and your x and n find q
    #print(gcd_p[:1], gcd_q[:1])
    gcd_p1 = [ int(x) for x in gcd_p ]
    gcd_q1 = [ int(x) for x in gcd_q ]

    if(gcd_p1[0] < 0):
        p = -1*int(gcd_p1[0]) #convert p into its positive counterpart

    else: p = int(gcd_p1[0])  
    if(gcd_q1[0]<0):
        q = -1*int(gcd_q1[0]) #convert q into its positive counterpart

    else: q = int(gcd_q1[0])

    print("You found p = ",p, "q = ",q) 
    
    clientsocket.send(bytes(str(p), 'utf8')) #send your p to show that you know n's factors and that you win
    if clientsocket.recv(1024).decode() == 'OK': #send ok to move to next code
        clientsocket.send(bytes(str(q), 'utf8')) #send your q to show that you know n's factors and that you win


print()

print("Thank you for using coin flipping by telephone")

