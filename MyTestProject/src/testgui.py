""" Gareth Wilson
    13-Feb-15 """

import tkinter as tk #s
import threading
from board import GameBoard
import network as nw
from tkinter.constants import DISABLED, NORMAL



""" The GUI class and implementation and main running code. All of the program interaction
is received from the user through the GUI and after changes to the internal logic the GUI 
must be updated accordingly. """
class Application(tk.Frame):
    
    
    STATE = None #d
    GAMETYPE = None
    PLAYER = None
    SELECTED = None
    POTENTIAL = None
    NUM_DELETED = {"red": 0, "white": 0}
    MESSAGE = None
    
    
    """ Creates initial board state by calling the draw method."""
    def __init__(self, inBoard, master, nwobj):
        tk.Frame.__init__(self, master)
        #self.grid()
        self.draw(inBoard, master)
        self.nwobj = nwobj
              
    
    """ Changes the GUI tile color. 
    ~~ Not used. - early version of highlight code. """
    def changeTileColour(self, base, iid, availableMovesAsTags, col):
        #available moves as list of coords
        #for coord in abvailableMoves
        for move in availableMovesAsTags:
            #print("isisisis ", move)
            tileId = base.find_withtag("uniqueTag" + move)
            
            
            #this should be printing the item id of the element with that tag
            # instead its printing the item id as 10 ...
            
            # EVERY GUI ITEM WITH ID = say 10, WILL DEFAULT HAVE AN AUTO TAG OF "10"
            # SO NEEDED TO MAKE THE TAGS MORE UNIQUE EG "uniqueTag10"
            base.itemconfig(tileId, fill=col)
        # need to get the item id for each of those in available moves or the tag
        # the program should deal in coordinates for logic, so easiest way would be to
        # add a tag to each gui element (containing the coords) to manipulate them
        
        
    """ TODO: takes a color of a tile and the highlight color and returns the 
    nicely blended color. Probably adding the color values and taking the 
    averages is the best approach. """
    def colorBlend(self, tileCol, highlightCol):
        if highlightCol != '': # eg if highlighted specified
            blendedCol = highlightCol
        else:
            blendedCol = tileCol
        return blendedCol
    
    
    
    
    """ This function checks the logic tiles for changes and updates the corresponding
    gui tiles if a change is required.
    Version 1.1 update the GUI tiles with the corresponding information in the logic tiles.
    Firstly apply TILE COLOR, then super impose the piece (if it exists) finally blend it with the
    highlight if it is required
    Version 1.1 current - ignoring blend atm, just highlighting by replacing tile color. """    
    def refreshDisplay(self, base, board):
        #set each gui tile icon to whatever it is in logic tile
        #but if logic tile is marked as highlighted set it to hilight color
        
        
        
        ## UPDATE BOARD GUI ELEMENTS
        ## GET THE CORRESPONDING GUI TILE FOR EACH LOGIC TILE
        for row in board:
            for logicTile in row:
                #print("tile is at pos", logicTile.tileCoord)
                tag = "uniqueTag" + str(logicTile.tileCoord[0]) + str(logicTile.tileCoord[1])
                guiTile = base.find_withtag(tag)
                ## now update gui tile with logic tile info etc, make into a func?
                
                ## the gui tile returned is currently just the black/white square
                highlight = '#fb0' if logicTile.isHighlighted else '' #transparent
                
                tileColor = self.colorBlend(logicTile.tileIcon, highlight)
                
                base.itemconfig(guiTile, state=NORMAL) # ensures the board is enabled (mainly only for initial press)
                # basically here so that player cant interact with board before he has clicked the 'start' button
                # which populates it etc
                base.itemconfig(guiTile, fill = tileColor)
                
                if logicTile.guiMustBeUpdated and logicTile.isTileOccupied:           # AND PIECE NOT ALREADY PLACED !!!!
                    ## if its occupied create another thing to put on top
                    tileCoords = base.coords(guiTile)
                    # create a smaller box to put on top (or an image)
                    tileCoords[0] += 70
                    tileCoords[1] += 70
                    tileCoords[2] -= 70     #      -?
                    tileCoords[3] -= 70
                    
                    
                    
                    guiTilePiece = base.create_oval(tileCoords, fill=logicTile.occupyingPiece.icon, tags = tag+"piece")
                    ## NOW the tile itself and the playing piece respond to the players clicks
                    base.tag_bind(guiTilePiece, "<Button-1>", lambda evt, iid=guiTilePiece, coord=logicTile.tileCoord, base=base: self.somethingHappened(coord, iid, base))
                    logicTile.guiMustBeUpdated = False
                
                if logicTile.guiMustBeUpdated and not logicTile.isTileOccupied:
                    ## then remove the previous gui piece from it (since it has been removed in the logic)
                    ## identify using the standard tag for this tile + "piece" addition
                    base.delete(tag + "piece")
                    logicTile.guiMustBeUpdated = False
                    
                
        ## UPDATE SCORE GUI ELEMENTS
        score_board = base.find_withtag('disp')
        formattedScore = 'Pieces Lost\nRed: %(red)s White: %(white)s' % self.NUM_DELETED
        base.itemconfig(score_board, text = formattedScore)
        ## UPDATE message display
        message_board = base.find_withtag('msg')
        base.itemconfig(message_board, text = self.MESSAGE)
                
    def smh(self):
        print("presseed") 
                
    """Version 1.0 Regardless of game state, reset the internal logic to the initial position by
    first clearing it then repopulating it. As well as the logical pieces needing to be reset
    the flags for the gui (in the logic model) also required resetting. Finally calls refresh 
    display. """
    def setup(self, base, Board):
        # ALSO MUST RESTORE HIGHLIGHTING
        
        # the input Board is the class containing board at black/white stage
        # the pieces in the initial state
        Board.clearGameBoard() # logic
        #self.refreshDisplay(base, Board.board) # gui
        
        Board.populateGameBoard() # logic
        self.refreshDisplay(base, Board.board) # gui      # only need to send the physical board to the gui    
        self.STATE = 1
        self.PLAYER = "red"
        self.SELECTED = None    # needed?? 
        self.POTENTIAL = None
        self.NUM_DELETED = {"red": 0, "white": 0}
        self.refreshDisplay(base, Board.board) # gui      # only need to send the physical board to the gui    
        self.MESSAGE = "it is " + self.PLAYER + "'s turn"
        self.refreshDisplay(base, Board.board)
              
              
    """Opens the 'about' pane, focussing the cursor on it and placing it
    in the middle of the screen""" 
    def openAbout(self):
        aboutPane = tk.Toplevel()
        aboutPane.resizable(0, 0)
        
        
        # centre it in the middle of the screen
        width = aboutPane.winfo_screenwidth()
        height = aboutPane.winfo_screenheight()

        
        # geometry will place top-left in this central position
        # need to offset it so middle of the pane is in the central position
        
        paneWidth = 220
        paneHeight = 170
        middle_x = str(int(width / 2 - paneWidth / 2))
        middle_y = str(int(height / 2 - paneHeight / 2))
        
        
        aboutPane.geometry(str(paneWidth) + "x" + str(paneHeight) + "+" + middle_x + "+" + middle_y)
        aboutPane.attributes("-toolwindow", 1)
        #settingsPane.overrideredirect(1)
        aboutPane.grab_set()
        aboutPane.title("About")
        
        msg = tk.Message(aboutPane, text="\nEnglish Draughts 1.2 by Gareth Wilson. " + 
                                         "Players can play a local one versus one game, sharing " +
                                         "a computer, or host or join a game over the internet. " +
                                         "Connection parameters can be adjusted in the settings.")
        msg.pack()   
        
        btn1 = tk.Button(aboutPane, text="Close", command=aboutPane.destroy)
        btn1.pack()
        
        # when the window is closed, grab_set is released              
              

    """Opens a settings pane, focussing the cursor on it and placing it
    in the middle of the screen. SETTINGS SHOULD be stored in a file""" 
    def openSettings(self):
        settingsPane = tk.Toplevel()
        settingsPane.resizable(0, 0)
        
        # centre it in the middle of the screen
        width = settingsPane.winfo_screenwidth()
        height = settingsPane.winfo_screenheight()

        
        # geometry will place top-left in this central position
        # need to offset it so middle of the pane is in the central position
        
        paneWidth = 500
        paneHeight = 300
        middle_x = str(int(width / 2 - paneWidth / 2))
        middle_y = str(int(height / 2 - paneHeight / 2))
        
        
        settingsPane.geometry(str(paneWidth) + "x" + str(paneHeight) + "+" + middle_x + "+" + middle_y)
        settingsPane.attributes("-toolwindow", 1)
        #settingsPane.overrideredirect(1)
        settingsPane.grab_set()
        settingsPane.title("Settings")
        # add a canvas
        # add fields and buttons etc
        msg = tk.Message(settingsPane, text="add fields and buttons etc")
        msg.pack()   
        
        btn1 = tk.Button(settingsPane, text="Close", command=settingsPane.destroy) 
        btn2 = tk.Button(settingsPane, text="Apply", command=0) #TODO saves the settings to file
        btn1.pack()
        btn2.pack()
        
        # when the window is closed, grab_set is released
        
        
        
    
    
    """ This is the main callback function. This is executed whenever a tile/piece is clicked
    on the displayed board. This function also uses a couple of global state variables to 
    determine correct responses to certain sequences of tile/piece clicking. This is a small 
    amount of game logic which could possibly be moved further into the model if required. 
    Responses to gui actions are calls to various board methods, followed by a refreshDisplay call
    in order to update the GUI. """
    def somethingHappened(self, coord, iid, base):
        
        
        ## if self.GAMETYPE == "hosting" - do game with moves sent to network
        
        tileInfo = inBoard.tilePressed(coord) # get the tile which was pressed
        #if first press of turn
        if self.STATE == 1: 
            
            # check if there are any jumps available
            available_jumps = inBoard.checkAvailableMoves(self.PLAYER, onlyJumps=True)
            
            # if jumps available and the clicked tile isn't in one of them
            if available_jumps and not tileInfo.tileCoord in available_jumps:
                self.MESSAGE = "you must capture a piece if possible"
            
            else:
                # if the tile contains the player's own piece
                if tileInfo.isTileOccupied and tileInfo.occupyingPiece.player == self.PLAYER:
                    
                    # firstly get the potential places to move to for the selected piece (jumps)
                    potentialMoveCoords = inBoard.getAvailableMoveCoords(coord, getOnlyJumps=True)
                    
                    # if there are no potential jump moves, then get the normal moves
                    if not potentialMoveCoords:
                        potentialMoveCoords = inBoard.getAvailableMoveCoords(coord)
                        
                    # highlight these places as potential places to move to
                    inBoard.plsHighlight(potentialMoveCoords)
                   
                    # board is now highlighted
                    # SELECTED contains that initial tile
                    # POTENTIAL contains those tiles which are highlighted
                    self.SELECTED = tileInfo
                    self.POTENTIAL = potentialMoveCoords
                    
                    # change the state to "tileA is clicked and board highlighted"
                    self.STATE = 2
        
        #elif the second press of the turn (board has highlighted valid tileBs))
        elif self.STATE == 2:
            # tileInfo will contain the tileB which was just pressed
            #SELECTED will contain tileA
            #POTENTIAL will contain the valid positions tileB can b
           
            
            # if tileB is Highlighted (eg same as in potential)
            if tileInfo.isHighlighted:
                
                # move the piece from tileA (SELECTED) to tileB(tileInfo)
                # identifies this 'move' in the POTENTIAL (list of moves)
                # in order to get info about any captured pieces
                outcome = inBoard.plsMovePiece(self.SELECTED, tileInfo, self.POTENTIAL)
                
                # now the logic move has completed,
                inBoard.plsUnHighlight(self.POTENTIAL)
                
                
                # need to check for a kinging result / further jumps for the turn
                if outcome['piece_captured']:
                    captured_piece = outcome['piece_captured']
                    self.NUM_DELETED[captured_piece.player] += 1
                    
                    # eg the tileB is the new tileA
                    self.SELECTED = tileInfo
                    
                    
                    if outcome['piece_isKinged']:
                        # the 'kinging' of the piece is done in the plsMovePiece function
                        # so just end the turn (a new king cant continue jumping)
                        
                        ## TODO change this to a function
                        self.PLAYER = "white" if self.PLAYER == "red" else "red"
                        self.MESSAGE = "it is " + self.PLAYER + "'s turn"
                        self.STATE = 1
                    #else not king so just check for extra jumps
                    else:
                        anyMoreAvailableJumpMovesQQ = inBoard.getAvailableMoveCoords(tileInfo.tileCoord, getOnlyJumps=True)
                        if anyMoreAvailableJumpMovesQQ:
                            self.POTENTIAL = anyMoreAvailableJumpMovesQQ
                            self.STATE = 3 # "jump sequence continues"
                        # else no move moves, so just end turn and change player
                        # state is reset back to 1 for the next player
                        else:
                            self.PLAYER = "white" if self.PLAYER == "red" else "red"
                            self.MESSAGE = "it is " + self.PLAYER + "'s turn"
                            self.STATE = 1
                # else the move was just a 1,1 move (no captures etc)
                else:
                    self.PLAYER = "white" if self.PLAYER == "red" else "red"
                    self.MESSAGE = "it is " + self.PLAYER + "'s turn"
                    self.STATE = 1
                    
            # elif the player has clicked on another of their pieces (instead of a highlighted tile)
            elif not tileInfo.isHighlighted and tileInfo.isTileOccupied and tileInfo.occupyingPiece.player == self.PLAYER:
                # if the player has clicked on another of their pieces
                if self.SELECTED.tileCoord != tileInfo.tileCoord:
                    # remove the current highlight
                    inBoard.plsUnHighlight(self.POTENTIAL)
                    # go back to state 1 and repeat from start
                    self.STATE = 1
                    self.somethingHappened(coord, iid, base)
                # else the player just clicked on that tileA again
                else:
                    # so just unhighlight (like a toggle)
                    inBoard.plsUnHighlight(self.POTENTIAL)
                    self.STATE = 1
                
            # else the player just clicked somehwere else on the board
            else:
                
                inBoard.plsUnHighlight(self.POTENTIAL)
                self.STATE = 1
           
           
        # elif:        
        # an opponent's piece has just been jumped
        # and there are further pieces which can be jumped
        elif self.STATE == 3:
            
            if tileInfo == self.SELECTED:
                
                inBoard.plsHighlight(self.POTENTIAL)
                self.SELECTED = tileInfo
                self.STATE = 2
            # force player to continue this jump sequence
            else:
                self.MESSAGE = self.PLAYER + ", please continue the capture sequence"
                
            
        
        ## AT the END OF EVERY TURN also need to check that there are possible normal moves
        ## for the next player to make

        piecesWithAvailableMoves = inBoard.checkAvailableMoves(self.PLAYER)
        if not piecesWithAvailableMoves:
            # make it better
            winner = 'white' if self.PLAYER == 'red' else 'red'
            self.MESSAGE = '\n', self.PLAYER, 'has no more legal moves\n', winner, ' wins!\n'
        
        
        #print("the logic has been completed, finally redraw the display")
        #this function takes the board and uses it to update the disaply
        ## is basically a 'draw' based on new version of inBoard
        self.refreshDisplay(base, inBoard.board)
    
    
    def on_client_connect(self, base, Board):
        print("connection has been made so now allow each prog to proceed to thegame")
        self.GAMETYPE = "hosting"
        # state is set tp multiplayer-host
        # have access to base (gui) and board
        self.setup(base, Board)
        
        
    
    
    def hostGame(self, base, Board):
        # calls the methods in network module, updating message status as it goes
        # draft paper how this should be designed
        # create dialogue box using base??
        # success = nw.host
        ## MESSAGE = waiting for connecting
        t = threading.Thread(target=nwobj.host, args=(base, Board, self.on_client_connect))
        t.start()
    
        print("main thread in waiting on connection status, but thread not blocked")
        
        #result = nwobj.host()
        #if result:
            #print("connection established")
        #else:
            #print("connection failed")
        # if result success, MESSAGE = "connected successfully etc", and refreshDisplay
        # eg just updates the message value
        
        ## BREAK REFRESH DISPLAY INTO 2 FUNCS SO NOT HAVING TO REFRESH WHOLE BOARD AT THIS STAGE
        
    def joinGame(self):
        jt = threading.Thread(target=nwobj.join, args=(self.connection_success_callback,))
        jt.start()
        print("main thread in waiting on result of join attempt, not blocked")
    
    def closeSock(self):
        nwobj.close_sockets()
    
    
            
            
    def localGame(self, base, Board):
        self.STATE = 1
        self.setup(base, Board)
            
    """ Draws the GUI buttons, board and tiles and attaches each tile to a callback function
    with relevant parameters (coords according to which tile was pressed). 
    sets parameters for the window (Frame) and attaches the canvas to it"""
    def draw(self, Board, window):
        
        
        window.resizable(0,0)
        width = window.winfo_screenwidth()
        height = window.winfo_screenheight()

        
        # geometry will place top-left in this central position
        # need to offset it so middle of the window is in the central position
        
        #canvas size params
        cWidth = 900
        cHeight = 703
        middle_x = str(int(width / 2 - cWidth / 2))
        middle_y = str(int(height / 2 - (cHeight / 2) - 30)) # the extra 30 pixels is to account for task bar
        
        
        window.geometry(str(cWidth) + "x" + str(cHeight) + "+" + middle_x + "+" + middle_y)
        window.attributes("-toolwindow", 1)
        
        
        base = tk.Canvas(window, width=cWidth, height=cHeight, background='OliveDrab4')
        #make it a window, then add buttons etc
        
        
        # change to create windows, add the buttons etc,
        #create an gui array to contain these elements
        # for i in numbuttons, calculate next coord/dimensions
        #    i = base.create_rectangle(dimensions)
        #    add bind tp it with arg=i (tile num etc)
        # add each of these elements to an array so the gui elements can be accessed
        
        
        
        # eg these view tiles are not linked to internal tiles, but their colours etc are derived
        # gui updates by mimicing internal,
        # user interacts with gui, gives view coords, which are passed to the logic through one func (interface)
        # at the end of an event, and internal change state, the view will need to redraw/update itself ?
        
        #THIS CODES ADD TO ABOVE FORLOOP
        # OR ECACH TIME THE BOARD IS REFRESHED
        
        
        #total canvas size 
        #cWidth, cHeight = 600
        
        
        
        
        # #FAF0E6 - linen
        
        baseX=20
        baseY=653
        
        #compute coords for each tile using (x,y) from tile and finite canvas size (600,600)
        
        # ITS POPULATING TILES FROM BOT LEFT TO TOP RIGHT wHILE INTERNAL BOARD IS CURRENTLY REVERESED SETUP
        
        
        for row in Board.board:
            for tile in row:
                btmLeftX = baseX+tile.tileCoord[0]*75
                btmLeftY = baseY-tile.tileCoord[1]*75
                topRightX = btmLeftX+75
                topRightY = btmLeftY-75
                

                #guiTile = base.create_rectangle(3, 600, 600, 103, activefill=tile.tileColour)
                #the guiTileRepresentative represents the tile plus whatever piece is on the tile
                #use create_image and the ICON within tile->piece if it exists for the icon
                guiTileRepresentative = base.create_rectangle(btmLeftX, btmLeftY, topRightX, topRightY, fill=tile.tileIcon, state=DISABLED, tags= "uniqueTag" + str(tile.tileCoord[0]) + str(tile.tileCoord[1]))
                
                #guiTileRepresentative = base.create_image(btmLeftX, btmLeftY, anchor=NS, image=tile.getIcon())
                
                # add id / coords of that tile to the callback
                base.tag_bind(guiTileRepresentative, "<Button-1>", lambda evt, iid=guiTileRepresentative, coord=tile.tileCoord, base=base: self.somethingHappened(coord, iid, base))
                
                
        # menuDisplay1 = base.create_rectangle(3, 50, 53, 3, fill = 'orange2', activefill='orange1')
        # base.tag_bind(menuDisplay1, "<Button-1>", lambda evt, base = base, Board = Board: self.setup(base, Board))
        
        base.create_rectangle(650, 53, 870, 275, fill='antique white')
        base.create_text(710, 70, text="SCORE", tags = 'disp')
        base.create_text(710, 100, text="MESSAGE", tags = 'msg')
        
        
      
        
        # main drop down menu (button for it)
        menubutton = tk.Menu(window)
        
        filemenu = tk.Menu(tearoff=0)
        filemenu.add_command(label="Local Game", command=lambda: self.localGame(base, Board))
        # this is another inner cascade menu with the join and host options (its added to the mainmenu)
        
        multimenu = tk.Menu(tearoff=0)
        multimenu.add_command(label="Host", command=lambda: self.hostGame(base, Board))
        multimenu.add_command(label="Join", command=self.joinGame)
        
        filemenu.add_cascade(label="Multiplayer Game", menu=multimenu)
        #filemenu.add_command(label="Save", command=0)
        filemenu.add_command(label="Settings", command=self.openSettings)
        filemenu.add_command(label="About", command=self.openAbout)
        filemenu.add_command(label="close sockets (test)", command=self.closeSock)
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=window.quit)
        
        # the above items are added to the main menubutton
        menubutton.add_cascade(label="Menu", menu=filemenu)
        
        window.config(menu=menubutton)
        
        
        base.pack()
        
        
        


inBoard = GameBoard()  #logic
nwobj = nw.Network()
master = tk.Tk()
app = Application(inBoard, master, nwobj)
app.master.title('English Draughts')
app.mainloop()
        