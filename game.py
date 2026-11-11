from board import initial_board, move_piece, SIZE
from rules import (
    simple_move,
    capture_move,
    promote,
    check_and_promote,
    has_pieces,
    has_legal_moves,
    get_all_captures,
    get_captures_for_piece,
)


class Checkers:
    def __init__(self):
        self.board = initial_board()
        self.player = "R"
        self.active_jump_pos = None

    def print_board(self):
        print("\n   " + " ".join(str(c) for c in range(SIZE)))
        for r, row in enumerate(self.board):
            print(f"{r}  " + " ".join(row))

    def check_game_over(self):
        other_player = "B" if self.player == "R" else "R"
        if not has_pieces(self.board, self.player):
            return other_player, f"Player {self.player} has no pieces remaining."
        if not has_legal_moves(self.board, self.player):
            return other_player, f"Player {self.player} has no legal moves."
        return None, ""

    def run(self):
        print("Checkers — move: sr sc er ec")
        while True:
            if self.active_jump_pos is None:
                winner, reason = self.check_game_over()
                if winner:
                    self.print_board()
                    print(f"Game over: {reason} Player {winner} wins!")
                    return

            self.print_board()
            prompt = (
                f"{self.player} (continue jump from {self.active_jump_pos[0]} {self.active_jump_pos[1]})> "
                if self.active_jump_pos
                else f"{self.player}> "
            )
            raw = input(prompt).strip().lower().split()
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

            start, end = (sr, sc), (er, ec)

            # If inside multi-capture
            if self.active_jump_pos is not None:
                if start != self.active_jump_pos:
                    print(f"Multi-capture in progress: you must continue jumping with the piece at {self.active_jump_pos}.")
                    continue
                valid_captures = get_captures_for_piece(self.board, self.player, self.active_jump_pos)
                if end not in valid_captures:
                    print("Invalid capture jump.")
                    continue

                was_king_before = self.board[sr][sc] == self.player + "K"
                move_piece(self.board, start, end)
                promoted = check_and_promote(self.board, end)

                if promoted and not was_king_before:
                    self.active_jump_pos = None
                    self.player = "B" if self.player == "R" else "R"
                    continue

                next_captures = get_captures_for_piece(self.board, self.player, end)
                if next_captures:
                    self.active_jump_pos = end
                else:
                    self.active_jump_pos = None
                    self.player = "B" if self.player == "R" else "R"
                continue

            # Standard turn
            if self.board[sr][sc] not in (self.player, self.player + "K"):
                print("That is not your piece.")
                continue

            all_captures = get_all_captures(self.board, self.player)
            if all_captures:
                if (start, end) not in all_captures:
                    print("A capture is mandatory when available.")
                    continue
                was_king_before = self.board[sr][sc] == self.player + "K"
                move_piece(self.board, start, end)
                promoted = check_and_promote(self.board, end)

                if promoted and not was_king_before:
                    self.player = "B" if self.player == "R" else "R"
                    continue

                next_captures = get_captures_for_piece(self.board, self.player, end)
                if next_captures:
                    self.active_jump_pos = end
                else:
                    self.player = "B" if self.player == "R" else "R"
                continue

            # No captures available: simple move
            if simple_move(self.board, self.player, start, end):
                move_piece(self.board, start, end)
                check_and_promote(self.board, end)
                self.player = "B" if self.player == "R" else "R"
            else:
                print("Invalid move.")
                continue
