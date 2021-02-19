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
            ["--", "--", "--", "--", "bp", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]]
        self.MoveFunctions = {'p': self.getPawnMoves, 'r': self.getRookMoves, 'n': self.getKnightMoves,
                              'b': self.getBishopMoves, 'q': self.getQueenMoves, 'k': self.getKingMoves}

        self.WhiteToMove = True
        self.moveLog = []

#  takes move as parameter and excute it(this will not work for castling, pawn pramotion  and en-passant
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log the move so we can undo it later
        self.WhiteToMove = not self.WhiteToMove #swap players

#  this will undo the last move made
    def undoMove(self):
        if len(self.moveLog) != 0: # make sure there is move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.WhiteToMove = not self.WhiteToMove #switch turn back

#  All moves considering checks
    def getValidMoves(self):
        return self.getAllPossibleMoves() # for now we will not worry anout checks

# All moves without considering checks
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):# this is the number of rows
            for c in range(len(self.board[r])): # this is the num of col in given row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.WhiteToMove) or (turn == 'b' and not self.WhiteToMove):
                    piece = self.board[r][c][1]
                    self.MoveFunctions[piece](r, c, moves) #call the appropriate move function based on piece type
        return moves

# get all the pawn moves for the pawn located at row, col and add these moves to the list
    def getPawnMoves(self, r, c, moves):
        if self.WhiteToMove: # white pawn move
            if self.board[r-1][c] == "--": # 1 square pawn advance
                moves.append(Move((r, c),(r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--": # 2 square pawn advance
                    moves.append(Move((r,c), (r-2, c), self.board))
            if c-1 >= 0: # capture to the left
                if self.board[r-1][c-1][0] == 'b': # enemy piece to capture
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7: # captres to the right
                if self.board[r-1][c+1][0] == 'b': # enemy piece to capture
                    moves.append(Move((r, c), (r-1, c+1), self.board))
        else:#black pawn moves
            if self.board[r+1][c] == "--": # 1 square pawn advance
                moves.append(Move((r, c),(r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--": # 2 square pawn advance
                    moves.append(Move((r,c), (r+2, c), self.board))
            # capture
            if c-1 >= 0: # capture to the left
                if self.board[r+1][c-1][0] == 'w': # enemy piece to capture
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1 <= 7: # captres to the right
                if self.board[r+1][c+1][0] == 'w': # enemy piece to capture
                    moves.append(Move((r, c), (r+1, c+1), self.board))
        # add pawn pramotion later

# get all the Rook moves for the Rook located at row, col and add these moves to the list
    def getRookMoves(self, r, c, moves): # up, left, down, right
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


# get all the king moves for the Rook located at row, col and add these moves to the list
    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, 1), (0, -1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.WhiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

# get all the queen moves for the Rook located at row, col and add these moves to the list
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

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
