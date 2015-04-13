import socket
 
host = "192.168.1.26"
port = 9999
 
def be_client():
 
        # create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
       
        #host = socket.gethostbyname(socket.gethostname())    
 
        # connection to remote hostname on remote port
        s.connect((host, port))                              
 
        # Receive no more than 1024 bytes                                
 
        msg = s.recv(1024)
        while msg:
 
                print(": %s" % msg.decode('ascii'))
                msg = s.recv(1024)
        s.close()
 
 
be_client()