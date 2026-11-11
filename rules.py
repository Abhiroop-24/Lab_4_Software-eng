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


def simple_move(board, player, start, end):
    sr, sc = start
    er, ec = end
    if not (0 <= sr < SIZE and 0 <= sc < SIZE and 0 <= er < SIZE and 0 <= ec < SIZE):
        return False
    if not is_player_piece(board[sr][sc], player):
        return False
    if board[er][ec] != ".":
        return False

    direction = -1 if player == "R" else 1
    return (
        abs(er - sr) == 1 and abs(ec - sc) == 1 and
        er - sr == direction
    )


def capture_move(board, player, start, end):
    sr, sc = start
    er, ec = end
    if not (0 <= sr < SIZE and 0 <= sc < SIZE and 0 <= er < SIZE and 0 <= ec < SIZE):
        return False
    if not is_player_piece(board[sr][sc], player):
        return False
    if board[er][ec] != ".":
        return False

    direction = -1 if player == "R" else 1
    mr, mc = (sr + er) // 2, (sc + ec) // 2
    return (
        abs(er - sr) == 2 and abs(ec - sc) == 2 and
        er - sr == 2 * direction and
        is_opponent_piece(board[mr][mc], player)
    )


def has_pieces(board, player):
    """Returns True if player has at least one piece on the board."""
    for r in range(SIZE):
        for c in range(SIZE):
            if is_player_piece(board[r][c], player):
                return True
    return False


def has_legal_moves(board, player):
    """Returns True if player has at least one legal simple or capture move."""
    for r in range(SIZE):
        for c in range(SIZE):
            if is_player_piece(board[r][c], player):
                start = (r, c)
                # Check simple moves
                for dr in (-1, 1):
                    for dc in (-1, 1):
                        end = (r + dr, c + dc)
                        if 0 <= end[0] < SIZE and 0 <= end[1] < SIZE:
                            if simple_move(board, player, start, end):
                                return True
                # Check capture moves
                for dr in (-2, 2):
                    for dc in (-2, 2):
                        end = (r + dr, c + dc)
                        if 0 <= end[0] < SIZE and 0 <= end[1] < SIZE:
                            if capture_move(board, player, start, end):
                                return True
    return False


def promote(board):
    for c in range(SIZE):
        if board[0][c] == "R":
            board[0][c] = "RK"
        if board[SIZE - 1][c] == "B":
            board[SIZE - 1][c] = "BK"
