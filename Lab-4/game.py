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

    def other_player(self):
        return "B" if self.player == "R" else "R"

    def print_board(self):
        print("\n   " + " ".join(f"{c:>2}" for c in range(SIZE)))
        for r, row in enumerate(self.board):
            print(f"{r}  " + " ".join(f"{p:>2}" for p in row))

    def check_game_over(self):
        """Detects if active player has no pieces or no legal moves."""
        if not has_pieces(self.board, self.player):
            return self.other_player(), f"Player {self.player} has no pieces remaining."
        if not has_legal_moves(self.board, self.player):
            return self.other_player(), f"Player {self.player} has no legal moves."
        return None, ""

    def process_move(self, start, end):
        """
        Processes a move from start to end for the active player.
        Returns a tuple: (success: bool, message: str, turn_ended: bool)
        """
        sr, sc = start
        er, ec = end

        if not (0 <= sr < SIZE and 0 <= sc < SIZE and 0 <= er < SIZE and 0 <= ec < SIZE):
            return False, "Outside board.", False

        # If inside multi-capture
        if self.active_jump_pos is not None:
            if start != self.active_jump_pos:
                return False, f"Multi-capture in progress: you must continue jumping with the piece at {self.active_jump_pos}.", False

            valid_captures = get_captures_for_piece(self.board, self.player, self.active_jump_pos)
            if end not in valid_captures:
                return False, "Invalid capture jump.", False

            was_king = self.board[sr][sc] == self.player + "K"
            captured = move_piece(self.board, start, end)
            mr, mc = (sr + er) // 2, (sc + ec) // 2
            promoted = check_and_promote(self.board, end)

            if promoted and not was_king:
                self.active_jump_pos = None
                curr_player = self.player
                self.player = self.other_player()
                msg = f"{curr_player} captured {captured} at ({mr}, {mc}), jumped to ({er}, {ec}), and was promoted to King!"
                return True, msg, True

            next_captures = get_captures_for_piece(self.board, self.player, end)
            if next_captures:
                self.active_jump_pos = end
                msg = f"{self.player} captured {captured} at ({mr}, {mc}) and jumped to ({er}, {ec}). Multi-capture available from ({er}, {ec})!"
                return True, msg, False
            else:
                self.active_jump_pos = None
                curr_player = self.player
                self.player = self.other_player()
                msg = f"{curr_player} captured {captured} at ({mr}, {mc}) and jumped to ({er}, {ec}). Capture sequence complete."
                return True, msg, True

        # Regular turn
        if self.board[sr][sc] not in (self.player, self.player + "K"):
            return False, "That is not your piece.", False

        all_captures = get_all_captures(self.board, self.player)
        if all_captures:
            if (start, end) not in all_captures:
                return False, "A capture is mandatory when available.", False

            was_king = self.board[sr][sc] == self.player + "K"
            captured = move_piece(self.board, start, end)
            mr, mc = (sr + er) // 2, (sc + ec) // 2
            promoted = check_and_promote(self.board, end)

            if promoted and not was_king:
                curr_player = self.player
                self.player = self.other_player()
                msg = f"{curr_player} captured {captured} at ({mr}, {mc}), jumped to ({er}, {ec}), and was promoted to King!"
                return True, msg, True

            next_captures = get_captures_for_piece(self.board, self.player, end)
            if next_captures:
                self.active_jump_pos = end
                msg = f"{self.player} captured {captured} at ({mr}, {mc}) and jumped to ({er}, {ec}). Multi-capture available from ({er}, {ec})!"
                return True, msg, False
            else:
                curr_player = self.player
                self.player = self.other_player()
                msg = f"{curr_player} captured {captured} at ({mr}, {mc}) and jumped to ({er}, {ec})."
                return True, msg, True

        # Simple move
        if simple_move(self.board, self.player, start, end):
            move_piece(self.board, start, end)
            promoted = check_and_promote(self.board, end)
            curr_player = self.player
            self.player = self.other_player()
            if promoted:
                msg = f"{curr_player} moved from ({sr}, {sc}) to ({er}, {ec}) and was promoted to King!"
            else:
                msg = f"{curr_player} moved from ({sr}, {sc}) to ({er}, {ec})."
            return True, msg, True
        else:
            return False, "Invalid move.", False

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
                print("Game ended by player.")
                return
            if len(raw) != 4:
                print("Enter four coordinates.")
                continue
            try:
                sr, sc, er, ec = map(int, raw)
            except ValueError:
                print("Coordinates must be numbers.")
                continue

            success, message, _ = self.process_move((sr, sc), (er, ec))
            print(message)
