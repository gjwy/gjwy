""" Gareth Wilson
    13-Feb-15 """
# minusminusminus
from tile import Tile
from piece import Piece

""" The internal gameboard representation primarily a container for the logical tile objects and
performing game logic calculations. Changes made as a result (mostly to tiles) are flagged and 
will be seen by the gui code and the corresponding graphical tiles etc will be updated. """
class GameBoard():
    board = [] #contains all board infoy
    size = 0
    def __init__(self, size=8):
        self.size = size
        self.generateGameBoard()
        # now board contains rows containing pieces
        # pieces will be filled in with colours etc when
        # the board is populated
        #self.populateGameBoard()
    
    """Creates an internal logic board by filling it with tile objects"""
    def generateGameBoard(self):
        for y in range(0, self.size):
            # create each row to contain each piece
            row = []
            for x in range(0, self.size):
                # create each piece in the row
                # add coord info based on x,y
                # add the piece to the row
                tile = Tile()
                if (y % 2) == 0: # is even
                    col = 'black' if (x % 2) == 0 else 'antique white' # is even
                else:
                    col = 'antique white' if (x % 2) == 0 else 'black'
                
                tile.tileIcon = col
                tile.tileCoord = (x,y)
                #print("== tile", tile.tileCoord, "is ", tile.tileIcon)
                row.append(tile)
            # add the row to the board
            self.board.append(row)
    
    
    """Removes all pieces and flags from the internal board"""
    def clearGameBoard(self):
        for row in self.board:
            for tile in row:
                tile.occupyingPiece = ''
                tile.isTileOccupied = False
                tile.isHighlighted = False
                tile.guiMustBeUpdated = True
        
    
    
    
    # TODO
    # populate with pieces according to rules
    # needs info about coords
    """Fills the board with player pieces in the initial board state and flags them
    as needing to be updated accordingly by the gui code"""
    def populateGameBoard(self, rules=None):
        # far side
        for y in range(0, 3):
            player = 'white'
            row = self.board[y]
            for x in range(0, self.size):
                tile = row[x]
                if tile.tileIcon == 'black':
                    coord = (x,y)
                    piece = Piece(player, 'd_men', coord)
                    tile.occupyingPiece = piece
                    tile.isTileOccupied = True
                    tile.guiMustBeUpdated = True
            
        for y in range(5, 8):   
            player = 'red'
            row = self.board[y]
            for x in range(0, self.size):
                tile = row[x]
                if tile.tileIcon == 'black':
                    coord = (x,y)
                    piece = Piece(player, 'd_men', coord)
                    tile.occupyingPiece = piece
                    tile.isTileOccupied = True
                    tile.guiMustBeUpdated = True
                
            
            
            
    """Returns a subset of the board object.
    Not used. """
    def getDisplayBoard(self):
        # TODO
        # returns a subset of board
        # containing just the colors in the x,y 
        # format ready for displaying
        dispBoard = []
        for y in range(0, self.size):
            row = []
            for x in range(0, self.size):
                dispStr = self.board[y][x].tileIcon
                if self.board[y][x].isTileOccupied:
                    dispStr += self.board[y][x].occupyingPiece.player
                row.append(dispStr)
            dispBoard.append(row)
            
        # ls of ls containing colour values (str)
        return dispBoard
    
    
    """Takes as input some x, y coordinates and returns the logical tile 
    at that position in the board. """
    def tilePressed(self, coords):
        #print(coords, " has been pressed")
        xCoord, yCoord = coords[0], coords[1]
        
        #print("tile requested is ", self.board[yCoord][xCoord])
        return self.board[yCoord][xCoord]
    
    
    """Takes as input coordinates and retrieves the logical tile object, then gets a list of
    *available* moves the piece on that tile can make. The function further sanity checks the
    available moves to make sure they are legally on the board and are not obstructed by other
    playing pieces. The function returns this valid set of available moves. """
    """TODO: add checks for jump moves eg. probably reorganise this entire process. """
    def getAvailableMoveCoords(self, inCoords, getOnlyJumps=False):
        xCoord, yCoord = inCoords[0], inCoords[1]
        tile = self.board[yCoord][xCoord]
        if tile.isTileOccupied:
            piece = tile.occupyingPiece
            availableMoves = piece.getAvailableMoves()
            # Contains (+1,+1) move objects
            
            
        #now this func (at board level) must take the LEGAL subset from these available hereabouts
        # ...
        validAvailableMoves = []
            
        if not getOnlyJumps: # otherisew it will onl return the jump moves
            for availableMove in availableMoves: # eg [3, 4]
                #print("23: ", availableMove)
                isValid = True
                
                ## change to a check function
                for endPoints in availableMove.pos11:
                    if not endPoints in range(0, self.size):
                        isValid = False
                        
                ## NOW CHECK IF NOT ALREADY OCCUPIED BY ANOTHER PIECE -EXTRA COMPLEXITY FOR JUMPING
                # make the tile at this 'availableMove' and check if its occupied
                if isValid: #if the move is properly on the board, next check for the landing tile being free
                    endX, endY = availableMove.pos11[0], availableMove.pos11[1]
                    endTile = self.board[endY][endX]
                    if endTile.isTileOccupied:
                        isValid = False #then this move is not valid, but also check for a legal jump
                        
                ## only adds those initial +1,+1 moves which are 'properly on the board' and not blocked from landing
                if isValid:
                    validAvailableMoves.append(availableMove)
                    
        
        for availableMove in availableMoves:
            isValid = True
            
            for endPoints in availableMove.pos22:
                if not endPoints in range(0, self.size):
                    isValid = False # then this 'jump move' is not needed for further testing .. 
                    # break - ?
            #print("25: ", isValid)
            if isValid: # otherwise its on the board so check it for jump as usual
                pos22X, pos22Y = availableMove.pos22[0], availableMove.pos22[1]
                pos11X, pos11Y = availableMove.pos11[0], availableMove.pos11[1]
                pos22Tile = self.board[pos22Y][pos22X]
                pos11Tile = self.board[pos11Y][pos11X]
                
                # sanity check first ..
                
                if pos11Tile.isTileOccupied and pos11Tile.occupyingPiece.player != piece.player and not pos22Tile.isTileOccupied:
                    isValid = True
                    availableMove.isJump = True
                else:
                    isValid = False
            
                
                
            if isValid:
                validAvailableMoves.append(availableMove)
                    
                    
                    
            
        # ...
        
        
        # 1. check for +1+1 and sanity check and add to valid
        # 2. check for +2+2 and sanity check and add to valid
        # 3. then all the moves can be highlighted. when it comes to MOVING a piece
        # how it moves will depend on the type of move (eg wheter it contains jump move )
        
        # better this way than above version since even if it found a jump move all this sanity
        # check code would have to be inserted in again and it would look messy.
        return validAvailableMoves
    
    """ Scans the board looking for pieces owned by player and creates and returns a list of
    those pieces which have available jumps to make currently. - EXPENSIVE"""
    def checkAvailableMoves(self, player, onlyJumps=False):
        
        pieces_coords_where_available_jumps = []
        for row in self.board:
            for tile in row:
                if tile.isTileOccupied and tile.occupyingPiece.player == player:
                    # get tile coords
                    # use the getAvailableMoves
                    result = self.getAvailableMoveCoords(tile.tileCoord, onlyJumps)
                    # if result non [] then this tile should be in the list of available jumps
                    if result:
                        pieces_coords_where_available_jumps.append(tile.tileCoord)
        
        return pieces_coords_where_available_jumps
    
    
    
    """ Takes a list of logical move objects and marks them for highlighting.
    The gui code will then apply the highlights. """
    def plsHighlight(self, lsOfMoves):
        for move in lsOfMoves:
            if move.isJump: #then highlight this one
                xCoord, yCoord = move.pos22[0], move.pos22[1]
                self.board[yCoord][xCoord].isHighlighted = True
            else:
                
                xCoord, yCoord = move.pos11[0], move.pos11[1]
                self.board[yCoord][xCoord].isHighlighted = True
            
        
        
            #self.board[coord]
    """ Takes a list of logical move objects and marks them to be un-highlighted.
    The gui code will apply this change accordingly. """
    def plsUnHighlight(self, lsOfMoves):
        for move in lsOfMoves:
            if move.isJump: #then unhighlight this one
                xCoord, yCoord = move.pos22[0], move.pos22[1]
                self.board[yCoord][xCoord].isHighlighted = False
            else:
                
                xCoord, yCoord = move.pos11[0], move.pos11[1]
                self.board[yCoord][xCoord].isHighlighted = False
        
    
    """Receives a piece as input and returns whether that piece is currently on the corresponding
    King row for that player (that owns the piece). """
    def checkIfPieceOnKingRow(self, somePiece):
        kingRow = 0 if somePiece.player == 'red' else self.size-1
        
        isOnKingRow = kingRow == somePiece.currentPos[1] # eg compares the pieces current y position
        
        return isOnKingRow
    
    
    
        
    """Version 1.0 - moves the occupying piece at tileA to tileB
    both arguments are logicTile tile objects. Also takes care of 
    flagging so the gui knows to update it accordingly. 
    Version 1.1 - as above but uses the tileA and tileB in the lsOfMoves to determine
    which 'move' has been made. This way it will be able to get information about any captured
    piece as well. The function returns the tile / piecew which is captured if so"""        
    def plsMovePiece(self, tileA, tileB, lsOfMoves):
        
        ## work out which move object is been chosen.
        # tileA, b are tile objects, (has x,y coords) lsOfMoves is move objects (only x,y coords)
        theMoveJustMade = None
        moveOutcome = {'piece_captured': None, 'piece_isKinged': False}
        for move in lsOfMoves:
            if move.isJump:
                #then cf with startPos and pos22
                if move.startPos == tileA.tileCoord and move.pos22 == tileB.tileCoord:
                    theMoveJustMade = move
            else:
                # startPos and pos11
                if move.startPos == tileA.tileCoord and move.pos11 == tileB.tileCoord:
                    theMoveJustMade = move
                    
        if theMoveJustMade == None:
            print("Error: board.py (286) move not found in list.")
       
            
        
        #print("28: ", tileA.tileCoord)
        #print("29: ", tileB.tileCoord)
        #print("30: ", move.pos11)
            #if tileA.tileCoord 
        
        
        
        tileB.occupyingPiece = tileA.occupyingPiece
        tileB.occupyingPiece.updateCurrentPos(tileB.tileCoord)
        
        tileB.isTileOccupied = True
        tileB.guiMustBeUpdated = True
        
        tileA.occupyingPiece = ''
        tileA.isTileOccupied = False
        tileA.guiMustBeUpdated = True
        
        if theMoveJustMade.isJump:
            coordJumpedX, coordJumpedY = theMoveJustMade.pos11[0], theMoveJustMade.pos11[1]
            tileJumped = self.board[coordJumpedY][coordJumpedX] # will always contain a piece to remove aswell
            moveOutcome['piece_captured'] = tileJumped.occupyingPiece
            tileJumped.occupyingPiece = ''
            tileJumped.isTileOccupied = False
            tileJumped.guiMustBeUpdated = True
        ## update piece info
        #print("its new pos is ", tileB.tileCoord)
        
        
        ## ADD FUNCTIONALITY FOR DETECTING WHEN REACHED THE END OF THE BOARD AND CHANGE THE PIECE TO A KING
        
        ## moved from A to B
        ## must check if B is the opposite side
        ## - after being made the king, even if it jumps into kings row, the move terminates
        ## - i must change the return-piece method of determining continuous moves
        ## - eg it returns a status code / variable along with it exempting kings from this. 
        ##
        ## do the check and if a king has been made as a result, set 
        ## moveOutcome['piece_isKinged'] = True (after upgrading it too ofc)
        
        ## now look at the piece and check if its reached the end of the board
        
        onKingRow = self.checkIfPieceOnKingRow(tileB.occupyingPiece)
        if tileB.occupyingPiece.ptype != 'd_king' and onKingRow: #eg if not already a king
            #print("the piece should be upgraded now")
            #upgrade to king
            tileB.occupyingPiece.upgradeToKing()
            moveOutcome['piece_isKinged'] = True
        
            
    
    
        
        
        
        
        return moveOutcome # returns the piece which has been jumped if it existed in this move
                            # otherwise None is returned
        
        
        
        