"""
this class is responsiabe for storing all the information about the current state of the chessgame.
it will also responsiabe for determining the valid moves at the current state.it will also keep a move log.
"""

class GameState():
    def __init__(self):
        # board is 8x8 2d list, each elelment of the list has 2 charectors.
        # first charector represents the colour of the piece, 'b' or 'w'
        # second charector represents the type of the piece, 'K', 'Q', 'N', 'B', 'R', or 'P'.
        # "--" - represents empty space with no piece.
        self.board = [
            ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]]
        self.MoveFunctions = {'p': self.getPawnMoves, 'r': self.getRookMoves, 'n': self.getKnightMoves,
                              'b': self.getBishopMoves, 'q': self.getQueenMoves, 'k': self.getKingMoves}

        self.WhiteToMove = True
        self.moveLog = []
        self.WhiteKingLocation = (7, 4)
        self.BlackKingLocation = (0, 4)
        self.inCheck= False
        self.checkMate = False
        self.Stalemate = False
        self.pins = []
        self.checks = []



#  takes move as parameter and excute it(this will not work for castling, pawn pramotion  and en-passant
    def makeMove(self, move):
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.board[move.startRow][move.startCol] = "--"
        self.moveLog.append(move)  # log the move so we can undo it later
        self.WhiteToMove = not self.WhiteToMove #swap players
        # update the king's location if moved
        if move.pieceMoved == 'wk':
            self.WhiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bk':
            self.BlackKingLocation = (move.endRow, move.endCol)

#  this will undo the last move made
    def undoMove(self):
        if len(self.moveLog) != 0: # make sure there is move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.WhiteToMove = not self.WhiteToMove #switch turn back
            # update kings position if needed
            if move.pieceMoved == 'wk':
                self.WhiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bk':
                self.BlackKingLocation = (move.startRow, move.startCol)

