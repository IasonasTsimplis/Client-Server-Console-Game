#===================================================#
#  Network & Security Assignment --- Part I, v1.0   #
#  Jason Tsimplis, 04-11-2017, University of Derby  #
#===================================================#

import socket

HELLO_MSG = "Hello\r\n"
GAME_MSG = "Game\r\n"
GREETINGS_MSG = "Greetings\r\n"
READY_MSG = "Ready\r\n"
GUESS_MSG = "My Guess is: "
FAR_MSG = "Far\r\n"
CLOSE_MSG = "Close\r\n"
CORRECT_MSG = "Correct\r\n"


#User input - Validation loop
while(True):
    print(">> Enter your destination IP:")
    print("-----------------------------")
    print("Access Privilege: USER")
    print("Destination PORT: 4000")
    ip = input("Destination IP: ")
    port = 4000
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
    except (ConnectionRefusedError, ConnectionAbortedError, ConnectionResetError, OSError):
        break

    if (recvData == GREETINGS_MSG):
        s.send(GAME_MSG.encode())

    elif ((recvData == READY_MSG) or (recvData == FAR_MSG) or (recvData == CLOSE_MSG)):
        if (recvData == READY_MSG):
            print("\n>> Welcome to the guess the number game!")
            print("----------------------------------------")
        elif (recvData == FAR_MSG):
            print("You are way off.\n")
        elif (recvData == CLOSE_MSG):
            print("You are close !\n")
        
        #User input validation loop
        while(True):
            guess = input(">> Enter your Guess: ")
            print()
            try:
                guess = int(guess)
            except ValueError:
                print("[x] Invalid input. Use integers only \n")
                continue
            
            #Sending guess to server. Error Handling in case of dropped connection or OS error.
            if ((guess >= 1) and (guess <= 30)):
                try:
                    s.send((GUESS_MSG+str(guess)+"\r\n").encode())
                except (ConnectionError, ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError, OSError):
                    print("[x] Connection Error\n")
                    s.close()
                    break
                else:
                    break                                                   #If message is sent, and no exception was thrown, break from the loop.
            else:
                print("\n[x] Invalid input. Guess between 1 - 30 ** \n")

    elif(recvData == CORRECT_MSG):
        print("You guessed correctly !\n")
        break
s.close()

#Optional keyboard input to control the termination of the program.
input(">> Connection Closed. Hit 'Enter' to exit...") 