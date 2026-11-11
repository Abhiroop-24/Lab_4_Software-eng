"""
Comprehensive unit and integration test suite for Checkers.
Covers all required areas:
- Ordinary moves
- Captures & piece removal
- Multiple captures
- Forced captures
- Promotion
- King movement (forward and backward)
- Win and no-move detection
- Invalid coordinates & validation
- Quitting
"""

import unittest
from io import StringIO
import os
import sys

# Ensure repository root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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
from game import Checkers


class TestCheckersRules(unittest.TestCase):
    def setUp(self):
        self.empty_board = [["."] * SIZE for _ in range(SIZE)]

    def test_ordinary_moves(self):
        board = initial_board()
        # Red ordinary forward move
        self.assertTrue(simple_move(board, "R", (5, 0), (4, 1)))
        self.assertTrue(simple_move(board, "R", (5, 2), (4, 3)))
        # Red backward move is invalid
        self.assertFalse(simple_move(board, "R", (5, 0), (6, 1)))

        # Black ordinary forward move
        self.assertTrue(simple_move(board, "B", (2, 1), (3, 0)))
        self.assertTrue(simple_move(board, "B", (2, 1), (3, 2)))
        # Black backward move is invalid
        self.assertFalse(simple_move(board, "B", (2, 1), (1, 0)))

        # Blocked destination
        board[4][1] = "B"
        self.assertFalse(simple_move(board, "R", (5, 0), (4, 1)))

    def test_captures_and_piece_removal(self):
        board = self.empty_board
        board[5][2] = "R"
        board[4][3] = "B"
        board[3][4] = "."

        # Capture validity
        self.assertTrue(capture_move(board, "R", (5, 2), (3, 4)))
        
        # Execute capture
        captured = move_piece(board, (5, 2), (3, 4))
        self.assertEqual(captured, "B")
        self.assertEqual(board[5][2], ".")
        self.assertEqual(board[3][4], "R")
        # Ensure jumped piece was removed (Task 1 defect fix)
        self.assertEqual(board[4][3], ".")

        # Cannot capture own piece
        board[4][3] = "R"
        self.assertFalse(capture_move(board, "R", (5, 2), (3, 4)))

    def test_forced_captures(self):
        game = Checkers()
        # Initial board has no captures available
        self.assertEqual(len(get_all_captures(game.board, "R")), 0)

        # Setup capture position
        game.board[4][3] = "B"
        # R at (5, 2) can capture (3, 4) and R at (5, 4) can capture (3, 2)
        captures = get_all_captures(game.board, "R")
        self.assertGreater(len(captures), 0)

        # Simple move must be rejected when capture is available
        success, msg, _ = game.process_move((5, 0), (4, 1))
        self.assertFalse(success)
        self.assertIn("mandatory", msg)

        # Valid capture must be accepted
        success, msg, _ = game.process_move((5, 2), (3, 4))
        self.assertTrue(success)
        self.assertIn("captured", msg)

    def test_multiple_captures(self):
        game = Checkers()
        game.board = [["."] * SIZE for _ in range(SIZE)]
        # Setup R at (6, 1), B at (5, 2) and B at (3, 4)
        game.board[6][1] = "R"
        game.board[5][2] = "B"
        game.board[3][4] = "B"

        # First jump: from (6, 1) over (5, 2) to (4, 3)
        success, msg, turn_ended = game.process_move((6, 1), (4, 3))
        self.assertTrue(success)
        self.assertFalse(turn_ended)
        self.assertEqual(game.player, "R")
        self.assertEqual(game.active_jump_pos, (4, 3))
        self.assertIn("Multi-capture available", msg)
        self.assertEqual(game.board[5][2], ".")

        # Trying to move a different piece or wrong start fails
        game.board[7][0] = "R"
        success, msg, _ = game.process_move((7, 0), (6, 1))
        self.assertFalse(success)
        self.assertIn("Multi-capture in progress", msg)

        # Second jump: from (4, 3) over (3, 4) to (2, 5)
        success, msg, turn_ended = game.process_move((4, 3), (2, 5))
        self.assertTrue(success)
        self.assertTrue(turn_ended)
        self.assertEqual(game.player, "B")
        self.assertIsNone(game.active_jump_pos)
        self.assertEqual(game.board[3][4], ".")
        self.assertEqual(game.board[2][5], "R")

    def test_promotion(self):
        board = self.empty_board
        board[1][2] = "R"
        board[6][3] = "B"

        # Moving to row 0 promotes Red
        success = simple_move(board, "R", (1, 2), (0, 1))
        self.assertTrue(success)
        move_piece(board, (1, 2), (0, 1))
        promoted = check_and_promote(board, (0, 1))
        self.assertTrue(promoted)
        self.assertEqual(board[0][1], "RK")

        # Moving to row 7 promotes Black
        success = simple_move(board, "B", (6, 3), (7, 4))
        self.assertTrue(success)
        move_piece(board, (6, 3), (7, 4))
        promoted = check_and_promote(board, (7, 4))
        self.assertTrue(promoted)
        self.assertEqual(board[7][4], "BK")

    def test_king_movement_and_captures(self):
        board = self.empty_board
        board[4][3] = "RK"

        # King moving backward (increasing row)
        self.assertTrue(simple_move(board, "R", (4, 3), (5, 2)))
        self.assertTrue(simple_move(board, "R", (4, 3), (5, 4)))
        # King moving forward (decreasing row)
        self.assertTrue(simple_move(board, "R", (4, 3), (3, 2)))
        self.assertTrue(simple_move(board, "R", (4, 3), (3, 4)))

        # King backward capture
        board[5][4] = "B"
        self.assertTrue(capture_move(board, "R", (4, 3), (6, 5)))
        captured = move_piece(board, (4, 3), (6, 5))
        self.assertEqual(captured, "B")
        self.assertEqual(board[5][4], ".")
        self.assertEqual(board[6][5], "RK")

    def test_no_move_positions_and_win_detection(self):
        game = Checkers()
        game.board = [["."] * SIZE for _ in range(SIZE)]
        # R has no pieces
        game.board[0][1] = "B"
        winner, reason = game.check_game_over()
        self.assertEqual(winner, "B")
        self.assertIn("no pieces remaining", reason)

        # R has a trapped piece (no legal moves)
        game.board = [["."] * SIZE for _ in range(SIZE)]
        game.board[0][1] = "R"  # R piece on row 0 cannot move forward
        game.board[7][0] = "B"
        winner, reason = game.check_game_over()
        self.assertEqual(winner, "B")
        self.assertIn("no legal moves", reason)

    def test_invalid_coordinates_and_inputs(self):
        game = Checkers()
        # Coordinates out of board
        success, msg, _ = game.process_move((-1, 0), (4, 1))
        self.assertFalse(success)
        self.assertIn("Outside board", msg)

        success, msg, _ = game.process_move((5, 0), (8, 1))
        self.assertFalse(success)
        self.assertIn("Outside board", msg)

        # Moving opponent piece
        success, msg, _ = game.process_move((0, 1), (1, 2))
        self.assertFalse(success)
        self.assertIn("not your piece", msg)

        # Moving empty square
        success, msg, _ = game.process_move((4, 0), (3, 1))
        self.assertFalse(success)
        self.assertIn("not your piece", msg)

        # Illegal non-diagonal step
        success, msg, _ = game.process_move((5, 0), (4, 0))
        self.assertFalse(success)
        self.assertIn("Invalid move", msg)

    def test_quitting_and_run_termination(self):
        game = Checkers()
        # Mock input 'q'
        old_stdin = sys.stdin
        old_stdout = sys.stdout
        try:
            sys.stdin = StringIO("q\n")
            sys.stdout = StringIO()
            game.run()
            output = sys.stdout.getvalue()
            self.assertIn("Game ended by player.", output)
        finally:
            sys.stdin = old_stdin
            sys.stdout = old_stdout


if __name__ == "__main__":
    unittest.main()
