SIZE = 8


def initial_board():
    board = [["."] * SIZE for _ in range(SIZE)]
    for r in range(3):
        for c in range(SIZE):
            if (r + c) % 2 == 1:
                board[r][c] = "B"
    for r in range(5, 8):
        for c in range(SIZE):
            if (r + c) % 2 == 1:
                board[r][c] = "R"
    return board


def move_piece(board, start, end):
    """
    Moves piece from start to end coordinates.
    If the move is a capture (distance of 2), removes the jumped opponent piece.
    Returns the captured piece (e.g. 'B', 'BK', 'R', 'RK') or None if simple move.
    """
    piece = board[start[0]][start[1]]
    board[end[0]][end[1]] = piece
    board[start[0]][start[1]] = "."

    captured = None
    if abs(end[0] - start[0]) == 2 and abs(end[1] - start[1]) == 2:
        mr = (start[0] + end[0]) // 2
        mc = (start[1] + end[1]) // 2
        captured = board[mr][mc]
        board[mr][mc] = "."

    return captured
