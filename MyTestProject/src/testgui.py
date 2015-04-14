""" Gareth Wilson
    13-Feb-15 """

import tkinter as tk
import threading
from board import GameBoard
import network as nw
from tkinter.constants import DISABLED, NORMAL



""" The GUI class and implementation and main running code. All of the program interaction
is received from the user through the GUI and after changes to the internal logic the GUI 
must be updated accordingly. """
class Application(tk.Frame):
    
    
    STATE = None #
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
    def somethingHappened(self, coord, iid, base): #selected tile, board / self.board
        #print("after smth happend", self.STATE)
        
        # A STATE VARIABLE WILL KEEP TRACK OF EG IF A CLICK ELSEWHERE WILL RESET THE HIGHLIGHTING
        # EG THIS FUNCTION CALLED ACTS DIFFERENTLY DEPENDING ON STATE VARIABLE
        
        #first press code
        tileInfo = inBoard.tilePressed(coord)
        if self.STATE == 1:
            
            
            
            
            ## AT THE START OF EVERY STATE 1 (eg this is following an initial click)
            ## MUST ENFORCE THE 'MUST JUMP' RULE
            ## HOW TO DO THAT EFFICIENTLY?
            ## SCAN EACH PIECE (of the current player)
            ## get a list of jump moves, assert that the tileInfo (one just pressed) is in
            ## this list before proceeding. Else give relevant message etc.
            
            piecesWithJumpsCoords = inBoard.checkAvailableMoves(self.PLAYER, onlyJumps=True)
            #print("====> At start of a turn. If >", len(piecesWithJumpsCoords), "< is not 0,\nthen must assert that the piece selected for this turn is one of those in there.\nIf it's 0 then can select any piece since that means there are no\n jump moves that must be made.")
            if piecesWithJumpsCoords and not tileInfo.tileCoord in piecesWithJumpsCoords: #if there is some in there
                #give message
                self.MESSAGE = "you must capture a piece if possible"
            else:
            
                if tileInfo.isTileOccupied and tileInfo.occupyingPiece.player == self.PLAYER:
                    
                    potentialMoveCoords = inBoard.getAvailableMoveCoords(coord, getOnlyJumps=True)
                    
                    # only look for 1,1 moves when no 2,2 moves
                    # but going to need an entire board check for priority of 2,2 over 1,1 for all pieces
                    if not potentialMoveCoords:
                        potentialMoveCoords = inBoard.getAvailableMoveCoords(coord)
                        
                    #for the initial error double click bug, fix in here
                    
                    
                    #print("24: ", potentialMoveCoords)
                    #print("1. ", potentialMoveCoords)
                    # this line is changing the gui tiles directly
                    #need to make it first change the logic tiles
                    
                    ## USE TILEPRESSED COORD TO GET POTENTIAL MOVE COORDS
                    ## CHANGE EACH OF THE LOGIC TILES AT THOSE POSITIONS TO HIGHLIHGHTED
                    ## REDRAW THE BOARD (WHERE HIGHLIGHTED gets diff colour) 
                    
                    inBoard.plsHighlight(potentialMoveCoords)
                    ## NOW THE LOGIC TILES ARE MARKED TRUE FOR HIGHLIGHT
                    
                    ## NOW RENDER THE DISPLAY
                    
                    #now the board is highlighted accordingly
                    # so update the state
                    self.SELECTED = tileInfo
                    self.POTENTIAL = potentialMoveCoords
                    self.STATE = 2
                    #break (so next if is not executed ...)
        
        # so on the second press when STATE==2 this code is executed
        elif self.STATE == 2:
            #board is currently highlighted
            # tileInfo will contain the tile which was just pressed
            # so check if its highlighted, if it is, move piece FROM PREVIOUS STEP (?) to here
            # otherwise its out of the legal moves so reset the highlighting and then reset the state
            
            #simpler to just check with gui tile rather than mainting syncronisation between gui and logic tiles
            
            # convert tileInfo to the gui tile, 
            # check that gui tile is highlighted / not
            
            # CHECK AGAINST LOGI FOR CONSISTENCY
            if tileInfo.isHighlighted:
                #print("OK, moving piece now") # using self.SELECTED
                
                ## so a valid (highlighted) targeted tile has been clicked to move the piece to
                ## NEED TO work out which move object has been selected, in order to remove any jumped pieces
                
                #         self.SELECTED is tileA
                #         tileInfo is tileB
                #         self.POTENTIAL contains the list of moves it could be
                
                ## CALL FUNC TO MOVE THE PIECE
                ## MOVING PIECE FROM self.SELECTED to tileInfo
                
                outcome = inBoard.plsMovePiece(self.SELECTED, tileInfo, self.POTENTIAL)
                
                inBoard.plsUnHighlight(self.POTENTIAL)
                
                ## swap players
                ## end of turn, swap players 
                ## BUT if pieceDeleted is occupied then allow further checking for successive jumps
                #print("========== END OF TURN ===========")
                if outcome['piece_captured']:
                    captured_piece = outcome['piece_captured']
                    self.NUM_DELETED[captured_piece.player] += 1
                    # instead of going to other players turn, keep on current player,
                    # make selected the recently landed (tileInfo)
                    self.SELECTED = tileInfo
                    
                    #print(self.STATE)
                    # want to get the new landeed location and only go to state 9 if there are
                    # more available jump moves
                    if outcome['piece_isKinged']:
                        # eg if a piece was kinged as a result, dont look for more jumps
                        #print('king created, move ends')
                        #CHANGE THESE TO FUNCTIONS
                        self.PLAYER = "white" if self.PLAYER == "red" else "red"
                        self.MESSAGE = "it is " + self.PLAYER + "'s turn"
                        self.STATE = 1
                    else:
                        anyMoreAvailableJumpMovesQQ = inBoard.getAvailableMoveCoords(tileInfo.tileCoord, getOnlyJumps=True)
                        if anyMoreAvailableJumpMovesQQ:
                            self.POTENTIAL = anyMoreAvailableJumpMovesQQ
                            self.STATE = 9
                        else:
                            self.PLAYER = "white" if self.PLAYER == "red" else "red"
                            self.MESSAGE = "it is " + self.PLAYER + "'s turn"
                            self.STATE = 1
                else:
                    self.PLAYER = "white" if self.PLAYER == "red" else "red"
                    self.MESSAGE = "it is " + self.PLAYER + "'s turn"
                    self.STATE = 1
                #use tile from SELECTED to move to  guiTile/tileInfo
                # and reset the highlighting
            # ELIF the player has clicked on another of their pieces instead of a highlighted place
            elif not tileInfo.isHighlighted and tileInfo.isTileOccupied and tileInfo.occupyingPiece.player == self.PLAYER:
                if self.SELECTED.tileCoord != tileInfo.tileCoord:
                    # if its a new piece (same player) just update the highlight
                    inBoard.plsUnHighlight(self.POTENTIAL)
                    self.STATE = 1
                    # essentially repeat top code
                    self.somethingHappened(coord, iid, base)
                else:
                    
                    #its the same piece which has been clicked, just remove the highlight is all
                    inBoard.plsUnHighlight(self.POTENTIAL)
                    self.STATE = 1
                
            
            else:
                #its not a highlighted position OR one of their other pieces
                # so reset the highlighting of those tiles in POTENTIAL
                # the colour needs to be the original COLOR OF THE TILES
                
                #the current highlights are stored in POTENTIAL
                #but its better to just reset all tiles back to non-highlight ...
                inBoard.plsUnHighlight(self.POTENTIAL)
            
                self.STATE = 1
        
        elif self.STATE == 9: #test state
            #if state is 9 then this means player has just captured a piece
            # need to take the piece he just used (which will be placed into selected)
            # and see if there are successive jump moves eg only allow the clicked tile (tileInfo)
            # to be == to selected
            #print("getting to here, player is: ", self.PLAYER)
            if tileInfo == self.SELECTED:
                
                #print("my list of jump moves is: ", self.POTENTIAL)
                
                # if there are no move valid jumps (2,2), change player and go to state 1
                # otherwise repeat for successive jumps
                
                inBoard.plsHighlight(self.POTENTIAL)
                self.SELECTED = tileInfo # redundant
                self.STATE = 2
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
    
    
    
    def hostGame(self, base=None):
        # calls the methods in network module, updating message status as it goes
        # draft paper how this should be designed
        # create dialogue box using base??
        # success = nw.host
        ## MESSAGE = waiting for connecting
        t = threading.Thread(target=nwobj.host)
        t.start()
        print(t.is_alive())
        print(t.is_alive())
        #result = nwobj.host()
        #if result:
            #print("connection established")
        #else:
            #print("connection failed")
        # if result success, MESSAGE = "connected successfully etc", and refreshDisplay
        # eg just updates the message value
        
        ## BREAK REFRESH DISPLAY INTO 2 FUNCS SO NOT HAVING TO REFRESH WHOLE BOARD AT THIS STAGE
        
    def joinGame(self):
        pass
    
    
    
    
            
            
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
        filemenu.add_command(label="Local Game", command=lambda: self.setup(base, Board))
        # this is another inner cascade menu with the join and host options (its added to the mainmenu)
        
        multimenu = tk.Menu(tearoff=0)
        multimenu.add_command(label="Host", command=self.hostGame)
        multimenu.add_command(label="Join", command=self.joinGame)
        
        filemenu.add_cascade(label="Multiplayer Game", menu=multimenu)
        #filemenu.add_command(label="Save", command=0)
        filemenu.add_command(label="Settings", command=self.openSettings)
        filemenu.add_command(label="About", command=self.openAbout)
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
        