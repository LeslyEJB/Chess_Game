from Heuristic import evaluate_board

def minimax(board, depth, maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, False)
            board.pop()
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, True)
            board.pop()
            min_eval = min(min_eval, eval)
        return min_eval

def minimax_decision(board, depth):
    best_score = float('-inf')
    best_move = None
    for move in board.legal_moves:
        board.push(move)
        score = minimax(board, depth - 1, False)
        board.pop()
        if score > best_score:
            best_score = score
            best_move = move
    return best_move
