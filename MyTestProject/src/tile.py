""" Gareth Wilson
    13-Feb-15 """

""" The logical tile object (which makes up the internal board) and which can contain pieces
which are placed onto it. """
class Tile():
    
    # fields: color, coords are external, possible moves
    def __init__(self):
        self.isTileOccupied = False
        self.occupyingPiece = ''
        self.tileIcon = ''
        self.isPieceKing = False
        self.tileCoord = ''
        self.isHighlighted = False
        self.guiMustBeUpdated = True
    
  
    
    """ Gets the icon for this tile, if the tile has an occupying piece it uses this piece icon,
        otherwise uses the default icon for that tile (black/white). 
        ~~ Not used. Will be reasonably updated and reused. """
    def getIcon(self):
        if self.isTileOccupied:               # delete
            icon = self.occupyingPiece.getPieceIcon() #todo
        else:
            self.img = Image.open("tatras.jpg")
            self.tatras = ImageTk.PhotoImage(self.img)
            icon = self.tileIcon
        return icon
    
    
    """ Debugs ~~ Not used. """
    def mrepr(self):
        repStr = 'occupied: ' + str(self.isTileOccupied) + '\ncolour: ' + self.tileIcon + '\nking: ' + str(self.isPieceKing)
        return repStr
    
    
    """ Returns the tile tag to be used to tag the tile. The tag must be unique thus is derived from
    the coordinates + 'uniqueString' since an auto tag was basically similar format using numbers. 
    ~~ Not used. -? just for testing the gui. """
    def getTileTag(self):
        return str(self.tileCoord[0]) + str(self.tileCoord[1])
    
    
    """Version 1 : returns all diagonal pieces from this tile, that it 
    could potentially move to before sanity checking
    ~~ Not used. - I believe this has been replaced by the piece-rule code. """
    def getValidMoves(self):
        # returns them as a list of tuple coords
        
        # assert(self.tileCoord != '')
        x, y = self.tileCoord[0], self.tileCoord[1]
        adjDiagPos = []
        #diagonals
        #when it goes off left side (-1) that goes to end of array (-1) which is wrong 
        #and when it goes off right (8) that is out of range of the 7len list cause error
        adjDiagPos.append((x+1, y-1))
        adjDiagPos.append((x+1, y+1))
        adjDiagPos.append((x-1, y-1))
        adjDiagPos.append((x-1, y+1))
        
        # print(adjDiagPos)
        return adjDiagPos
    