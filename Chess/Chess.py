import pygame
import chess
import os
import random

# Configuración inicial
WIDTH, HEIGHT = 512, 512
DIMENSION = 8  # 8x8 tablero
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15

IMAGES = {}

def generate_images():
    if not os.path.exists("images"):
        os.makedirs("images")

    files_colors_letters = [
        ("images/wk.png", (200, 200, 200), "K"),  # Rey blanco
        ("images/wr.png", (150, 150, 150), "R"),  # Torre blanca
        ("images/bk.png", (50, 50, 50), "K"),     # Rey negro
    ]

    for path, color, letter in files_colors_letters:
        if not os.path.isfile(path):
            surf = pygame.Surface((SQ_SIZE, SQ_SIZE))
            surf.fill(pygame.Color("white"))
            pygame.draw.rect(surf, color, (10, 10, SQ_SIZE - 20, SQ_SIZE - 20))
            font = pygame.font.SysFont("Arial", 36, bold=True)
            text = font.render(letter, True, pygame.Color("black" if color != (50, 50, 50) else "white"))
            text_rect = text.get_rect(center=(SQ_SIZE//2, SQ_SIZE//2))
            surf.blit(text, text_rect)
            pygame.image.save(surf, path)

def load_images():
    pieces = ['wk', 'wr', 'bk']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(
            pygame.image.load(os.path.join("images", piece + ".png")),
            (SQ_SIZE, SQ_SIZE)
        )

def draw_board(screen):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, board):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            row = 7 - (square // 8)
            col = square % 8
            color = 'w' if piece.color == chess.WHITE else 'b'
            name = piece.symbol().lower()
            key = color + name
            if key in IMAGES:
                screen.blit(IMAGES[key], pygame.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def get_square_under_mouse():
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    x, y = [int(v // SQ_SIZE) for v in mouse_pos]
    if 0 <= x < DIMENSION and 0 <= y < DIMENSION:
        return chess.square(x, 7 - y)
    return None

def show_message(screen, white_won):
    pass


def generate_random_position():
    # Genera posiciones aleatorias para rey blanco, 2 torres blancas y rey negro sin superposiciones y legales
    squares = list(range(64))
    random.shuffle(squares)

    # El rey blanco no debe estar en jaque al inicio, ni las torres sobre el rey blanco
    # Solo aseguramos que no se superpongan para simplificar
    positions = {}

    # Colocar rey blanco
    king_white = squares.pop()
    positions['wk'] = king_white

    # Colocar 2 torres blancas
    rooks = []
    for _ in range(2):
        while True:
            sq = squares.pop()
            if sq != king_white:
                rooks.append(sq)
                break
    positions['wr1'] = rooks[0]
    positions['wr2'] = rooks[1]

    # Colocar rey negro (falta)

def create_board_from_positions(pos):
    pass

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rey y Dos Torres vs Rey")
    clock = pygame.time.Clock()

    generate_images()
    load_images()

    positions = generate_random_position()
    board = create_board_from_positions(positions)

    selected_square = None
    player_turn = True  # True = blanco (usuario), False = negro (computadora)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and player_turn:
                sq = get_square_under_mouse()
                if sq is not None:
                    piece = board.piece_at(sq)
                    if selected_square is None:
                        if piece and piece.color == chess.WHITE:
                            selected_square = sq
                    else:
                        move = chess.Move(selected_square, sq)
                        if move in board.legal_moves:
                            board.push(move)
                            selected_square = None
                            player_turn = False
                        else:
                            selected_square = None

        # Turno computadora: Rey negro mueve aleatoriamente (falta)

        # Detectar fin de juego y mostrar mensaje (falta)
        pygame.display.flip()
        clock.tick(MAX_FPS)


    pygame.quit()

if __name__ == "__main__":
    main()
