"""
this is our main driver file.it will be resposable for handling useer input and displaying game current GameState object.
"""

import pygame as p
from chess import chessEngine
# from chess.chessEngine import moves

WIDTH = HEIGHT = 512
DIMENSION = 8 # DIMENSION OF THE CHESS BOARD 8X8.
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 30 # FOR ANIMATION LATER PART
IMAGES = {}

# initialize a global dictionary of images. this will be called exactly once in the main

def LoadImages():
    pieces = ['wp', 'wr', 'wk', 'wn', 'wq', 'wb', 'bp', 'br', 'bk', 'bn', 'bq', 'bb']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
        # we can access an image by saying 'IMAGES['wp']'

# the main driver for our code. this will handel user input and updating the graphics.

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag veriable for when a move is made
    Animate = False # flag veriable for when we should animate a move
    LoadImages()  #only do this once, before the while loop.
    running = True
    SQ_SELECTED = () #no square is selected,keep track of the last click of the user (tuple: (row,col))
    PLAYERCLICKS = [] #keep track of the player clicks (two tuples: [(6,4),(4,4)]
    p.display.set_caption("Chess with Rohit")

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x,y) location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if SQ_SELECTED == (row, col):#the user click the same square twice.
                    SQ_SELECTED = () # deselect
                    PLAYERCLICKS = [] #clear players clicks
                else:
                    SQ_SELECTED = (row, col)
                    PLAYERCLICKS.append(SQ_SELECTED)# append both first and second clicks
                if len(PLAYERCLICKS) == 2: #this is after second click
                    move = chessEngine.Move(PLAYERCLICKS[0], PLAYERCLICKS[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        Animate = True
                        SQ_SELECTED = () # reset user clicks
                        PLAYERCLICKS = [] #
                    else:
                        PLAYERCLICKS = [SQ_SELECTED]
            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # it will undo when z is pressed
                    gs.undoMove()
                    moveMade = True
                    Animate = False
                if e.key == p.K_r: # reset the board when r is pressed
                    gs = chessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    SQ_SELECTED = ()
                    PLAYERCLICKS = []
                    moveMade = False
                    Animate = False

        if moveMade:
            if Animate:
                AnimateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            Animate = False

        drawGameState(screen, gs, validMoves, SQ_SELECTED)
        clock.tick(MAX_FPS)
        p.display.flip()

# highlight square selected and moves for piece sselected
def HighlightSquare(screen, gs, validMoves,SQ_SELECTED):
    if SQ_SELECTED != ():
        r, c = SQ_SELECTED
        if gs.board[r][c][0] == ('w' if gs.WhiteToMove else 'b'):# sq selected a piece that can be moved
            # highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) # transparency value
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
# highlight square from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))




# responsibale for the grapnics with in current game state.
def drawGameState(screen, gs, validMoves, SQ_SELECTED):
    drawBoard(screen) # draw square on the board
    drawPieces(screen, gs.board) #draw pieces on the top of the squares
    HighlightSquare(screen, gs, validMoves, SQ_SELECTED)

# draw the squares on the board
def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("light blue")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))



# draw pieces on the board using the current GameState.board
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": # not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

#  this function is animating move
def AnimateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10 # frames to move one square
    frameCount = (abs(dR)+ abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = ((move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount))
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from it' ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        # draw the captured piece onto rectangle
        if move.pieceCaptured != "--":
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # draw the moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)




if __name__ == '__main__':
    main()
