#====================================================
#  Networks & Security Assignment -- Part II, v1.0  #
#  Jason Tsimplis, 28-11-2017, University of Derby  #
#====================================================

#___________________________..:: NOTE ::..___________________________#
# Both Multiplexing and Multi-Threading have been implemented        #  
# as well as a good amount of Error/Exception Handling. IP Address   #
# is an input from the user, to make things easier and offer better  #
# compatibility, in case clients are on different physical machines. #
# Output from server has been removed according to the specification # 
# of the assignment, except some error handling/exception messages.  #
#--------------------------------------------------------------------#

import threading
import socket
import select
import random
import re
import time

#Messages
HELLO_MSG = "Hello\r\n"
GAME_MSG = "Game\r\n"
GREETINGS_MSG = "Greetings\r\n"
ADMIN_GREETINGS_MSG = "Admin-Greetings\r\n"
READY_MSG = "Ready\r\n"
FAR_MSG = "Far\r\n"
CLOSE_MSG = "Close\r\n"
CORRECT_MSG = "Correct\r\n"
WHO_MSG = "Who\r\n"

admin = False           #flag used in the message handler
connections = []        #list of active connections
admin_connections = []  #list of admin connections

#Building RegEx for "My Guess is: <int>"
def regexCheck():
    re1='(My)'	# Word 1
    re2='(\\s+)'	# White Space 1
    re3='(Guess)'	# Word 2
    re4='(\\s+)'	# White Space 2
    re5='(is)'	# Word 3
    re6='(:)'	# Any Single Character 1
    re7='(\\s+)'	# White Space 3
    re8='(\\d+)'	# Integer Number 1
    regex = re.compile(re1+re2+re3+re4+re5+re6+re7+re8)
    return regex


#Generates a random number
def generateNumber():
    return random.randint(1,30)



#Main Message transmission handler
def clientHandler(admin, conn, addr):
    if not (admin):
        number = generateNumber()

    while (True):
        #Error Handling - In case of connection drop or OS error.
        try:
            recvData = conn.recv(2048).decode()
        except:
            print("\n[x] Connection Closed\n")
            if not (admin):
                connections.remove(conn)
            else:
                admin_connections.remove(conn)
            conn.close()
            break
        
        #Server response according to type of message received
        if (recvData == HELLO_MSG):
            if (admin == False):
                conn.send(GREETINGS_MSG.encode())
            else:
                conn.send(ADMIN_GREETINGS_MSG.encode())
 
        elif (recvData == WHO_MSG):
            for data in connections:
                if ((data != adminserver_socket) and (data != clientserver_socket)):
                    conn.send((str(data.getpeername()[0])+" "+str(data.getpeername()[1])+"\r\n").encode())
            admin_connections.remove(conn)
            conn.close()
            break
    
        elif (recvData == GAME_MSG):
            conn.send(READY_MSG.encode())
                  
        elif (regexCheck().match(recvData)):
            for char in (recvData.split()):
                if (char.isdigit()):
                    guess = int(char)
                    break
            if (guess > number):
                if (abs(number-guess) <= 5 and (abs(number-guess) != 0)):
                    conn.send(CLOSE_MSG.encode())
                else:
                    conn.send(FAR_MSG.encode())
            elif (guess < number):
                if (abs(number-guess) <= 5 and (abs(number-guess) != 0)):
                    conn.send(CLOSE_MSG.encode())
                else:
                    conn.send(FAR_MSG.encode())
            else:
                conn.send(CORRECT_MSG.encode())
                connections.remove(conn)
                conn.close()
                break
        else:
            print("[x] Communication Protocol Violation !!")



#Server Sockets Initialization - Program Start
clientserver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
adminserver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    clientserver_socket.bind((socket.gethostbyname(socket.gethostname()),4000))
    adminserver_socket.bind((socket.gethostbyname(socket.gethostname()), 4001))
except (OSError):
    print("\n[x] Invalid server initialization. Try again...\n")
else:
    clientserver_socket.listen(5)
    adminserver_socket.listen(2)
    connections.append(clientserver_socket)
    connections.append(adminserver_socket)
    print("Waiting...")



#Main Program Loop
while (True):
            #Mutliplexing used to determine if socket is an admin socket or not.
            (read, write, error) = select.select(connections, [], [])
            for data in read:
                if (data is clientserver_socket):
                    (conn,addr)=clientserver_socket.accept()
                    connections.append(conn)
                    admin = False
                    threading.Thread(target = clientHandler, args = (admin, conn, addr)).start()
                
                elif (data is adminserver_socket):
                    (conn,addr)=adminserver_socket.accept()
                    admin_connections.append(conn)
                    admin = True
                    threading.Thread(target = clientHandler, args = (admin, conn, addr)).start()