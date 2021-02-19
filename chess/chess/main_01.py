"""
this is our main driver file.it will be resposable for handling useer input and displaying game current GameState object.
"""

import pygame as p
from chess import chessEngine

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
    LoadImages()  #only do this once, before the while loop.
    running = True
    SQ_SELECTED = () #no square is selected,keep track of the last click of the user (tuple: (row,col))
    PLAYERCLICKS = [] #keep track of the player clicks (two tuples: [(6,4),(4,4)]
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
                    SQ_SELECTED = () # reset user clicks
                    PLAYERCLICKS = [] #
            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # it will undo when z is pressed
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

# responsibale for the grapnics with in current game state.
def drawGameState(screen, gs):
    drawBoard(screen) # draw square on the board
    drawPieces(screen, gs.board) #draw pieces on the top of the squares

# draw the squares on the board
def drawBoard(screen):
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


if __name__ == '__main__':
    main()
