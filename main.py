# iD Tech: Python Chess AI, 2022

# Import Modules & Libraries
import global_vars as G
import display_gui as gui
import ai_algorithms as ai
import pygame, chess, time, sys

# Game Settings
TEST_MODE = False
AI_DELAY = 1
B_DIFFICULTY = -1
W_DIFFICULTY = -1

# Board Setup
G.BOARD_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
G.BOARD.set_board_fen(G.BOARD_FEN)
gui.draw_board()
from_square = None
outcome = None

# Difficulty Control Function
def difficulty_options(move, difficulty):
    if difficulty == 0:
        move = chess.Move.null()
    elif difficulty == 1:
        print("Random Mode")
    elif difficulty == 2:
        print("Positional Mode")
    elif difficulty > 2:
        print("Predictive Mode")
        if difficulty >= 0:
            ai.make_ai_move(move, AI_DELAY)

    return move

# Pygame Display Loop
while not outcome:
    G.CLOCK.tick(60)
    move = None

# Player Control Flow
    if G.BOARD.turn == chess.BLACK:
        move = difficulty_options(move, B_DIFFICULTY)
    elif G.BOARD.turn == chess.WHITE:
        move = difficulty_options(move, W_DIFFICULTY)

        # Check Input Events
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Reset Highlight on Any Click
            tile_num = gui.tile_pos_to_num(event.pos)
            gui.draw_board()

            # First Click on New Turn -> Select Square
            if from_square == None:
                from_square = gui.make_selection(tile_num)
            # Selected Square Clicked Again -> Unselect Square
            elif from_square == tile_num:
                gui.draw_board()
                from_square = None
            # Potential Move Clicked -> ...
            elif from_square != None:
                # ...If Valid, Highlight & Move Selected Piece
                for move in G.BOARD.legal_moves:
                    if move.from_square == from_square and move.to_square == tile_num:
                        gui.draw_select_square(move.from_square)
                        gui.draw_select_square(move.to_square)
                        gui.print_san(move)
                        G.BOARD.push(move)
                        from_square = None
                # ...If Invalid, Only Select Square Instead
                if from_square != None:
                    from_square = gui.make_selection(tile_num)

        # Window Close -> End Program
        elif event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()

    # Draw All Pieces on Screen
    for piece_type in range(1, 7):
        w_piece_tiles = G.BOARD.pieces(piece_type, chess.WHITE)
        for tile_num in w_piece_tiles:
            gui.draw_piece(tile_num, piece_type, chess.WHITE)

        b_piece_tiles = G.BOARD.pieces(piece_type, chess.BLACK)
        for tile_num in b_piece_tiles:
            gui.draw_piece(tile_num, piece_type, chess.BLACK)

    # Check End Game Conditions
    outcome = G.BOARD.outcome()
    if not TEST_MODE and outcome:
        gui.determine_outcome(outcome)

    # Update the Display Screen
    pygame.display.update()

# Wait till Exit after Game Over
while True:
    G.CLOCK.tick(60)
    for event in pygame.event.get():
        # Window Close -> End Program
        if event.type == pygame.QUIT:
            outcome = True
            pygame.display.quit()
            pygame.quit()
            sys.exit()
