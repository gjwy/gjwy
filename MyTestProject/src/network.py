import json
import socket

class Network():
    
    HOST = "192.168.1.16"
    PORT = 9999
    SERVERSOCKET = None
    CLIENTSOCKET = None # the connection is sent to this one ultimately
    CONNECTION = None 
    
    def host(self, success_callback):
    # load settings from file, do a quick check to ensure they are valid
    # create the connection and wait for a join,
    # offload it to client socket,
    # after join, or certain time, return success value
        
        print("I am host")
        
        self.SERVERSOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SERVERSOCKET.bind((self.HOST, self.PORT)) # binds socket to that host on the local port
    
        #client connected, handled by a created clientsocket
        self.SERVERSOCKET.listen(1) ## allow 1 independant connection
        while not self.CLIENTSOCKET:
            self.CLIENTSOCKET, addr = self.SERVERSOCKET.accept()
            print("Got a connection from %s" % str(addr))
            
        
        print("clientsocket handling the connection")
        self.CONNECTION = True
        #if get to here then connection made,
        success_callback()
        return self.CONNECTION
            
                #msg = input("> press enter to send")
                ## nw.send_msg(msg, cs)
                #theMsg = {'msg_type': 'info', 'game': 'english_draughts', 'assigned_player': 'red', 'start_player': 'white'}
                #game_info = json.dumps(theMsg).encode('ascii')
                #self.send_game_info(cs, game_info)
                #thisPlayer = 'white' # make proper
    
                #primaryInfo = self.prepare_for_game(theMsg, thisPlayer)
            #then start the game, each side does an action depending on contents of game_info
            #so one side will make a move and ready to send it
            #other side will have the board disabled and be waiting to receive a move
            #after which it will alter the internal state based on the recent move
        
            
        
        
        
    
    
  

    
    def join(self, success_callback):
        clientsSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        clientsSocket.connect((self.HOST, self.PORT))
        print("the client has connected to the host")
        success_callback()
        
        
        
        
        
        