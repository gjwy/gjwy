""" Gareth Wilson
    13-Feb-15 """
    

"""Each position will be a coord in [x, y] format. """
class Move():
    def __init__(self, startPos, pos11, pos22):
        self.startPos = startPos
        self.pos11 = pos11
        self.pos22 = pos22
        self.isJump = False
            