""" Gareth Wilson
    13-Feb-15 """

class Rules():
    
    
    """player refers to which side of the board the piece 
    faces, white (close side) or red (far side). The player on the opposite
    side of the board's pieces will be advancing down the -y rather than the +y
    so the piece rules must be adjusted here."""
    
    def getPattern(self, ptype, player, isJump=False):
        
        yDirection = -1 if player == "red" else 1
        
        if ptype == 'd_men':
            availableMoves = [{'x': 1, 'y': 1}, {'x': -1, 'y': 1}]
            
            
            
            
        # finally multiply each occurrence of the y value with the adjusted yDirection
        for move in availableMoves:
            move['y'] *= yDirection
            
            
        return availableMoves
    
    
    def getDraughtsmanYDirWest(self, player): # add nw tag?
        yDirection = -1 if player == "red" else 1
        yw = {'pos1x': -1, 'pos1y': 1 * yDirection, 'pos2x': -2, 'pos2y': 2 * yDirection}
        return yw
    
    
    def getDraughtsmanYDirEast(self, player):
        yDirection = -1 if player == "red" else 1 # eg the away from player y direction
        ye = {'pos1x': 1, 'pos1y': 1 * yDirection, 'pos2x': 2, 'pos2y': 2 * yDirection}
        return ye
    
    def getKingOtherYDirWest(self, player):
        yDirection = 1 if player == "red" else -1
        otheryw = {'pos1x': -1, 'pos1y': 1 * yDirection, 'pos2x': -2, 'pos2y': 2 * yDirection}
        return otheryw
    
    def getKingOtherYDirEast(self, player):
        yDirection = 1 if player == "red" else -1 # eg the away from player y direction
        otherye = {'pos1x': 1, 'pos1y': 1 * yDirection, 'pos2x': 2, 'pos2y': 2 * yDirection}
        return otherye


            