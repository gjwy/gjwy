""" Gareth Wilson
    13-Feb-15 """

from rules import Rules
from move import Move


""" The logical Piece object class. This is used within the logical game board tiles. A tile 
may contain a piece and the piece can be moved from one tile to another. The piece also has 
access to the rules governing the types of moves it may make. """
class Piece():
    def __init__(self, player, ptype, initialPos):
        self.player = player
        self.ptype = ptype # eg pawn
        self.currentPos = initialPos
        self.posHistory = [initialPos]
        self.icon = 'navajo white' if player == 'white' else 'red' #todo
        # id = rndm (
        # TODO: generates unique id for that piece
        # fro tracking purposes
        # MAKE initial position be given its coords
        # requires changing populate function to
        # include X instead of for tile in row..
        
    # for any time the piece is now moved, the coord
    # will be added to the posHistory by use of a 
    # method
    
    """Allows the current coordinate position to be updated. Also takes care of keeping 
    a record of the piece's position history over the board - might be helpful for undoing
    moves etc. """
    def updateCurrentPos(self, newPos):
        self.posHistory.append(self.currentPos)
        self.currentPos = newPos
    
    """Return a list of available moves (coords) ignoring board-level constraints, according simply to 
    the rules governing that piece type. """
    def getAvailableMoves(self):
        #availableMoves = []
        #look up rules governing this piece's type
        
        #player is needed since different perspectives of the board
        #patterns = Rules.getPattern(self, self.ptype, self.player)
        #print("patterns are ", patterns)
        #x, y = self.currentPos[0], self.currentPos[1]
        #print("originals: ", x, y)
        #for pattern in patterns: #dict obj in list
            # replace the x,y with rules
            #available_x = x + pattern['x']
            #available_y = y + pattern['y']
            #availableMoves.append([available_x, available_y])
            
        #return availableMoves
        
        startX, startY = self.currentPos[0], self.currentPos[1]
        
        listOfMoves = []
        
        #these moves are the east and west moves in the direction of the players corresponding facing direction eg
        if self.ptype in ['d_men', 'd_king']: # eg yDirwest and east gotten for either of those pieces
            
            yDirWest = Rules.getDraughtsmanYDirWest(self, self.player)
            pos11X, pos11Y = startX + yDirWest['pos1x'], startY + yDirWest['pos1y']
            pos22X, pos22Y = startX + yDirWest['pos2x'], startY + yDirWest['pos2y']
            yDirwMove = Move( (startX, startY), (pos11X, pos11Y), (pos22X, pos22Y) )
            
            
            
            yDirEast = Rules.getDraughtsmanYDirEast(self, self.player)
            pos11X, pos11Y = startX + yDirEast['pos1x'], startY + yDirEast['pos1y']
            pos22X, pos22Y = startX + yDirEast['pos2x'], startY + yDirEast['pos2y']
            yDireMove = Move( (startX, startY), (pos11X, pos11Y), (pos22X, pos22Y) )
            
            listOfMoves.append(yDirwMove)
            listOfMoves.append(yDireMove)
        # these moves are additional ones for the king and they include the opposite y directions (eeg back
        # towards that player )
        if self.ptype in ['d_king']:
            otherYDirWest = Rules.getKingOtherYDirWest(self, self.player)
            pos11X, pos11Y = startX + otherYDirWest['pos1x'], startY + otherYDirWest['pos1y']
            pos22X, pos22Y = startX + otherYDirWest['pos2x'], startY + otherYDirWest['pos2y']
            otherYDirwMove = Move( (startX, startY), (pos11X, pos11Y), (pos22X, pos22Y) )
            
            
            
            otherYDirEast = Rules.getKingOtherYDirEast(self, self.player)
            pos11X, pos11Y = startX + otherYDirEast['pos1x'], startY + otherYDirEast['pos1y']
            pos22X, pos22Y = startX + otherYDirEast['pos2x'], startY + otherYDirEast['pos2y']
            otherYDireMove = Move( (startX, startY), (pos11X, pos11Y), (pos22X, pos22Y) )
            
            listOfMoves.append(otherYDirwMove)
            listOfMoves.append(otherYDireMove)
            
        return listOfMoves
    
    
    
    def upgradeToKing(self): #method which upgrades the type and icon etc
        self.ptype = 'd_king'
        self.icon = 'red4' if self.player == 'red' else 'NavajoWhite3' # change all this shit to images for now ..
        
        
    ## ALTERNATIVE
    # if ptype == draughtsmen
    # getmoveNE, getMoveNW (gets the patterns) then use original x,y like above to make move object
    # for all of these move objects, if landingTile is occupied by oposition, then get corresponding 
    # jump move
    
    #return all the move objects
            
            
        
        
        