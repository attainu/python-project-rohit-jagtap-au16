# CHESS GAME
##Requirements
    1.Pycharm
    2.python
    3.pygame

his program runs a virtual chess game by initializing the pieces and keeping track of their movements across the board. The challenge of this game is ensuring that all moves are legal. The important tasks it must accomplish are listed below. They form a basic summary of the main while loop that controls the program.
 
    1. Initialize a game containing an object for each piece on the board.
    2. Draw the board and pieces.
    3. Confirm that the king is not in checkmate or stalemate otherwise end the game
    4. Get user input and confirm the input is valid or otherwise get new input.
    5. Check target space. If blocked, get new input. If empty or guarded, store that information.
    6. Find all pieces which match the move input and can legally carry out the move. If none are found, get new input.
    7. Of the legal pieces which match the input, find all pieces whose paths are clear based on the movement rules for each chess piece type. If none are found, get new input.
    8. If u get check from one direction you can either block check or you have to move the king
    9. if your king get check from two directions, you have to move your king
    10. Repeat steps 2-10 until checkmate is achieved.
    11. Highlight all gthe possible moves for selected pawn
    12. If king is in check you can not move another piece if that piece doesn’t block check.
    13. Pins it will pin your pawn which is between your king and opponants pawn.

The motivation behind this program is to eventually use it to control a physical chess board which controls the movement of pieces for the players based on some kind of computer input (whether that is typing, talking or some other form). Hopefully, this could eventually become a set of two remote chess boards, such that players could play physical chess games with anybody, anywhere.
Additional features: undo – highlight possible moves undoes last move quit - quits the game and closes the pygame window reset - resets the game- it will restart the game and undo all the previous moves

Keywords to make your game easy :

q -> Quit game.

r -> Reset game.

z -> undo the last move.

#Note
    if u open this game in vscode it will show An export error which thats why you should prefer pychar over vs code to run this game
