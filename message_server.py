import socket
import sys
import threading
from threading import *
import time
from datetime import datetime

print(datetime.now())




#creating socket object
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('----------------------------------------MESSAGE SERVER-------------------------------------')
ip=input('Enter Ip Address of the host(server):')

#creating mesage server
server.bind((ip,2222))

#limiting sever to 2 conneections
server.listen(2)


logs=[]

#message thread for live messaging
class message(Thread):

    def __init__(self,c1,c2):
        threading.Thread.__init__(self)
        self.sender=c1[0]
        self.reciever=c2[0]
        self.sender_address=c1[1]
        self.reciever_address=c2[1]

    def run(self):


        while True:
            message = None
            while True:
                while message == None:
                    message = self.sender.recv(4096).decode() #getting Message from sender 
                    logdata=(str(datetime.now()) + '\t FROM-' +str(self.sender_address) +'\tTO-'+str(self.reciever_address)+'\t MESSAGE-' +str(message))
                    logs.append(logdata)
                    print(logdata,'\n')
                self.reciever.send(bytes(message,'utf-8')) #sending message to reciever
                message=None


connections=0       #for counting connections
details=[]          #storing client objects
while connections<2:
    c,addr=server.accept()
    print('[+]Client',connections+1,'Connected')
    details.append([c,addr])        #appending client details to single list
    connections+=1


print(details)
#separating client details
c1=details[0]
c2=details[1]

#Sending Acknowledgements
c1[0].send(bytes('ok','utf-8'))
c2[0].send(bytes('ok','utf-8'))

#creaitng thread objects
client1=message(c1,c2)
client2=message(c2,c1)

#starting threads
client1.start()
client2.start()


#closing connctions
server.close()
print(logs)




