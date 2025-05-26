import pygame # Importa la librería Pygame para la interfaz gráfica
import chess # Importa la librería python-chess para la lógica del ajedrez

class ChessGUI:
    def __init__(self, square_size=80):
        # Inicializa todos los módulos importados de Pygame
        pygame.init() 
        
        self.square_size = square_size # Define el tamaño de cada casilla del tablero en píxeles (ej. 80x80)
        # Calcula el ancho y alto de la ventana del juego (8 casillas x tamaño de casilla)
        self.width = 8 * self.square_size
        self.height = 8 * self.square_size
        
        # Crea la ventana de visualización de Pygame
        self.screen = pygame.display.set_mode((self.width, self.height))
        # Establece el título de la ventana del juego
        pygame.display.set_caption("Two Rooks vs. King Endgame")

        # Define un diccionario con los colores usados para dibujar el tablero y resaltados
        self.colors = {
            "light_square": (234, 234, 210),  # Color para casillas claras
            "dark_square": (120, 150, 86),   # Color para casillas oscuras
            "selected_square": (255, 255, 100), # Color amarillo para la casilla de la pieza seleccionada
            "highlight_move": (100, 200, 255, 150) # Azul semi-transparente para resaltar movimientos legales
        }
        
        # Carga las imágenes de las piezas de ajedrez
        self.pieces = self.load_pieces()
        self.selected_square = None # Almacena la casilla de la pieza que el usuario ha seleccionado (para mover)
        self.dragging_piece = None # Almacena la pieza que se está arrastrando con el mouse
        self.drag_offset_x, self.drag_offset_y = 0, 0 # Desplazamiento para que la pieza se arrastre suavemente desde el clic
        self.board = None # El objeto 'chess.Board' se inicializará después de la fase de configuración

        # --- Variables del Modo de Configuración ---
        self.setup_mode = True # Indica si el juego está en la fase de configuración de piezas
        self.current_piece_to_place = chess.KING # La primera pieza que el usuario debe colocar (Rey Blanco)
        self.white_rooks_placed = 0 # Contador para saber cuántas torres blancas se han colocado
        self.setup_message = "" # Mensaje que se muestra al usuario durante la configuración
        self.update_setup_message() # Actualiza el mensaje inicial de configuración


    def load_pieces(self):
        """
        Carga las imágenes de las piezas de ajedrez desde la carpeta 'pieces'.
        """
        pieces = {} # Diccionario para almacenar las superficies de las imágenes de las piezas
        # Nombres de archivo de las imágenes de las piezas que necesitamos para este final de juego
        piece_names = {
            'K': 'white_king.png', # Rey Blanco
            'R': 'white_rook.png', # Torre Blanca
            'k': 'black_king.png'  # Rey Negro
        }
        
        # Itera sobre el diccionario para cargar cada imagen
        for piece_symbol, filename in piece_names.items():
            try:
                # Construye la ruta completa a la imagen. Se espera una carpeta 'pieces'
                # en el mismo directorio que el script.
                img_path = f"pieces/{filename}"
                # Carga la imagen y la convierte para un rendimiento óptimo con transparencia
                image = pygame.image.load(img_path).convert_alpha()
                # Escala la imagen al tamaño de la casilla y la guarda en el diccionario
                pieces[piece_symbol] = pygame.transform.scale(image, (self.square_size, self.square_size))
            except pygame.error as e:
                # Si hay un error al cargar la imagen, imprime un mensaje de error
                print(f"Error loading piece image {filename}: {e}")
                pieces[piece_symbol] = None # Marca la pieza como no cargada (para usar un fallback visual)
        return pieces

    def draw_board(self):
        """
        Dibuja las casillas del tablero de ajedrez.
        Alterna los colores de las casillas.
        """
        for row in range(8):
            for col in range(8):
                # Determina el color de la casilla (claro u oscuro)
                color = self.colors["light_square"] if (row + col) % 2 == 0 else self.colors["dark_square"]
                # Dibuja un rectángulo para cada casilla
                pygame.draw.rect(self.screen, color, (col * self.square_size, row * self.square_size, self.square_size, self.square_size))

    def draw_pieces(self):
        """
        Dibuja las piezas de ajedrez en sus posiciones actuales en el tablero.
        """
        # Si el tablero aún no está configurado (al inicio de la fase de setup), no dibuja piezas.
        if not self.board: 
            return

        # Itera sobre todas las 64 casillas del tablero
        for square in chess.SQUARES:
            # Obtiene la pieza en la casilla actual
            piece = self.board.piece_at(square)
            if piece:
                # En modo de juego, si una pieza se está arrastrando, no la dibuja en su posición original.
                if self.dragging_piece and square == self.selected_square and not self.setup_mode:
                    continue 

                piece_symbol = piece.symbol() # Obtiene el símbolo de la pieza (ej. 'K' para Rey Blanco)
                img = self.pieces.get(piece_symbol) # Obtiene la imagen correspondiente a la pieza
                if img:
                    col = chess.square_file(square) # Columna de la casilla (0-7)
                    row = 7 - chess.square_rank(square) # Fila de la casilla (invertida para coordenadas de Pygame)
                    # Dibuja la imagen de la pieza en la posición correcta
                    self.screen.blit(img, (col * self.square_size, row * self.square_size))
                else:
                    # Alternativa si la imagen de la pieza no se cargó: dibuja un círculo de color
                    center_x = chess.square_file(square) * self.square_size + self.square_size // 2
                    center_y = (7 - chess.square_rank(square)) * self.square_size + self.square_size // 2
                    color = (255, 0, 0) if piece.color == chess.WHITE else (0, 0, 0)
                    pygame.draw.circle(self.screen, color, (center_x, center_y), self.square_size // 3)

    def draw_selected_square(self):
        """
        Resalta la casilla actualmente seleccionada con un borde amarillo.
        Solo se usa en el modo de juego.
        """
        if self.selected_square is not None and not self.setup_mode: # Solo resalta en modo de juego
            col = chess.square_file(self.selected_square) # Columna de la casilla seleccionada
            row = 7 - chess.square_rank(self.selected_square) # Fila (invertida)
            # Dibuja un rectángulo de borde alrededor de la casilla seleccionada
            pygame.draw.rect(self.screen, self.colors["selected_square"],
                             (col * self.square_size, row * self.square_size, self.square_size, self.square_size), 3) # El '3' es el grosor del borde

    def draw_legal_moves(self):
        """
        Resalta las casillas a las que la pieza seleccionada puede moverse legalmente.
        Solo se usa en el modo de juego.
        """
        if self.selected_square is not None and not self.setup_mode: # Solo resalta en modo de juego
            # Crea una superficie semi-transparente para el resaltado
            s = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
            s.fill(self.colors["highlight_move"]) # Rellena con el color azul semi-transparente

            # Itera sobre todos los movimientos legales en el tablero
            for move in self.board.legal_moves:
                # Si el movimiento comienza desde la casilla seleccionada
                if move.from_square == self.selected_square:
                    to_col = chess.square_file(move.to_square) # Columna de la casilla de destino
                    to_row = 7 - chess.square_rank(move.to_square) # Fila de la casilla de destino (invertida)
                    # Dibuja la superficie semi-transparente en la casilla de destino
                    self.screen.blit(s, (to_col * self.square_size, to_row * self.square_size))

    def draw_dragging_piece(self):
        """
        Dibuja la pieza que el usuario está arrastrando en la posición actual del mouse.
        Solo se usa en el modo de juego.
        """
        # Si hay una pieza siendo arrastrada y su imagen está cargada, y NO estamos en modo de configuración
        if self.dragging_piece and self.pieces.get(self.dragging_piece.symbol()) and not self.setup_mode:
            mouse_x, mouse_y = pygame.mouse.get_pos() # Obtiene la posición actual del mouse
            img = self.pieces[self.dragging_piece.symbol()] # Obtiene la imagen de la pieza arrastrada
            # Dibuja la imagen de la pieza ajustando con el offset para que siga el cursor
            self.screen.blit(img, (mouse_x - self.drag_offset_x, mouse_y - self.drag_offset_y))

    def draw_text(self, text, x, y, color=(255, 255, 255), size=30):
        """
        Dibuja texto en la pantalla en una posición específica.
        """
        font = pygame.font.Font(None, size) # Crea una fuente de texto
        text_surface = font.render(text, True, color) # Renderiza el texto
        text_rect = text_surface.get_rect(center=(x, y)) # Obtiene el rectángulo del texto y lo centra
        self.screen.blit(text_surface, text_rect) # Dibuja el texto en la pantalla

    def update_display(self):
        """
        Actualiza y refresca toda la pantalla del juego.
        Se llama en cada iteración del bucle principal.
        """
        self.draw_board() # Dibuja el tablero
        self.draw_selected_square() # Dibuja el resaltado de la casilla seleccionada
        self.draw_legal_moves() # Dibuja los resaltados de movimientos legales
        self.draw_pieces() # Dibuja todas las piezas en el tablero
        self.draw_dragging_piece() # Dibuja la pieza que se está arrastrando (si aplica)

        # Si estamos en modo de configuración, dibuja los mensajes de ayuda al usuario
        if self.setup_mode:
            # Crea una superficie semi-transparente para oscurecer un poco el tablero
            s = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            s.fill((0, 0, 0, 100)) # Color negro semi-transparente
            self.screen.blit(s, (0,0)) # Dibuja esta superficie sobre el tablero

            # Dibuja los mensajes de instrucciones para la configuración
            self.draw_text(self.setup_message, self.width // 2, self.height // 2 - 50, color=(255, 255, 0)) # Mensaje principal
            self.draw_text("Click to place. Right-click to remove.", self.width // 2, self.height // 2, size=24) # Instrucciones de clic
            # Muestra un mensaje para iniciar el juego una vez que todas las piezas estén colocadas
            if self.white_rooks_placed == 2 and self.current_piece_to_place is None:
                 self.draw_text("Press ENTER to start game.", self.width // 2, self.height // 2 + 50, color=(0, 255, 0))

        pygame.display.flip() # Actualiza la pantalla completa para mostrar todo lo dibujado

    def get_square_from_coords(self, x, y):
        """
        Convierte las coordenadas de píxeles del mouse a la casilla de ajedrez (0-63).
        """
        col = x // self.square_size # Columna del tablero
        row = 7 - (y // self.square_size) # Fila del tablero (invertida porque Y en Pygame va de arriba a abajo)
        return chess.square(col, row) # Devuelve la constante de la casilla de python-chess

    # --- Lógica del Modo de Configuración ---
    def update_setup_message(self):
        """
        Actualiza el mensaje que se muestra al usuario durante la fase de configuración,
        indicando qué pieza debe colocar a continuación.
        """
        if self.current_piece_to_place == chess.KING and self.board is None:
            self.setup_message = "Place White King" # Mensaje inicial si el tablero está vacío
        elif self.current_piece_to_place == chess.ROOK:
            self.setup_message = f"Place White Rook {self.white_rooks_placed + 1} (2 needed)" # Mensaje para colocar torres
        elif self.current_piece_to_place == chess.KING and self.board and self.board.king(chess.BLACK) is None:
            self.setup_message = "Place Black King" # Mensaje para colocar el Rey Negro
        else:
            self.setup_message = "All pieces placed." # Mensaje cuando todas las piezas requeridas están en su lugar

    def place_piece_at_mouse(self, mouse_pos):
        """
        Intenta colocar la pieza 'actual' en la casilla donde el usuario hizo clic.
        """
        square = self.get_square_from_coords(*mouse_pos) # Obtiene la casilla de ajedrez desde la posición del mouse

        # Si la casilla ya está ocupada, imprime un mensaje y no hace nada
        if self.board.piece_at(square) is not None:
            print("Square is already occupied. Choose an empty square.")
            return

        # Lógica para colocar cada tipo de pieza en secuencia
        if self.current_piece_to_place == chess.KING and self.board.king(chess.WHITE) is None:
            self.board.set_piece_at(square, chess.Piece(chess.KING, chess.WHITE)) # Coloca el Rey Blanco
            self.current_piece_to_place = chess.ROOK # La siguiente pieza a colocar será una torre
        elif self.current_piece_to_place == chess.ROOK and self.white_rooks_placed < 2:
            self.board.set_piece_at(square, chess.Piece(chess.ROOK, chess.WHITE)) # Coloca una Torre Blanca
            self.white_rooks_placed += 1 # Incrementa el contador de torres colocadas
            if self.white_rooks_placed == 2:
                self.current_piece_to_place = chess.KING # Después de 2 torres, la siguiente es el Rey Negro
        elif self.current_piece_to_place == chess.KING and self.board.king(chess.BLACK) is None:
            self.board.set_piece_at(square, chess.Piece(chess.KING, chess.BLACK)) # Coloca el Rey Negro
            self.current_piece_to_place = None # Todas las piezas requeridas han sido colocadas
        
        self.update_setup_message() # Actualiza el mensaje para reflejar la pieza que se espera

    def remove_piece_at_mouse(self, mouse_pos):
        """
        Elimina una pieza de la casilla donde el usuario hizo clic derecho durante la configuración.
        """
        square = self.get_square_from_coords(*mouse_pos) # Obtiene la casilla de ajedrez
        piece = self.board.piece_at(square) # Obtiene la pieza en esa casilla

        if piece:
            self.board.remove_piece_at(square) # Elimina la pieza del tablero
            # Ajusta el estado de la configuración si se elimina una pieza crítica
            if piece.piece_type == chess.KING and piece.color == chess.WHITE:
                self.current_piece_to_place = chess.KING # Vuelve a la fase de colocar el Rey Blanco
            elif piece.piece_type == chess.ROOK and piece.color == chess.WHITE:
                self.white_rooks_placed = max(0, self.white_rooks_placed - 1) # Decrementa el contador de torres
                self.current_piece_to_place = chess.ROOK # Vuelve a la fase de colocar torres
            elif piece.piece_type == chess.KING and piece.color == chess.BLACK:
                self.current_piece_to_place = chess.KING # Vuelve a la fase de colocar el Rey Negro
            self.update_setup_message() # Actualiza el mensaje de configuración

    def run_setup_phase(self):
        """
        Gestiona la fase interactiva de colocación de piezas por parte del usuario.
        """
        # Inicializa un tablero vacío para la configuración
        self.board = chess.Board("8/8/8/8/8/8/8/8 w - - 0 1") 
        self.setup_mode = True # Establece el modo de configuración a verdadero
        
        # Bucle principal de la fase de configuración
        while self.setup_mode:
            self.update_display() # Actualiza la pantalla para mostrar el tablero y los mensajes de setup
            for event in pygame.event.get(): # Procesa los eventos de Pygame
                if event.type == pygame.QUIT: # Si el usuario cierra la ventana
                    pygame.quit() # Cierra Pygame
                    exit() # Sale del programa
                elif event.type == pygame.MOUSEBUTTONDOWN: # Si se presiona un botón del mouse
                    if event.button == 1: # Clic izquierdo para colocar pieza
                        self.place_piece_at_mouse(event.pos)
                    elif event.button == 3: # Clic derecho para eliminar pieza
                        self.remove_piece_at_mouse(event.pos)
                elif event.type == pygame.KEYDOWN: # Si se presiona una tecla
                    if event.key == pygame.K_RETURN and self.current_piece_to_place is None:
                        # Verifica si todas las piezas necesarias han sido colocadas antes de iniciar el juego
                        if (self.board.king(chess.WHITE) is not None and # Rey Blanco
                            len(self.board.pieces(chess.ROOK, chess.WHITE)) == 2 and # Dos Torres Blancas
                            self.board.king(chess.BLACK) is not None): # Rey Negro
                            self.setup_mode = False # Sale del modo de configuración
                            self.board.turn = chess.WHITE # Asegura que sea el turno de Blancas al iniciar el juego
                        else:
                            # Si faltan piezas, muestra un mensaje de advertencia
                            self.setup_message = "Missing pieces! Need 1 WK, 2 WR, 1 BK."
                            self.update_display() # Actualiza la pantalla con el mensaje
                            pygame.time.wait(1500) # Espera 1.5 segundos para que el usuario lea el mensaje
                            self.update_setup_message() # Vuelve al mensaje de colocación de piezas
            pygame.time.Clock().tick(60) # Limita la velocidad de fotogramas a 60 FPS
        
        return self.board # Devuelve el tablero configurado para el juego

    # --- Lógica del Modo de Juego (similar a la versión anterior) ---
    def get_user_move(self):
        """
        Espera y devuelve un movimiento válido del usuario (Negras) durante el juego.
        """
        while True: # Bucle infinito hasta que se obtiene un movimiento válido o se sale
            for event in pygame.event.get(): # Procesa los eventos de Pygame
                if event.type == pygame.QUIT: # Si el usuario cierra la ventana
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN: # Si el usuario hace clic hacia abajo
                    self.handle_mouse_down(event) # Maneja la selección de piezas
                elif event.type == pygame.MOUSEBUTTONUP: # Si el usuario suelta el clic
                    move = self.handle_mouse_up(event) # Intenta hacer el movimiento
                    if move: # Si el movimiento es válido, lo devuelve
                        return move
                elif event.type == pygame.MOUSEMOTION and self.dragging_piece: # Si el mouse se mueve y hay una pieza arrastrándose
                    self.update_display() # Actualiza la pantalla para mostrar la pieza arrastrándose
            pygame.time.Clock().tick(60) # Limita la velocidad de fotogramas

    def handle_mouse_down(self, event):
        """
        Maneja los eventos de clic del mouse hacia abajo durante el modo de juego.
        Selecciona la pieza a arrastrar si es del color correcto.
        """
        if self.setup_mode: return # No hace nada si todavía está en modo de configuración

        mouse_x, mouse_y = event.pos # Posición X, Y del mouse
        clicked_square = self.get_square_from_coords(mouse_x, mouse_y) # Casilla clicada
        piece_at_square = self.board.piece_at(clicked_square) # Pieza en la casilla clicada

        # Si hay una pieza y es del color del turno actual (Negras para el usuario)
        if piece_at_square and piece_at_square.color == self.board.turn: 
            self.selected_square = clicked_square # Guarda la casilla seleccionada
            self.dragging_piece = piece_at_square # Guarda la pieza que se arrastrará
            # Calcula el offset para que la pieza se arrastre desde el punto exacto donde se hizo clic
            piece_x = chess.square_file(clicked_square) * self.square_size
            piece_y = (7 - chess.square_rank(clicked_square)) * self.square_size
            self.drag_offset_x = mouse_x - piece_x
            self.drag_offset_y = mouse_y - piece_y
        else:
            self.selected_square = None # Deselecciona si no se clicó una pieza válida
            self.dragging_piece = None

    def handle_mouse_up(self, event):
        """
        Maneja los eventos de soltar el clic del mouse durante el modo de juego.
        Intenta realizar el movimiento si es legal.
        """
        if self.setup_mode: return None # No hace nada si todavía está en modo de configuración

        if self.selected_square is None: # Si no había una pieza seleccionada para mover
            return None

        mouse_x, mouse_y = event.pos # Posición X, Y del mouse al soltar
        target_square = self.get_square_from_coords(mouse_x, mouse_y) # Casilla de destino

        move = chess.Move(self.selected_square, target_square) # Crea un objeto de movimiento

        self.selected_square = None # Deselecciona la casilla
        self.dragging_piece = None # Deja de arrastrar la pieza
        self.update_display() # Actualiza la pantalla para limpiar los resaltados

        if move in self.board.legal_moves: # Si el movimiento es legal
            return move # Devuelve el movimiento
        else:
            print("Illegal move. Please try again.") # Mensaje si el movimiento es ilegal
            return None # No devuelve ningún movimiento válido

    def show_game_over_screen(self, message):
        """
        Muestra una pantalla de fin de juego con un mensaje.
        """
        # Crea una superficie semi-transparente para oscurecer el tablero
        s = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128)) # Negro semi-transparente
        self.screen.blit(s, (0,0)) # Dibuja la superficie sobre el tablero

        # Dibuja el mensaje de fin de juego y las instrucciones para salir
        self.draw_text(message, self.width // 2, self.height // 2, color=(255, 0, 0))
        self.draw_text("Press any key to exit.", self.width // 2, self.height // 2 + 50, size=24)
        pygame.display.flip() # Actualiza la pantalla para mostrar el mensaje

        waiting = True # Bucle para esperar una pulsación de tecla antes de salir
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Si el usuario cierra la ventana
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN: # Si se presiona cualquier tecla
                    waiting = False # Sale del bucle de espera
        pygame.quit() # Cierra Pygame al salir