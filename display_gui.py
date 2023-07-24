# Import Modules & Libraries
from os import system, name
import pygame, chess, math
import global_vars as G

# Clear Output & Print Game Start
def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
clear()
print(' iD Tech: PGN,  Portable Game Notation')
print('---------------------------------------')

# Pygame Initializations
pygame.init()
pygame.font.init()
pygame.display.init()
pygame.display.set_caption(G.ID_TECH_TITLE)
pygame.display.set_icon(G.ID_TECH_LOGO)

# Load Chess Game Pieces
w_king_img = pygame.image.load('images/w_king.png')
w_queen_img = pygame.image.load('images/w_queen.png')
w_bishop_img = pygame.image.load('images/w_bishop.png')
w_knight_img = pygame.image.load('images/w_knight.png')
w_rook_img = pygame.image.load('images/w_rook.png')
w_pawn_img = pygame.image.load('images/w_pawn.png')
b_king_img = pygame.image.load('images/b_king.png')
b_queen_img = pygame.image.load('images/b_queen.png')
b_bishop_img = pygame.image.load('images/b_bishop.png')
b_knight_img = pygame.image.load('images/b_knight.png')
b_rook_img = pygame.image.load('images/b_rook.png')
b_pawn_img = pygame.image.load('images/b_pawn.png')

# Set System Font Information
font_size = math.floor(G.LABEL_SIZE * 0.8)
label_font = pygame.font.SysFont('freemono', font_size, True)
result_size = math.floor(G.TILE_SIZE * 0.5)
result_font = pygame.font.SysFont('freemono', result_size, True)

# Convert Tile Position to Number
def tile_pos_to_num(tile_position):
    (tile_x, tile_y) = tile_position
    file = math.floor((tile_x - G.LABEL_SIZE) / G.TILE_SIZE + 1)
    rank = math.ceil((G.BOARD_SIZE - tile_y) / G.TILE_SIZE)

    tile_num = (rank - 1) * G.TILE_COUNT + file - 1
    return tile_num

# Convert Tile Number to Position
def tile_num_to_pos(tile_num):
    rank = math.ceil((tile_num + 1) / G.TILE_COUNT)
    file = (tile_num + 1) - ((rank - 1) * G.TILE_COUNT)

    tile_x = ((file - 1) * G.TILE_SIZE) + G.LABEL_SIZE
    tile_y = G.BOARD_SIZE - (rank * G.TILE_SIZE)
    tile_position = (tile_x, tile_y)
    return tile_position

# Print Standard Algebraic Notation for Move to Output
def print_san(move):
    if G.BOARD.turn == chess.WHITE:
        print("{0:>4}".format(str(G.BOARD.fullmove_number) + '.'), end='\t')
        print("{0:<8}".format(G.BOARD.san(move)), end='', flush='True')
    else:
        print(G.BOARD.san(move))

# Determine the Results String to Display Based on Outcome
def determine_outcome(outcome):
    if outcome.termination == chess.Termination.CHECKMATE:
        if outcome.winner == chess.WHITE:
            display_results("MATE: WHITE WINS!")
        else:
            display_results("MATE: BLACK WINS!")
    elif outcome.termination == chess.Termination.STALEMATE:
        display_results("DRAW: STALEMATE!")
    elif outcome.termination == chess.Termination.INSUFFICIENT_MATERIAL:
        display_results("DRAW: DEAD POSITION!")
    elif outcome.termination == chess.Termination.SEVENTYFIVE_MOVES:
        display_results("DRAW: 75 MOVE RULE!")
    elif outcome.termination == chess.Termination.FIVEFOLD_REPETITION:
        display_results("DRAW: 5 REPEAT RULE!")
    elif outcome.termination == chess.Termination.FIFTY_MOVES:
        display_results("DRAW: 50 MOVE RULE!")
    elif outcome.termination == chess.Termination.THREEFOLD_REPETITION:
        display_results("DRAW: 3 REPEAT RULE!")

# Display the Results String on the Board
def display_results(results):
    (result_w, result_h) = result_font.size(results)
    result_pos_x = (G.SCREEN_SIZE - result_w) / 2
    result_pos_y = (G.BOARD_SIZE - result_h) / 2
    result_pos = (result_pos_x, result_pos_y)

    result_label = result_font.render(results, True, G.BLACK)
    G.SCREEN.blit(result_label, result_pos)

# Select a Square & Highlight Potential Moves
def make_selection(tile_num):
    if G.BOARD.color_at(tile_num) == G.BOARD.turn:
        draw_select_square(tile_num)
    for move in G.BOARD.legal_moves:
        if move.from_square == tile_num:
            draw_move_circle(move.to_square)
    return tile_num

