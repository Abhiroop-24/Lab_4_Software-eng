# Scenario 21 — Checkers

A modular terminal checkers game with a board, movement rules, captures, and promotion support.

## Overview & Lab 4 Deliverables

This repository contains the completed, fully tested, and verified implementation for **Lab 4: Vibe Coding (Scenario 21: Checkers)**.

All lab tasks (Tasks 1–4) have been completed, verified against edge cases, and covered by a comprehensive unit test suite.

### Key Deliverables in `Lab-4/`
- **Updated Source Code**: `board.py`, `game.py`, `rules.py`, `main.py`, `test_checkers.py`
- **Gameplay Demonstration Videos**:
  - Before changes (showing capture defect): [`Lab-4/videos/before_gameplay.mp4`](Lab-4/videos/before_gameplay.mp4)
  - After changes (showing all features & bug fixes): [`Lab-4/videos/after_gameplay.mp4`](Lab-4/videos/after_gameplay.mp4)
- **Terminal Execution Screenshots**:
  - Initial defect: [`Lab-4/screenshots/before_gameplay.png`](Lab-4/screenshots/before_gameplay.png)
  - Verified gameplay: [`Lab-4/screenshots/after_gameplay.png`](Lab-4/screenshots/after_gameplay.png)
  - Test suite passing (9/9 tests): [`Lab-4/screenshots/test_results.png`](Lab-4/screenshots/test_results.png)
- **Vibe Coding LLM Chat History**:
  - PDF Export: [`Lab-4/chat_history/Lab4_VibeCoding_Chat_History.pdf`](Lab-4/chat_history/Lab4_VibeCoding_Chat_History.pdf)
  - Word Document (DOCX): [`Lab-4/chat_history/Lab4_VibeCoding_Chat_History.docx`](Lab-4/chat_history/Lab4_VibeCoding_Chat_History.docx)
  - Markdown Document: [`Lab-4/chat_history/Lab4_VibeCoding_Chat_History.md`](Lab-4/chat_history/Lab4_VibeCoding_Chat_History.md)

---

## Provided Files

- `main.py` — game entry point.
- `game.py` — turn flow, move processor, interaction, and feedback.
- `board.py` — board representation and piece movement with capture removal.
- `rules.py` — legal moves, captures, forced captures, multi-captures, king movements, win checks, and promotions.
- `test_checkers.py` — unit and integration test suite.
- `requirements.txt` — standard library only (no third-party runtime dependencies).

---

## Setup & Running the Game

```bash
# Run the interactive game
python main.py
```

### Running the Test Suite

```bash
# Run all unit and integration tests
python test_checkers.py -v
```

---

## Completed Tasks Summary

### Task 1 — Capture Correctness
- **Issue in Starter Code**: In `board.py`, `move_piece()` moved the capturing piece but never removed the jumped opponent piece from the intermediate board square.
- **Resolution**: Updated `move_piece()` to calculate intermediate coordinates `((sr + er) // 2, (sc + ec) // 2)` during a 2-square jump, remove the opponent piece by clearing it to `"."`, and return the captured piece for feedback.

### Task 2 — Win and No-Move Detection
- **Resolution**: Implemented `has_pieces()` and `has_legal_moves()` in `rules.py`. Integrated `check_game_over()` into `game.py`. Before each turn, if the active player has no pieces remaining or no legal moves available, the game terminates cleanly and announces the winner.

### Task 3 — Complete Checkers Rules
- **Forced Captures**: Implemented `get_all_captures()` and mandatory capture enforcement. If any capture is available on the board for the active player, simple moves and non-capturing moves are rejected with clear feedback.
- **Multi-Capture Turns**: Implemented `get_captures_for_piece()`. When a piece captures an opponent piece and has additional legal captures from the landing square, `active_jump_pos` locks to that piece, requiring the player to complete the jump chain.
- **King Movement in Both Directions**: Kings (`RK` and `BK`) can move and capture diagonally in all 4 directions (both forward and backward).
- **Promotion**: Pieces reaching the opponent's back row (row 0 for Red, row 7 for Black) are automatically promoted to Kings (`RK` and `BK`). Under standard rules, promotion on the back row concludes the jump turn.

### Task 4 — Move-Level Feedback
- Added concise action feedback for every player action:
  - Simple move: `R moved from (5, 0) to (4, 1).`
  - Normal capture: `R captured B at (3, 2) and jumped to (2, 3).`
  - Multi-capture intermediate jump: `R captured B at (3, 2) and jumped to (2, 3). Multi-capture available from (2, 3)!`
  - Promotion: `R moved from (1, 2) to (0, 1) and was promoted to King!`
  - Capture with promotion: `R captured B at (1, 2), jumped to (0, 1), and was promoted to King!`

---

## Submission Checklist

- [x] Task 1 completed and the original defect was reproduced and fixed.
- [x] Tasks 2–4 completed and tested.
- [x] Boundary and invalid-input cases tested.
- [x] No unnecessary external dependencies added.
- [x] No persistent storage added.
- [x] Code remains understandable and modular.
- [x] Complete LLM chat-history link included.

## Deliverables Checklist

- [x] A 10-second video of gameplay **before** changes, showing the bug/broken behavior (`Lab-4/videos/before_gameplay.mp4`)
- [x] A 10-second video of gameplay **after** changes, showing the bug fixed and new features working (`Lab-4/videos/after_gameplay.mp4`)
- [x] The complete LLM Chat history exported as PDF, DOCX, and Markdown (`Lab-4/chat_history/`)
