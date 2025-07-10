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
    
    count_X = sum(row.count('X') for row in board)
    count_O = sum(row.count('O') for row in board)
    
    if count_X == count_O:
        return 'X'
    
    return 'O'

    # raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    
    action = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] not in ['X', 'O']:
                action.add((i, j))

    return action

    # raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    if board[i][j] is not None:
        raise Exception("ERROR!")

    player_turn = player(board)

    # Deepcopy()
    new_board = copy.deepcopy(board)
    new_board[i][j] = player_turn

    return new_board
    
    # raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    # Check for horizontal line and vertical line
    for player in ['X', 'O']:
        for i in range(3):
            if all(board[i][j] == player for j in range(3)):
                return player
        for j in range(3):
            if all(board[i][j] == player for i in range(3)):
                return player
            
    # Check for diagonal line 
    if board[0][0] == board[1][1] == board[2][2] or board[0][2] == board[1][1] == board[2][0]:
        return board[1][1]
    
    # raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    
    if winner(board) is not None or all(board[i][j] is not None for i in range(3) for j in range(3)):
        return True
    return False
    
    # raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    
    if winner(board) == 'X':
        return 1
    elif winner(board) == 'O':
        return -1
    else:
        return 0
    
    # raise NotImplementedError

'''
MINIMAX 

def minimax(board):
    """
    Returns the optimal move for the current player on the board.
    """
    if terminal(board):
        return None

    player_turn = player(board)

    if player_turn == 'X':
        best_value = float("-inf")
        best_move = None
        for action in actions(board):
            move_value = min_value(result(board, action))
            if move_value > best_value:
                best_value = move_value
                best_move = action
    else:
        best_value = float("inf")
        best_move = None
        for action in actions(board):
            move_value = max_value(result(board, action))
            if move_value < best_value:
                best_value = move_value
                best_move = action

    return best_move

    # raise NotImplementedError
    

def max_value(board):
    if terminal(board):
        return utility(board)

    v = float("-inf")
    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v


def min_value(board):
    if terminal(board):
        return utility(board)

    v = float("inf")
    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v
'''

'ALPHA BETA PRUNING'

def minimax(board):
    """
    Returns the optimal move for the current player on the board.
    """
    if terminal(board):
        return None

    player_turn = player(board)

    if player_turn == 'X':
        return max_value(board, float("-1"), float("1"))[1]
    else:
        return min_value(board, float("-1"), float("1"))[1]
    
    # raise NotImplementedError


def max_value(board, alpha, beta):
    if terminal(board):
        return (utility(board), None)

    v = float("-1")
    best_move = None
    for action in actions(board):
        move_value = min_value(result(board, action), alpha, beta)[0]
        if move_value > v:
            v = move_value
            best_move = action
        alpha = max(alpha, v)
        if alpha >= beta:
            break
        
    return (v, best_move)


def min_value(board, alpha, beta):
    if terminal(board):
        return (utility(board), None)

    v = float("1")
    best_move = None
    for action in actions(board):
        move_value = max_value(result(board, action), alpha, beta)[0]
        if move_value < v:
            v = move_value
            best_move = action
        beta = min(beta, v)
        if alpha >= beta:
            break
        
    return (v, best_move)
