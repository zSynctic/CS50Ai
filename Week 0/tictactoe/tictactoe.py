"""
Tic Tac Toe Player
"""

import math
import copy

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
    countX = 0
    countO = 0
    
    # If the board is in its initial state, X plays first
    if board == initial_state():
        return X
    
    # Count the number of X's and O's on the board
    for row in board:
        for cell in row:
            if cell == X:
                countX += 1
            elif cell == O:
                countO += 1
            else:
                continue
    
    # If there are fewer O's than X's, it's O's turn; if equal, it's X's turn
    if countO < countX:
        return O
    elif countX == countO:
        return X
    else:
        return EMPTY
    

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    
    # Create an empty set to store available moves
    available_moves = set()
    
    # Iterate through the board to find empty available cells and add their coordinates to the set
    for row_index, row in enumerate(board):
        for col_index, cell in enumerate(row):
            if cell == EMPTY:
                available_moves.add((row_index, col_index))
                
    return available_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    # Check for invalid moves
    if i < 0 or i > 2 or j < 0 or j > 2:
        raise Exception("Invalid action: out of bounds")
    if board[i][j] != EMPTY:
        raise Exception("Invalid action: cell already taken")

    # Create a deep copy of the board to avoid mutating the original board
    board_copy = copy.deepcopy(board)
    
    # Place the player's mark on the board
    if player(board) == X:
        board_copy[i][j] = X
    elif player(board) == O:
        board_copy[i][j] = O
    else:
        raise Exception("No player to make a move")
    
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check for rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != EMPTY:
            return row[0]
    
    # Check for columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != EMPTY:
            return board[0][col]
    
    # Check for diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    if board[2][0] == board[1][1] == board[0][2] and board[0][2] != EMPTY:
        return board[2][0]

    # Return None if there is no winner of the game (either because the game is still on or a tie)
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    
    # Check for rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != EMPTY:
            return True
            
    # Check for columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != EMPTY:
            return True

    # Check for diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return True
    if board[2][0] == board[1][1] == board[0][2] and board[0][2] != EMPTY:
        return True
    
    # check for empty spaces and tie
    for row in board:
        if EMPTY in row:
            return False 
    
    # Returns true if all winning conditions are false and there is no empty spaces so its a tie
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    
    # Check for the winner and return 1 if X wins, -1 if O wins, and 0 for a tie or ongoing game
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    # Base case: if the game is over, return None (no moves left)
    if terminal(board):
        return None
    
    # Determine the current player
    current_player = player(board)
    
    # If the current player is O (minimizing player), we want to minimize the score
    if current_player == O:
        best_value = math.inf
        best_action = None
        for action in actions(board):
            v = MaxValue(result(board, action))
            if v < best_value:
                best_value = v
                best_action = action
        return best_action
    
    # If the current player is X (maximizing player), we want to maximize the score
    if current_player == X:
        best_value = -math.inf
        best_action = None
        for action in actions(board):
            v = MinValue(result(board, action))
            if v > best_value:
                best_value = v
                best_action = action
        return best_action

def MaxValue(board):

    v = -math.inf

    # Base case: if the game is over, return the utility value of the board
    if terminal(board):
        return utility(board)

    # Explore all possible actions and choose the one that maximizes the score
    for action in actions(board):
        v = max(v, MinValue(result(board, action)))

    return v

def MinValue(board):

    v = math.inf

    # Base case: if the game is over, return the utility value of the board
    if terminal(board):
        return utility(board)

    # Explore all possible actions and choose the one that minimizes the score
    for action in actions(board):
        v = min(v, MaxValue(result(board, action)))

    return v