#  All moves considering checks
    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.WhiteToMove:
            kingRow = self.WhiteKingLocation[0]
            kingCol = self.WhiteKingLocation[1]
        else:
            kingRow = self.BlackKingLocation[0]
            kingCol = self.BlackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1: #only one check, block check  or move king
                moves = self.getAllPossibleMoves()
                #To block a check you must move a piece into one of the squares between the enemy piece and king
                check = self.checks[0] #check information
                checkRow = check[0]
                checkCol = check[1]
                pieceCheking = self.board[checkRow][checkCol] #enemy piece causing the check
                validSquares = [] # squares that piece can move to
                # if knight, must capture knight or move king,other piece can be blocked
                if pieceCheking[1] == 'n':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i) #check[2] and check[3] are the check directions
                        validSquares.append(validSquare)
                        if validSquares[0] == checkRow and validSquares[1] == checkCol: # once you get to piece end checks
                            break
                # get rid of any moves that don't block check or move king
                for i in range(len(moves)-1, -1, -1): # go through backwards when you are removing from a list as iterating
                    if moves[i].pieceMoved[1] != 'k': # move doesn't move king so it must block or capture
                        if not (moves[i].endRow, moves[i].endCol) in validSquares: # move doesn't block check or capture piece
                            moves.remove(moves[i])
            else:# double check, king has to move
                self.getKnightMoves(kingRow, kingCol, moves)
        else: # not in check so all moves are fine
            moves = self.getAllPossibleMoves()
        if len(moves) == 0:# either checkmate or stalemate
            if self.inCheck:
                self.checkMate = True
            else:
                self.Stalemate = True
        else:
            self.checkMate = False
            self.Stalemate = False
        return moves

    def inCheck(self):
        if self.WhiteToMove:
            return self.squareUnderAttack(self.WhiteKingLocation[0], self.WhiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.BlackKingLocation[0],self.WhiteKingLocation[1])

    def squareUnderAttack(self, r, c):
        self.WhiteToMove = not self.WhiteToMove # switch to opponants turn
        oppMoves = self.getAllPossibleMoves()
        for Move in oppMoves:
            if Move.endRow == r and Move.endCol == c: #square under attack
                self.WhiteToMove = not self.WhiteToMove # switch turns back
                return  True
        self.WhiteToMove = not  self.WhiteToMove


    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):# this is the number of rows
            for c in range(len(self.board[r])): # this is the num of col in given row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.WhiteToMove) or (turn == 'b' and not self.WhiteToMove):
                    piece = self.board[r][c][1]
                    self.MoveFunctions[piece](r, c, moves)
        return moves

    # get all the pawn moves for the pawn located at row, col and add these moves to the list
    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        if self.WhiteToMove: # white pawn move
            if self.board[r-1][c] == "--": # 1 square move
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((r, c),(r-1, c), self.board))
                    if r == 6 and self.board[r-2][c] == "--": # 2 square pawn advance
                        moves.append(Move((r,c), (r-2, c), self.board))
            # capture
            if c-1 >= 0: # capture to the left
                if self.board[r-1][c-1][0] == 'b': # enemy piece to capture
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7: # captres to the right
                if self.board[r-1][c+1][0] == 'b': # enemy piece to capture
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(Move((r, c), (r-1, c+1), self.board))
        else:#black pawn moves
            if self.board[r+1][c] == "--": # 1 square pawn advance
                if not piecePinned or pinDirection == (1, 0):
                    moves.append(Move((r, c),(r+1, c), self.board))
                    if r == 1 and self.board[r+2][c] == "--": # 2 square pawn advance
                        moves.append(Move((r, c), (r+2, c), self.board))
            # capture
            if c-1 >= 0: # capture to the left
                if self.board[r+1][c-1][0] == 'w': # enemy piece to capture
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1 <= 7: # captres to the right
                if self.board[r+1][c+1][0] == 'w': # enemy piece to capture
                    if not piecePinned or pinDirection == (1, 1):
                        moves.append(Move((r, c), (r+1, c+1), self.board))
        # add pawn pramotion later

    # get all the Rook moves for the Rook located at row, col and add these moves to the list
    def getRookMoves(self, r, c, moves): # up, left, down, right
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2],self.pins[i][3])
                if self.board[r][c][1] != 'q': # can't remove quin from pin on rock moves, only remove it on bishop moves.
                    self.pins.remove(self.pins[i])
                break
        directions = ((-1, 0),(0, -1),(1, 0),(0, 1))
        enemyColor = "b" if self.WhiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow <8 and 0 <= endCol < 8: # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": # empty space valid
                        moves.append(Move((r, c),(endRow, endCol),self.board))
                    elif endPiece[0] == enemyColor: #enemy piece valid
                        moves.append(Move((r, c),(endRow, endCol), self.board))
                        break
                    else: # friendly piece invalid
                        break
                else: # off the board
                    break

    # get all the knight moves for the Rook located at row, col and add these moves to the list
    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2),(1,-2),(1, 2),(2,-1),(2,1))
        allyColor = "w" if self.WhiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))


    # get all the bishop moves for the Rook located at row, col and add these moves to the list
    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.WhiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on    board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # friendly piece invalid
                        break
                else:  # off the board
                    break

     # get all the queen moves for the Rook located at row, col and add these moves to the list
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)


    # get all the king moves for the Rook located at row, col and add these moves to the list
    def getKingMoves(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = 'w' if self.WhiteToMove else 'b'
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: # not an ally piece (empty or enemy piece)
                    #place king on end square and check for checks
                    if allyColor == 'w':
                        self.WhiteKingLocation = (endRow, endCol)
                    else:
                        self.BlackKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    # place king back on origional location
                    if allyColor == 'w':
                        self.WhiteKingLocation = (r, c)
                    else:
                        self.BlackKingLocation = (r, c)

    # return if the player in check, a list of pins, and a list of checks
    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.WhiteToMove:
            enemyColor = 'b'
            allyColor = 'w'
            startRow = self.WhiteKingLocation[0]
            startCol = self.WhiteKingLocation[1]
        else:
            enemyColor = 'w'
            allyColor = 'b'
            startRow = self.BlackKingLocation[0]
            startCol = self.BlackKingLocation[1]
        # check outward from king to pins and checks, keep track of pins
        directions = ((-1, 0),(0, -1),(1, 0),(0, 1),(-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = () # reset possible pins
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'k':
                        if possiblePin == (): # 1st allied piece could be pinned
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else: # 2nd allied piece, so no pin or checks possible in this direction
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        # 5 possibility here in complex condition
                        #1) orthogonally away from king and piece is a rook
                        #2) diagonally  away from king and piece is a bishop
                        #3) 1 square away from king and piece is pawn
                        #4) any direction and piece is queen
                        #5) any direction 1 square away and piece is king(this is necessary to prevert a king move to a square controlled by the other king)
                        if (0 <= j <= 3 and type =='r') or \
                                (4 <= j <= 7 and type == 'b') or \
                                (i == 1 and type == 'p' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <=5   ))) or \
                                (type == 'q') or (i == 1 and type == 'k'):
                            if possiblePin == ():# no piece blocking so check
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else: # piece is blocking so pin
                                pins.append(possiblePin)
                                break
                        else:# enemy piece is not applying check
                            break
                else:
                    break # off board
        # check for knight check
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'n':# enemy knight attacking king
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks

class Move():
    # map keys to values
    # key : value
    ranksToRows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    rowToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v:k for k, v in filesToCols.items()}

    def __init__(self, startsq, endsq, board):
        self.startRow = startsq[0]
        self.startCol = startsq[1]
        self.endRow = endsq[0]
        self.endCol = endsq[1]
        self.pieceMoved =board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 +self.endCol


    # overriding the equals method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        # you can add to make this like real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)


    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowToRanks[r]
