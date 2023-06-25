"""
Tic Tac Toe Player
"""

from copy import deepcopy
import math
from queue import Empty

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Turn counter
    turns = 0

    # Count non empty squares
    for row in board:
        for cell in row:
            if cell is not EMPTY:
                turns += 1
    
    # If no move or even number of moves are played return X else O if odd number of moves are played
    return X if turns % 2 == 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    
    # Initialize a set of all moves possible
    moves = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                moves.add((i, j))
    
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    newBoard = deepcopy(board)
    i, j = action

    if newBoard[i][j] != EMPTY:
        raise Exception("not a valid move")
    else:
        newBoard[i][j] = player(board)

    return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    # Horizontal
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]

    # Vertical
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]

    # Diagonal
    if (board[0][0] == board[1][1] == board[2][2] != EMPTY) or (board[0][2] == board[1][1] == board[2][0] != EMPTY):
        return board[1][1]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    
    # If there is a winner -> terminal
    if winner(board) == X or winner(board) == O:
        return True
    
    # If there is no winner but there is an empty space -> not terminal
    for row in board:
        for cell in row:
            if cell is EMPTY:
                return False
    
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action(1,1)for the current player on the board.
    """
    if terminal(board):
        return None
    
    if player(board) == X:
        moves = []
        for action in actions(board):
            moves.append((max_value(result(board, action)), action))
        moves.sort()        # Sort by value -> low to high 
        return moves[-1][1] # Return action (x,y) of the highest value i.e moves = [......, (. , .), ( 1 , (x,y) )]

    elif player(board) == O:
        moves = []
        for action in actions(board):
            moves.append((min_value(result(board, action)), action))
        moves.sort()        # Sort by value -> low to high
        return moves[0][1]  # Return action (x,y) of the least value i.e moves = [( -1 , (x,y) ), (. , .), ......]


def max_value(board):
    """
    Returns max value in current state
    """
    if terminal(board):
        return utility(board)

    v = -math.inf

    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    
    return v


def min_value(board):
    """
    Returns min value in current state
    """
    if terminal(board):
        return utility(board)

    v = math.inf
    
    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v

def main():
    board = [[O, O, X],
             [EMPTY, X, O],
             [EMPTY, EMPTY, X]]
    minimax(board)

if __name__ == "__main__":
    main()