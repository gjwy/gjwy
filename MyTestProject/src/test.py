""" Gareth Wilson
    7-Dec-14 """
    

from board import GameBoard

internalBoardRepresentation = GameBoard()

db = internalBoardRepresentation.getDisplayBoard()
for r in db:
    print(r)
    

    
print('\n')
print(internalBoardRepresentation.board[6][3].occupyingPiece.posHistory)
    
    
    
    
# internal representation     (update mrepr)
#print('\n\n\n\n')
#for r in internalBoardRepresentation.board:
#    print('===ROW===\n')
#    for t in r:
#        print(t.mrepr())
#    print('\n')
    