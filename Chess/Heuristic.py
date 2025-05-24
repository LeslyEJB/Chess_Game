import chess

def evaluate_board(board):
    if board.is_checkmate():
        return 1000  # Pierde el rey negro
    if board.is_stalemate():
        return -100  # Tablas
    black_king_square = board.king(chess.BLACK)
    rank = chess.square_rank(black_king_square)
    file = chess.square_file(black_king_square)
    # Penaliza estar en el centro, premia ir a esquinas (donde será más fácil atraparlo)
    return -((3 - min(rank, 7 - rank)) + (3 - min(file, 7 - file)))
