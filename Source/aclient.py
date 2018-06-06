#===================================================#
#  Network & Security Assignment -- Part ΙI, v1.0   #
#  Jason Tsimplis, 28-11-2017, University of Derby  #
#===================================================#

import socket
import re

#Messages
ADMIN_GREETINGS_MSG = "Admin-Greetings\r\n"
WHO_MSG = "Who\r\n"
HELLO_MSG = "Hello\r\n"
output = ""

#Building Regular Expression for "IP-Adress Port-Number">
def regexCheck():
    re1='(\\d+)'	# Integer Number 1
    re2='(\\.)'	# Any Single Character 1
    re3='(\\d+)'	# Integer Number 2
    re4='(\\.)'	# Any Single Character 2
    re5='(\\d+)'	# Integer Number 3
    re6='(\\.)'	# Any Single Character 3
    re7='(\\d+)'	# Integer Number 4
    re8='(\\s+)'	# White Space 1
    re9='(\\d+)'	# Integer Number 5
    regex = re.compile(re1+re2+re3+re4+re5+re6+re7+re8+re9)
    return regex


#User input - Validation loop
while(True):
    print(">> Enter your destination IP:")
    print("-----------------------------")
    print("Access Privilege: ADMIN")
    print("Destination PORT: 4001")
    ip = input("Destination IP: ")
    port = 4001
    print()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Error Handling in case of invalid connection or OS error.
    try:
        s.connect((ip, int(port)))
    except (ConnectionRefusedError, ConnectionAbortedError, TimeoutError, ConnectionResetError, ConnectionError, OSError, ValueError):
        print("\n[x] Connection Failed. Try again...\n")
    else:
        break

print(">> Connected to:", ip, port)
print("---------------------------------------")
s.send(HELLO_MSG.encode())


while(True):
    #Error Handling in case of dropped connection or OS error.
    try:
        recvData = s.recv(2048).decode()
    except:
        s.close()
        break

    if (recvData == ADMIN_GREETINGS_MSG):
        s.send(WHO_MSG.encode())
        print("The players currently playing are:")
    elif (regexCheck().match(recvData)):
            output = output+recvData
    else:
        print(output)
        print()
        break
s.close()

#Optional keyboard input to control the termination of the program.
input(">> Connection Closed. Hit 'Enter' to exit...") 