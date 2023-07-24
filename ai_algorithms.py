# Import Modules & Libraries

import global_vars as G
import display_gui as gui
import chess, random, time
# Select Random Move

# Get Game Status

# Get Board Score

# Select Positional Move

# Negamax with Alpha-Beta Pruning

# Quiescence Search

# Select Predictive Move

# Complete AI Move
def make_ai_move(move, delay):
    time.sleep(delay)
    if move != chess.Move.null():
        gui.draw_board()
        gui.draw_select_square(move.from_square)
        gui.draw_select_square(move.to_square)
    gui.print_san(move)
    G.BOARD.push(move)