#!/usr/bin/env python2

#A02. Implement SMTP protocol.

#Importing Required modules
import argparse
from socket import *
import time
import sys

SIZE = 1024

def main():

#Parser for command-line options and arguments 
    parser = argparse.ArgumentParser()
        
#Type "python2 G22.py --help", to get clear vision of this
    parser.add_argument("-f", help = "Sender E-mail id", type=str)
    parser.add_argument("-d", help = "Reciever E-mail id's", type=str)
    parser.add_argument("-i", help = "Input Filenames separated by \',\' where the mail Body is to be taken from files and subject of the mail should be name of the file. For Ex: Hello.txt >> where Subject: Hello Body: Welcome to World of programming", type=str)
    parser.add_argument("-s", help = "Server IP address >> If you Don't know what to give as input, just type \"localhost\"", type=str)
        
    args = parser.parse_args()

# Check for No inputs
    if(not args.f or not args.d or not args.i or not args.s):
        print "\nUsage: python2 ./G22.py -f 'from email address' -d 'recipient-1 email address','recipient 2 email address',... -i file1,file2,... -s 'server IP address'\n\nCheck this >>>>> Type \"python2 G22.py --help\"\n"
        sys.exit();
# Check for Content of each file constitute one email.
    if (len(args.d.split(",")) != len(args.i.split(","))):
        print "\nWARNING!! Please Enter Equal number of Recipient email address and file because Content of each file constitute one email.\n"
        print "Usage: python2 ./G22.py -f 'from email address' -d 'recipient-1 email address','recipient 2 email address',... -i file1,file2,... -s 'server IP address'\n\nCheck this >>>>> Type \"python2 G22.py --help\" <<<<<<\n"
        sys.exit();

#Calling SmtpClient Function to start the connection and send the mail
    print "\n>> Connecting to the Mail Server..."
    SmtpClient(args.s, args.f, args.d.split(","), args.i.split(","))
    return 0
    
##################################################################    
#Smtp Client Function
#IpAddress or Mail server (E.g Google Mail Server) 
def SmtpClient(ipAddr, mailFrom, mailTo, Msg):
    
    endMsg = ".\n"
#Port 25 is the original standard SMTP port
    portNumber = 25
    count = 0
    
# Create socket called clientSocket and establish a TCP connection with Mailserver or IpAddress
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((ipAddr, portNumber))

    print ""
    Rec = clientSocket.recv(SIZE)
    if (not Rec):
        print "There was an Error in Connected to the Server!!\n >>>>>>> Enter the Correct IpAddress <<<<<<<\n"
        sys.exit()
    print '  ' + Rec,
    
#Send EHLO(Extended helo or Smtp) command, the server and client perform some application-layer handshaking
    heloServer = 'HELO ' + ipAddr + '\r\n'
    print heloServer,
    clientSocket.send(heloServer)
    Rec = clientSocket.recv(SIZE)
    print '  ' + Rec,
    print "\n>> Successfully Connected to the IpAddress: '%s' through port-number: 25\n" % ipAddr
    
#loop to send more than one email in the same session.Also for the Knowledge Smtp uses "Persistent Connection."
    for i in range(len(mailTo)):
        count += 1
#Reading the Message from the File
        try:
            my_file = open(Msg[i], "r")
            msg = my_file.read()
        except IOError:
            print "\nError in File %d! Create File or Enter proper filename \n" % count
            sys.exit()
            
#Send MAIL From command and print the Server Response
        From = "MAIL FROM: " + mailFrom + '\r\n'
        print From,
        clientSocket.send(From)
        Rec = clientSocket.recv(SIZE)
        print '  ' + Rec,
            
#Send Recipient to command and print the Server Response
        to = 'RCPT TO: ' + mailTo[i] + '\r\n'
        print to,
        clientSocket.send(to)
        Rec = clientSocket.recv(SIZE)
        rcp = Rec.split(" ")
        time.sleep(0.8)
        if(250 != int(rcp[0])):
            print "\nInvalid User or Error on Recipient Side\n"
            sys.exit()
        print '  ' + Rec,

#Send DATA command and print the Server Response
        data = 'DATA \r\n'
        print data,
        clientSocket.send(data)
        Rec = clientSocket.recv(SIZE)
        print '  ' + Rec
            
#Sending the message Header and Subject
        From = 'From: ' + mailFrom + '\r\n'
        print From,
        clientSocket.send(From)
        to = 'To: ' + mailTo[i] + '\r\n'
        print to,
        clientSocket.send(to)
        date = 'Date: ' + time.asctime() + '\r\n'
        print date
        clientSocket.send(date)
        file = Msg[i].split(".");
        sub = 'Subject: ' + file[0] + '\r\n'
        print sub
        clientSocket.send(sub)
#Printing the required body for communication
        print msg + '\r\n',
        clientSocket.send(msg)
        
#End of Recipient or end of 1st E-mail, which ends with a period '.'
        print endMsg,
        clientSocket.send(endMsg)
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
#Closing the Connection by passing the Quit command     
    quit = "QUIT \r\n"
    print quit,
    clientSocket.send(quit)
    Rec = clientSocket.recv(SIZE)
    print '  ' + Rec,
    print "\n>> Closing the Connection...\n"
    return

if __name__ == "__main__":
    sys.exit(main())       
