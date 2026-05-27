from copy import deepcopy
from consts import *

def minimax(board, depth, alpha, beta, maximizing_player):
    # Warunek stopu: koniec głębokości lub brak ruchów (koniec gry)
    if depth == 0:
        return board.evaluate(), board

    valid_moves = board.get_valid_moves(WHITE if maximizing_player else BLACK)
    if not valid_moves:
        return board.evaluate(), board

    best_move_board = None
    if maximizing_player:
        max_eval = -float('inf')
        for move in valid_moves:
            temp_board = simulate_move(board, move)
            evaluation = minimax(temp_board, depth - 1, alpha, beta, False)[0]
            if evaluation > max_eval:
                max_eval = evaluation
                best_move_board = temp_board
            alpha = max(alpha, evaluation)
            if beta <= alpha: break
        return max_eval, best_move_board
    else:
        min_eval = float('inf')
        for move in valid_moves:
            temp_board = simulate_move(board, move)
            evaluation = minimax(temp_board, depth - 1, alpha, beta, True)[0]
            if evaluation < min_eval:
                min_eval = evaluation
                best_move_board = temp_board
            beta = min(beta, evaluation)
            if beta <= alpha: break
        return min_eval, best_move_board

def simulate_move(board, move):
    new_board = deepcopy(board)
    # Wykonujemy ruch (przesunięcie pionka z origin do dest)
    new_board.move(move['origin'], move['dest'])
    
    # Usuwamy wszystkie zbite pionki z listy 'captured'
    for r, c in move['captured']:
        new_board.board[r][c] = EMPTY
        
    return new_board