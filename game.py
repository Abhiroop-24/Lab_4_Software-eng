from board import initial_board, move_piece, SIZE
from rules import simple_move, capture_move, promote, has_pieces, has_legal_moves


class Checkers:
    def __init__(self):
        self.board = initial_board()
        self.player = "R"

    def print_board(self):
        print("\n   " + " ".join(str(c) for c in range(SIZE)))
        for r, row in enumerate(self.board):
            print(f"{r}  " + " ".join(row))

    def check_game_over(self):
        """Detects if active player has no pieces or no legal moves."""
        other_player = "B" if self.player == "R" else "R"
        if not has_pieces(self.board, self.player):
            return other_player, f"Player {self.player} has no pieces remaining."
        if not has_legal_moves(self.board, self.player):
            return other_player, f"Player {self.player} has no legal moves."
        return None, ""

    def run(self):
        print("Checkers — move: sr sc er ec")
        while True:
            winner, reason = self.check_game_over()
            if winner:
                self.print_board()
                print(f"Game over: {reason} Player {winner} wins!")
                return

            self.print_board()
            raw = input(f"{self.player}> ").strip().lower().split()
            if raw == ["q"]:
                return
            if len(raw) != 4:
                print("Enter four coordinates.")
                continue
            try:
                sr, sc, er, ec = map(int, raw)
            except ValueError:
                print("Coordinates must be numbers.")
                continue
            if not all(0 <= x < SIZE for x in (sr, sc, er, ec)):
                print("Outside board.")
                continue
            if self.board[sr][sc] not in (self.player, self.player + "K"):
                print("That is not your piece.")
                continue

            start, end = (sr, sc), (er, ec)
            if capture_move(self.board, self.player, start, end):
                move_piece(self.board, start, end)
            elif simple_move(self.board, self.player, start, end):
                move_piece(self.board, start, end)
            else:
                print("Invalid move.")
                continue

            promote(self.board)
            self.player = "B" if self.player == "R" else "R"
