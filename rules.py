SIZE = 8


def is_player_piece(piece, player):
    if player == "R":
        return piece in ("R", "RK")
    elif player == "B":
        return piece in ("B", "BK")
    return False


def is_opponent_piece(piece, player):
    if player == "R":
        return piece in ("B", "BK")
    elif player == "B":
        return piece in ("R", "RK")
    return False


def is_king(piece):
    return piece in ("RK", "BK")


def simple_move(board, player, start, end):
    sr, sc = start
    er, ec = end
    if not (0 <= sr < SIZE and 0 <= sc < SIZE and 0 <= er < SIZE and 0 <= ec < SIZE):
        return False
    piece = board[sr][sc]
    if not is_player_piece(piece, player):
        return False
    if board[er][ec] != ".":
        return False

    dr = er - sr
    dc = ec - sc
    if abs(dr) != 1 or abs(dc) != 1:
        return False

    if is_king(piece):
        return True

    expected_dr = -1 if player == "R" else 1
    return dr == expected_dr


def capture_move(board, player, start, end):
    sr, sc = start
    er, ec = end
    if not (0 <= sr < SIZE and 0 <= sc < SIZE and 0 <= er < SIZE and 0 <= ec < SIZE):
        return False
    piece = board[sr][sc]
    if not is_player_piece(piece, player):
        return False
    if board[er][ec] != ".":
        return False

    dr = er - sr
    dc = ec - sc
    if abs(dr) != 2 or abs(dc) != 2:
        return False

    mr = (sr + er) // 2
    mc = (sc + ec) // 2
    middle_piece = board[mr][mc]
    if not is_opponent_piece(middle_piece, player):
        return False

    if is_king(piece):
        return True

    expected_dr = -2 if player == "R" else 2
    return dr == expected_dr


def get_captures_for_piece(board, player, start):
    """Returns list of valid end positions that the piece at start can capture."""
    captures = []
    sr, sc = start
    if not (0 <= sr < SIZE and 0 <= sc < SIZE):
        return captures
    piece = board[sr][sc]
    if not is_player_piece(piece, player):
        return captures

    for dr in (-2, 2):
        for dc in (-2, 2):
            end = (sr + dr, sc + dc)
            if 0 <= end[0] < SIZE and 0 <= end[1] < SIZE:
                if capture_move(board, player, start, end):
                    captures.append(end)
    return captures


def get_all_captures(board, player):
    """Returns list of all ((sr, sc), (er, ec)) capture moves available for player."""
    all_captures = []
    for r in range(SIZE):
        for c in range(SIZE):
            if is_player_piece(board[r][c], player):
                start = (r, c)
                for end in get_captures_for_piece(board, player, start):
                    all_captures.append((start, end))
    return all_captures


def get_all_simple_moves(board, player):
    """Returns list of all ((sr, sc), (er, ec)) simple moves available for player."""
    all_moves = []
    for r in range(SIZE):
        for c in range(SIZE):
            if is_player_piece(board[r][c], player):
                start = (r, c)
                for dr in (-1, 1):
                    for dc in (-1, 1):
                        end = (r + dr, c + dc)
                        if 0 <= end[0] < SIZE and 0 <= end[1] < SIZE:
                            if simple_move(board, player, start, end):
                                all_moves.append((start, end))
    return all_moves


def has_pieces(board, player):
    """Returns True if player has at least one piece on the board."""
    for r in range(SIZE):
        for c in range(SIZE):
            if is_player_piece(board[r][c], player):
                return True
    return False


def has_legal_moves(board, player):
    """Returns True if player has at least one legal capture or simple move."""
    if get_all_captures(board, player):
        return True
    if get_all_simple_moves(board, player):
        return True
    return False


def check_and_promote(board, pos):
    """Promotes a piece at pos if it reached the back row. Returns True if promoted."""
    r, c = pos
    if not (0 <= r < SIZE and 0 <= c < SIZE):
        return False
    if board[r][c] == "R" and r == 0:
        board[r][c] = "RK"
        return True
    if board[r][c] == "B" and r == SIZE - 1:
        board[r][c] = "BK"
        return True
    return False


def promote(board):
    """Scans the board and promotes pieces on back rows."""
    promoted = False
    for c in range(SIZE):
        if board[0][c] == "R":
            board[0][c] = "RK"
            promoted = True
        if board[SIZE - 1][c] == "B":
            board[SIZE - 1][c] = "BK"
            promoted = True
    return promoted
