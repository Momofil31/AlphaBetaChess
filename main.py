import chess
import time
from typing import *

CUTOFF_DEPTH = 3

piece_value = {
    chess.PAWN: 100,
    chess.ROOK: 500,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.QUEEN: 900,
    chess.KING: 20000
}

pawnEvalWhite = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0
]
pawnEvalBlack = list(reversed(pawnEvalWhite))

knightEval = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]

bishopEvalWhite = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]
bishopEvalBlack = list(reversed(bishopEvalWhite))

rookEvalWhite = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0
]
rookEvalBlack = list(reversed(rookEvalWhite))

queenEval = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -5, 0, 5, 5, 5, 5, 0, -5,
    0, 0, 5, 5, 5, 5, 0, -5,
    -10, 5, 5, 5, 5, 5, 0, -10,
    -10, 0, 5, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
]

kingEvalWhite = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30
]
kingEvalBlack = list(reversed(kingEvalWhite))


def evaluate_piece(piece: chess.Piece, square: chess.Square) -> int:
    piece_type = piece.piece_type
    mapping = []
    if piece_type == chess.PAWN:
        mapping = pawnEvalWhite if piece.color == chess.WHITE else pawnEvalBlack
    if piece_type == chess.KNIGHT:
        mapping = knightEval
    if piece_type == chess.BISHOP:
        mapping = bishopEvalWhite if piece.color == chess.WHITE else bishopEvalBlack
    if piece_type == chess.ROOK:
        mapping = rookEvalWhite if piece.color == chess.WHITE else rookEvalBlack
    if piece_type == chess.QUEEN:
        mapping = queenEval
    if piece_type == chess.KING:
        # use end game piece-square tables if neither side has a queen
        mapping = kingEvalWhite if piece.color == chess.WHITE else kingEvalBlack

    return mapping[square]


def calc_board_value(board: chess.Board) -> float:
    total = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if not piece:
            continue

        value = piece_value[piece.piece_type] + evaluate_piece(piece, square)
        total += value if piece.color == chess.WHITE else -value

    return total


def evaluate_position(board: chess.Board, player: chess.Color):
    if board.is_checkmate():
        if player == chess.WHITE:
            return -float("inf")
        else:
            return float("inf")
    if board.is_stalemate():
        return 0.0
    else:
        return calc_board_value(board)


def alpha_beta_search(board: chess.Board) -> chess.Move:
    depth = CUTOFF_DEPTH
    if board.turn == chess.WHITE:
        value, move = max_value(board, depth - 1, alpha=-float("inf"), beta=float("inf"))
    else:
        value, move = min_value(board, depth - 1, alpha=-float("inf"), beta=float("inf"))
    # print(value)
    return move


def max_value(board: chess.Board, depth: int, alpha: float, beta: float) -> tuple[float, Optional[chess.Move]]:
    if depth == 0:
        value = evaluate_position(board, board.turn)
        return value, None
    v = -float("inf")
    move = None
    for action in board.legal_moves:
        # if depth == 1:
        #    print(f"Trying with action: {action}")
        board.push(action)
        v2, _ = min_value(board, depth - 1, alpha, beta)
        board.pop()
        if v2 > v:
            v, move = v2, action
            alpha = max(alpha, v)
        if alpha >= beta:
            return v, move
    return v, move


def min_value(board: chess.Board, depth: int, alpha: float, beta: float) -> tuple[float, Optional[chess.Move]]:
    if depth == 0:
        value = evaluate_position(board, board.turn)
        return value, None
    v = float("inf")
    move = None
    for action in board.legal_moves:
        # if depth == 1:
        #   print(f"Trying with action: {action}")
        board.push(action)
        # print("temp_board min")
        # print(temp_board)
        v2, _ = max_value(board, depth - 1, alpha, beta)
        board.pop()
        if v2 < v:
            v, move = v2, action
            beta = min(beta, v)
        if beta <= alpha:
            return v, move
    return v, move


if __name__ == '__main__':
    chessBoard = chess.Board()

    provideFen = input("Would you like to provide a FEN string? (y/n)\n")
    provideFen.lower()
    if provideFen == "y" or provideFen == "yes":
        fen = input("Provide FEN string\n")
        try:
            chessBoard.set_board_fen(fen)
        except ValueError:
            print("FEN string is invalid")
    # chessBoard.set_fen("4rk2/1bp3p1/5p2/p7/2B1rN2/1P4P1/P4P1P/3R2K1 w - - 1 1")
    print(f"Initial state:\n{chessBoard}\n")
    for i in range(0, 30):
        print("White moves") if chessBoard.turn == chess.WHITE else print("Black moves")

        if chessBoard.is_checkmate():
            print(f"Checkmate!\n{chessBoard.fen()}")
            break
        if chessBoard.is_stalemate():
            print("Stalemate!")
            break

        start = time.time()
        nextMove = alpha_beta_search(chessBoard)
        end = time.time()
        # print(move)
        chessBoard.push(nextMove)
        print(f"{i + 1}: Search performed in {(end - start):.3f} seconds, move {nextMove}:\n{chessBoard}\n")
