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

   
    
    n_length = 20 #length of p and q

    #function to get random primes
    while(True):
        p = number.getPrime(n_length, os.urandom) #getting p
        #print(p)
        if(p%4 != 3): #ensuring p is of the form 3mod4
            p = number.getPrime(n_length, os.urandom)
        else:    
            break

    while(True):
        q = number.getPrime(n_length, os.urandom) #getting q
        #print(q)
        if(q%4 != 3 or q == p): #ensuring q is of the form 3mod4 and not equal to p
            q = number.getPrime(n_length, os.urandom)

        else:    
            break    

    
    print("p = ",p,"q = ",q)


    n = p*q

    print("n = ", n)

    clientsocket.send(bytes(str(n), 'utf8')) #send n to Bob

    number1 = clientsocket.recv(1024) #recieve a
    strings = str(number1, 'utf8')
    #get the a
    a = int(strings)
    print("a = ",a)
   

    k_1 = (p-3)/4 #finding out value of k to find value of a^k+1 using p
    k_2 = (q-3)/4 #finding out value of k to find value of a^k+1 using q
 
    s1 = findRoot(k_1+1, p, a) #solution will help in finding final roots
    #print("root1 = ", s1)
    s2 = findRoot(k_2+1, q, a) #solution will help in finding final roots
    #print("root2 = ", s2)

    a1 , b1 = findalphabeta(p, q) #finding value of alpha, beta to find final roots
    #print(a1, b1)
    term1 = s2*b1*p 
    term2 = s1*a1*q
    r1 = term1 + term2 
    r2 = term1 - term2
    #print(term1, term2)
    root1 = r1%n #first root
    root2 = r2%n #second root
    root3 = (-1*r1)%n #third root
    root4 = (-1*r2)%n #fourth root
    roots = []
    print("Roots are ", root1, ",", root2, ",", root3, ",", root4)
    roots.append(root1)
    roots.append(root2)
    roots.append(root3)
    roots.append(root4)
    #print("roots = ",roots)

    guess = random.choice(roots) #choose a random choice out of the four roots
    print("Your guess = ", guess)
    
    clientsocket.send(bytes(str(guess), 'utf8')) #send your guess
    
    result = clientsocket.recv(1024).decode() #receive result, if you won or lost
    print(result)

    if(result == 'You win'):
        num1 = clientsocket.recv(1024) #recieve Bob's random choice of x
        str1 = str(num1, 'utf8')
        #get x
        x = int(str1) 
        print("Bob tells that x was", x)
        clientsocket.send(bytes(str(p), 'utf8')) #send p for Bob to check
        if clientsocket.recv(1024).decode() == 'OK': #recieve ok to move to next code
            clientsocket.send(bytes(str(q), 'utf8')) #send q for Bob to check
       
    elif(result == 'You lost'):  
        num1 = clientsocket.recv(1024) #recieve Bob's random choice of x
        str1 = str(num1, 'utf8')
        #get x
        x = int(str1) 
        print("Bob tells that x was", x)
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




def binaryform(k): #function to convert given k+1 to a binary expansion of the form b_m.2^m + b_m-1.2^m-1.... +b_0
    arr = []
    while(True):
        i = k%2
        arr.append(int(i)) #would always be either 0 or 1
        k = k//2           #dividing by 2 and using quotient as dividend for next step like Euclidean algorithm
        #print(k)

        if(k==0):
            break

    #print("binary = ", arr)
    return arr

def multiplyList(myList) : #function to multiply the two lists of coefficients and a^2xmodp
     
    # Multiply elements one by one
    result = 1
    for x in myList:
         result = result * x
    return result

def findRoot(k, p, n): #function to find the 1st solution using the binary expansion
    arr = []
    arr = binaryform(k)
    mod = []
    i=0
    while(True):
        m = n%p #finding amodp
        mod.append(int(m))
        n = m**2 #to find a^2, a^4...
        i=i+1
        if(2*i>k-1):
            break
   
    #print("coef = ", mod)
    products = []
    for num1, num2 in zip(arr, mod): #multiplying coefficient with a^2xmodp
	    products.append(num1*num2)
    
    #print("products = ", products)    
    
    products =  [i for i in products if i!=0] #removing any 0s
               

    #print("products = ", products)   
    #print("final = ", multiplyList(products))
    s = multiplyList(products) #multiplying the elements together
    root = s%p #smodp gives the first solution
    return root

 

def findalphabeta(r1, r2): #function to find alpha and beta to find roots
    alpha = []
    beta = []
    q = []
    alpha.append(1)
    beta.append(0)
    alpha.append(0)
    beta.append(1)

    while(True):
        q.append(r2//r1) #saving the quotients in an array
        temp = r1
        r1 = r2%r1       #taking the remainder as next divisor for Euclidean algorithm
        r2 = temp        #taking the quotient as next dividend
        #print("r1 = ", r1, "r2 = ", r2)
        if r1 == 1:      #stop when divisor becomes 1
            break
    #print("q = ", q)


    for i in range(1, len(q)+1): #using formula
        al = alpha[i-1] - q[i-1]*alpha[i]
        alpha.append(al)

    for i in range(1, len(q)+1):
        be = beta[i-1] - q[i-1]*beta[i]
        beta.append(be)

    #print("alpha = ", alpha)
    #print("beta = ", beta)

    i = len(alpha)-1
    j = len(beta)-1
    #print("al = ", alpha[i], "be = ", beta[j])
    return alpha[i], beta[j]            #returning final value of alpha and beta


   

while True:

    # wait until a client connects
    (clientsocket, address) = serversocket.accept() #--> returns (clientsocket, address)

    # we won't reach this point until a client connects
    
    # call the "handle_new_client" function to interact with the client
    new_encryption(clientsocket,address)

    clientsocket.close()    # close the connection and start the next iteration of the loop to wait for the next client





print('The server is going down!')
serversocket.close()    # close down the server
