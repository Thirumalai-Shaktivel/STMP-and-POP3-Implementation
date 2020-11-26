#!/usr/bin/env python2

#A03. Implement POP3 protocol

#Importing Required modules
import argparse
from socket import *
import sys

SIZE = 2048

def main():

#Parser for command-line options and arguments 
    parser = argparse.ArgumentParser()
#Type "python2 G22.py --help", to get clear vision of this
    parser.add_argument("-u", help = "Username in the host", type=str)
    parser.add_argument("-p", help = "Password for the above mentioned Username", type=str)
    parser.add_argument("-s", help = "Server IP address >> If you Don't know what to give as input, just type \"localhost\"", type=str)
    
    args = parser.parse_args()
# Check for No inputs
    if(not args.u or not args.p or not args.s):
        print "Usage: python2 ./asn1.py -u <username> -p <password> -s <POP3 server>"
        sys.exit();
#Calling POP3 Function.
    print "\n>> Connecting to the Mail Server...\n"
    pop3(args.u, args.p, args.s)
    return 0

##################################################################
# Pop3 Function
def pop3(userName, passWord, ipAddr):
# Port 110 - this is the default POP3 non-encrypted port   
    portNumber = 110
# Create socket called clientSocket
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((ipAddr, portNumber))
    Rec = clientSocket.recv(SIZE)
    print '  ' + Rec,
#Login Authentication by inputing the username and password
    userInput = 'USER ' + userName + '\r\n'
    print userInput,
    clientSocket.send(userInput)
    Rec = clientSocket.recv(SIZE)
    print '  ' + Rec,
    
    userPassword = 'PASS ' + passWord + '\r\n'
    print userPassword,
    clientSocket.send(userPassword)
    Rec = clientSocket.recv(SIZE)
    rec = Rec.split(" ")
    if(rec[0] == '-ERR'):
        print "\nLogin Failed!! Type the UserName and Password correctly\n"
        sys.exit()
    print ">> Authentication Successful!!"
    print '  ' + Rec

#Keep a count on how many mail received
    stat = 'STAT\r\n'
    clientSocket.send(stat)
    Rec = clientSocket.recv(SIZE).split(" ")
    lastMail = Rec[1]
#No Mail recieved then Exit    
    if(not int(lastMail)):
        print ">> No Mail for " + userName
        quit = 'QUIT\r\n'
        print quit,
        clientSocket.send(quit)
        Rec = clientSocket.recv(SIZE)
        print '  ' + Rec,
    
        print ">> Closing the Connection..."
        clientSocket.close()
        return

#list All the Mails Received
    print ">> Displaying the Mails Recieved!!\n"
    display = 'LIST\r\n'
    print display,
    clientSocket.send(display)
    Rec = clientSocket.recv(SIZE)
    print '  ' + Rec
     
    print ">> Deleting the First Mail..."
    delFirst = 'DELE 1\r\n'
    print delFirst,
    clientSocket.send(delFirst)
    Rec = clientSocket.recv(SIZE)
    print '  ' + Rec

#Checking for more than 1 mail
    if (int(lastMail) > 1):
        print ">> Deleting the Last Mail..."
        delLast = 'DELE ' + lastMail + '\r\n'
        print delLast,
        clientSocket.send(delLast)
        Rec = clientSocket.recv(SIZE)
        print '  ' + Rec
#Checking for more than 2 mail
    if (int(lastMail) > 2):
        print ">> Displaying the Mail after the Deletion\n"
        display = 'LIST\r\n'
        print display,
        clientSocket.send(display)
        Rec = clientSocket.recv(SIZE)
        print '  ' + Rec,
    else:
        print ">> Mailbox is Empty!!"
        print ">> No more Mail for " + userName + '\n'

#Quit to Disconnect and terminate the Connection
    quit = 'QUIT\r\n'
    print quit,
    clientSocket.send(quit)
    Rec = clientSocket.recv(SIZE)
    print '  ' + Rec,

# Close the port
    print ">> Closing the Connection..."
    clientSocket.close()
    return

if __name__ == "__main__":
    sys.exit(main())