# Draw the Square Select Highlight on the Clicked Square
def draw_select_square(tile_num):
    (tile_x, tile_y) = tile_num_to_pos(tile_num)
    offset = (1 - G.SELECT_SCALE) / 2 * G.TILE_SIZE
    select_position = (tile_x + offset, tile_y + offset)
    select_size = G.TILE_SIZE * G.SELECT_SCALE
    select_dimensions = (select_size, select_size)
    select_rect = pygame.Rect(select_position, select_dimensions)

    if G.BOARD.turn == chess.WHITE:
        pygame.draw.rect(G.SCREEN, G.L_SELECT_COLOR, select_rect)
    elif G.BOARD.turn == chess.BLACK:
        pygame.draw.rect(G.SCREEN, G.D_SELECT_COLOR, select_rect)
    pygame.draw.rect(G.SCREEN, G.LINE_COLOR, select_rect, G.LINE_SIZE)

# Draw the Move Option Highlight on a Potential Move
def draw_move_circle(tile_num):
    (tile_x, tile_y) = tile_num_to_pos(tile_num)
    center_x = tile_x + (G.TILE_SIZE / 2)
    center_y = tile_y + (G.TILE_SIZE / 2)
    tile_center = (center_x, center_y)
    radius = G.TILE_SIZE / 2 * G.MOVE_SCALE

    if G.BOARD.turn == chess.WHITE:
        pygame.draw.circle(G.SCREEN, G.L_SELECT_COLOR, tile_center, radius)
    elif G.BOARD.turn == chess.BLACK:
        pygame.draw.circle(G.SCREEN, G.D_SELECT_COLOR, tile_center, radius)
    pygame.draw.circle(G.SCREEN, G.LINE_COLOR, tile_center, radius, G.LINE_SIZE)

# Draw a Chess Piece
def draw_piece(tile_num, piece_type, piece_color):
    (tile_x, tile_y) = tile_num_to_pos(tile_num)
    piece_size = G.TILE_SIZE * G.PIECE_SCALE
    piece_dimensions = (piece_size, piece_size)
    piece_x = tile_x + ((G.TILE_SIZE - piece_size) / 2)
    piece_y = tile_y + ((G.TILE_SIZE - piece_size) / 2)
    piece_position = (piece_x, piece_y)

    if piece_color == chess.WHITE:
        if piece_type == chess.PAWN:
            piece_image = w_pawn_img
        elif piece_type == chess.KNIGHT:
            piece_image = w_knight_img
        elif piece_type == chess.BISHOP:
            piece_image = w_bishop_img
        elif piece_type == chess.ROOK:
            piece_image = w_rook_img
        elif piece_type == chess.QUEEN:
            piece_image = w_queen_img
        elif piece_type == chess.KING:
            piece_image = w_king_img
    elif piece_color == chess.BLACK:
        if piece_type == chess.PAWN:
            piece_image = b_pawn_img
        elif piece_type == chess.KNIGHT:
            piece_image = b_knight_img
        elif piece_type == chess.BISHOP:
            piece_image = b_bishop_img
        elif piece_type == chess.ROOK:
            piece_image = b_rook_img
        elif piece_type == chess.QUEEN:
            piece_image = b_queen_img
        elif piece_type == chess.KING:
            piece_image = b_king_img

    final_image = pygame.transform.scale(piece_image, piece_dimensions)
    final_rect = final_image.get_rect()
    final_rect.update(piece_position, piece_dimensions)
    G.SCREEN.blit(final_image, final_rect)

# Draw the Chess Board
def draw_board():
    G.SCREEN.fill(G.LABEL_COLOR)
    screen_rect = G.SCREEN.get_rect()
    pygame.draw.rect(G.SCREEN, G.BORDER_COLOR, screen_rect, G.BORDER_SIZE)

    for file in range(G.TILE_COUNT):
        file_label = label_font.render(chr(file + 97), True, G.BLACK)
        file_x = G.LABEL_SIZE + (file * G.TILE_SIZE) + (G.TILE_SIZE / 2) - (font_size / 4)
        file_position = (file_x, G.BOARD_SIZE + (G.LABEL_SIZE * 0.1))
        G.SCREEN.blit(file_label, file_position)

        for rank in range(G.TILE_COUNT):
            rank_label = label_font.render(str(rank + 1), True, G.BLACK)
            rank_y = G.BOARD_SIZE - (rank * G.TILE_SIZE) - (G.TILE_SIZE / 2) - (font_size / 2)
            rank_position = (G.LABEL_SIZE * 0.3, rank_y)
            G.SCREEN.blit(rank_label, rank_position)

            tile_position = ((file * G.TILE_SIZE) + G.LABEL_SIZE, rank * G.TILE_SIZE)
            tile_rect = pygame.Rect(tile_position, G.TILE_DIMENSIONS)

            if (file + rank) % 2 == 0:
                G.SCREEN.fill(G.LIGHT_COLOR, tile_rect)
            else:
                G.SCREEN.fill(G.DARK_COLOR, tile_rect)
            pygame.draw.rect(G.SCREEN, G.BORDER_COLOR, tile_rect, G.BORDER_SIZE)
