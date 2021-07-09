#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""
Adversarial search algorithms implementation

Your task for homework 5 is to implement:
1.  minimax
2.  alphabeta
3.  abdl (alpha beta depth limited)
"""
import random
import sys
from tictactoe import GameState


def rand(game_state):
    """
    Generate a random move.
    :param game_state: GameState object
    :return:  a tuple representing the row column of the random move
    """
    done = False
    while not done:
        row = random.randint(0, game_state.size - 1)
        col = random.randint(0, game_state.size - 1)
        if game_state.available(row, col):
            done = True
    return row, col


def minimax(game_state: GameState, player, depth):
    """
    Find the best move for our AI agent by applying the minimax algorithm
    (searching the entire tree from the current game state)
    :param game_state: GameState object
    :return:  a tuple representing the row column of the best move

    function minimax(node, depth, maximizingPlayer) is
        if depth = 0 or node is a terminal node then
            return the heuristic value of node
        if maximizingPlayer then
            value := −∞
            for each child of node do
                value := max(value, minimax(child, depth − 1, FALSE))
            return value
        else (* minimizing player *)
            value := +∞
            for each child of node do
                value := min(value, minimax(child, depth − 1, TRUE))
            return value
    """
    d = 0
    if game_state.is_win('user') or game_state.is_win('AI') or game_state.is_tie() or d > depth:
        # here we are returning a invalid move because no move needed here
        return game_state.eval(), (-1, -1)

    if player == 'AI':
        best_score = -sys.maxsize
        best_move = (-1, -1)
        for move in game_state.possible_moves():
            # Making an independent successor node to pass to child minimax calls
            # So we don't have to undo this move.
            next_state = game_state.successor(move, player)
            d += 1

            # Here we are receiving 2 value from child calls. first one is score of this current state
            # and second one is best move from child state. We can ignore that move. So using _
            # But you need this move in the root caller of this minimax(). I mean who calls this first.
            # there you need to catch value like:
            # best_score, best_move = minimax(initial_state, initial_player, total depth)
            # then you can make best_move to achieve that best_score
            score, _ = minimax(next_state, 'user', depth - 1)

            # Here we are maximizing our advantage. I mean we are seeking best state for AI
            # Also saving which move is causing this so far best_score
            best_score = max(score, best_score)
            best_move = max(best_move, move)
            # if score > best_score:
            #  best_score = score
            # best_move = move
        return best_score, best_move
    else:
        best_score = sys.maxsize
        best_move = (-1, -1)
        for move in game_state.possible_moves():
            next_state = game_state.successor(move, player)
            d += 1
            score, _ = minimax(next_state, 'AI', depth - 1)

            # Here we are maximizing our advantage. Here maximizing means, minimizing AI's advantage
            # Also saving which move is causing this so far best_score
            if score < best_score:
                best_score = score
                best_move = move
        return best_score, best_move


def value(game_state, player):
    """
    Calculate the minimax value for any state under the given agent's control
    : param game_state: GameState object - state may be terminal or non-terminal
    : param player: (string) 'user' or 'AI' - AI is max
    : return: (integer) value of that state - 1, 0 or 1
    """
    if game_state.is_win('AI'):
        return 1
    if game_state.is_win('user'):
        return -1
    if game_state.is_tie():
        return 0
    # If the agent is MAX return max-value
    if player is 'AI':
        return max_value(game_state)
    # If the agent is MIN return min-value
    return min_value(game_state)


def max_value(game_state):
    """
    Calculate the minimax value for a non-terminal state under Max's
    control(AI agent)
    : param game_state: non-terminal GameState object
    : return: (integer) value of that state - 1, 0 or 1
    """
    v = -sys.maxsize
    for move in game_state.possible_moves():
        v1 = value(game_state.successor(move, 'AI'), 'user')  # not good
        tup = [v, v1]
        # print("TUP", tup)
        v = max(tup)
        # print('MAX: ', v)
    return v


def min_value(game_state):
    """
    Calculate the minimax value for a non-terminal state under Min's
    control(user)
    : param game_state: non-terminal GameState object
    : return: (integer) value of that state - 1, 0 or 1
    """
    # Enter your code here and remove the pass statement below
    v = sys.maxsize
    for move in game_state.possible_moves():
        v1 = value(game_state.successor(move, 'user'), 'AI')  # little gud
        tup = [v, v1]
        # print("TUP", tup)
        v = min(tup)
        # print('MIN: ', v)
    return v

def alphabeta(game_state: GameState, player, depth):
    """
    Find the best move for our AI agent by applying the minimax algorithm
    with alpha beta pruning.
    : param game_state: GameState object
    : return:  a tuple representing the row column of the best move
                    o          depth:0
                 /     \
                1       1        depth: 1
               /  \    /  \
             o     o   o    o      depth: 2
    """
    # Enter your code here and remove the raise statement below\
    d = 0
    best_move = (-1, -1)
    alpha = -sys.maxsize
    beta = sys.maxsize

    if game_state.is_win('AI') or game_state.is_win('user') or game_state.is_tie() or depth == 0:
        return game_state.eval(), (-1, -1)

    if player == 'user':
        best_score = -sys.maxsize

        for move in game_state.possible_moves():
            next_state = game_state.successor(move, player)
            score, _ = alphabeta(next_state, 'AI', depth - 1)
            # value = max(value, alphabeta(move, depth - 1, 'user', alpha, beta))
            alpha = max(alpha, score)
            if score > best_score:
                best_score = score
                best_move = move
            if alpha >= beta:
                break
        return best_score, best_move
    else:
        best_score = sys.maxsize

        for move in game_state.possible_moves():
            next_state = game_state.successor(move, player)
            # d += 1
            # s = abmin_value(move, alpha, beta)
            score, _ = alphabeta(next_state, 'user', depth - 1)
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, score)
            if beta <= alpha:
                break
        return best_score, best_move


def ab_value(game_state, player, alpha, beta):
    """
    Calculate the minimax value for any state under the given agent's control
    using alpha beta pruning
    : param game_state: GameState object - state may be terminal or non-terminal
    : param player: (string) 'user' or 'AI' - AI is max
    : return: (integer) value of that state - 1, 0 or 1
    """
    # Enter your code here and remove the pass statement below
    if game_state.is_win('AI'):
        return 1
    if game_state.is_win('user'):
        return -1
    if game_state.is_tie():
        return 0
    # If the agent is MAX return max-value
    if player is 'AI':
        return abmax_value(game_state, alpha, beta)
    # If the agent is MIN return min-value
    return abmin_value(game_state, alpha, beta)


def abmax_value(game_state, alpha, beta):
    """
    Calculate the minimax value for a non-terminal state under Max's
    control(AI agent) using alpha beta pruning
    : param game_state: non-terminal GameState object
    : return: (integer) value of that state - 1, 0 or 1
    """
    # Enter your code here and remove the pass statement below
    a = alpha
    v = -sys.maxsize
    for move in game_state.possible_moves():
        v = max([v, ab_value(game_state.successor(move, 'AI'), 'user', a, beta)])
        if v >= beta:
            return v
        a = max(a, v)
    return v


def abmin_value(game_state, alpha, beta):
    """
    Calculate the minimax value for a non-terminal state under Min's
    control(user) using alpha beta pruning
    : param game_state: non-terminal GameState object
    : return: (integer) value of that state - 1, 0 or 1
    """
    # Enter your code here and remove the pass statement below
    b = beta
    v = sys.maxsize
    for move in game_state.possible_moves():
        v = min([v, ab_value(game_state.successor(move, 'user'), 'AI', alpha, b)])
        if v <= alpha:
            return v
        b = min([b, v])
    return v


def abdl(game_state : GameState, player, depth):
    """
    Find the best move for our AI agent by limiting the alpha beta search to
    the given depth and using the evaluation function game_state.eval()
    : param game_state: GameState object
    : return:  a tuple representing the row column of the best move
    """
    best_move = (-1, -1)
    alpha = -sys.maxsize
    beta = sys.maxsize

    if game_state.is_win('AI') or game_state.is_win('user') or game_state.is_tie() or depth == 0:
        return game_state.eval(), (-1, -1)

    if player == 'user':
        best_score = -sys.maxsize

        for move in game_state.possible_moves():
            next_state = game_state.successor(move, player)
            score, _ = alphabeta(next_state, 'AI', depth - 1)
            # value = max(value, alphabeta(move, depth - 1, 'user', alpha, beta))
            alpha = max(alpha, score)
            if score > best_score:
                best_score = score
                best_move = move
            if alpha >= beta:
                break
        return best_score, best_move
    else:
        best_score = sys.maxsize

        for move in game_state.possible_moves():
            next_state = game_state.successor(move, player)
            # d += 1
            # s = abmin_value(move, alpha, beta)
            score, _ = alphabeta(next_state, 'user', depth - 1)
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, score)
            if beta <= alpha:
                break
        return best_score, best_move


def abdl_value(game_state, player, alpha, beta, depth):
    """
    Calculate the utility for any state under the given agent's control
    using depth limited alpha beta pruning and the evaluation
    function game_state.eval()
    : param game_state: GameState object - state may be terminal or non-terminal
    : param player: (string) 'user' or 'AI' - AI is max
    : return: (integer) utility of that state
    """
    # Enter your code here and remove the pass statement below
    if player == 'AI' and game_state.is_win('AI'):
        return 1
    if player == 'user' and game_state.is_win('user'):
        return -1
    if game_state.is_tie():
        return 0
    if depth == 0:
        return game_state.eval()
    # If the agent is MAX return max-value
    if player is 'AI':
        return abdlmax_value(game_state, alpha, beta, depth)
    # If the agent is MIN return min-value
    return abdlmin_value(game_state, alpha, beta, depth)


def abdlmax_value(game_state, alpha, beta, depth):
    """
    Calculate the utility for a non-terminal state under Max's control
    using depth limited alpha beta pruning and the evaluation
    function game_state.eval()
    : param game_state: non-terminal GameState object
    : return: (integer) utility(evaluation function) of that state
    """
    # Enter your code here and remove the pass statement below
    a = alpha
    v = -sys.maxsize
    for move in game_state.possible_moves():
        v = max([v, abdl_value(game_state.successor(
            move, 'AI'), 'user', a, beta, depth - 1)])
        if v >= beta:
            return v
        a = max(a, v)
    return v


def abdlmin_value(game_state, alpha, beta, depth):
    """
    Calculate the utility for a non-terminal state under Min's control
    using depth limited alpha beta pruning and the evaluation
    function game_state.eval()
    : param game_state: non-terminal GameState object
    : return: (integer) utility(evaluation function) of that state
    """
    # Enter your code here and remove the pass statement below
    b = beta
    v = sys.maxsize
    for move in game_state.possible_moves():
        v = min([v, abdl_value(game_state.successor(
            move, 'user'), 'AI', alpha, b, depth - 1)])
        if v <= alpha:
            return v
        b = min([b, v])
    return v
