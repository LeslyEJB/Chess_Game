import chess
import chess.engine
import pygame
from Minimax import find_best_move # Importa la función principal del algoritmo Minimax
from Heuristic import CHECKMATE_SCORE # Importa la constante de puntuación de jaque mate
from ChessGUI import ChessGUI # Importa la clase de la interfaz gráfica de usuario

# --- Bucle Principal del Juego (Main Game Loop) ---
def main():
    # Inicializa la interfaz gráfica de usuario
    # Esto también configura la ventana de Pygame.
    gui = ChessGUI() 

    print("Starting setup phase...") # Mensaje para la consola indicando el inicio de la fase de configuración

    # Ejecuta la fase de configuración visual, donde el usuario coloca las piezas.
    # El método run_setup_phase() en ChessGUI devuelve el objeto Board ya configurado.
    board = gui.run_setup_phase() 
    print("Setup complete! Starting game.") # Mensaje para la consola indicando que la configuración ha terminado

    # Define la profundidad máxima para el algoritmo Minimax.
    # Un valor más alto hace que la IA sea más 'inteligente' pero también más lenta.
    MAX_DEPTH = 4 # Ajusta este valor para controlar la fuerza de la IA

    running = True # Variable de control para mantener el bucle del juego activo
    while running:
        # Actualiza y dibuja la interfaz gráfica del tablero en cada iteración del bucle.
        gui.update_display() 
        
        # --- Comprobación de Fin de Juego ---
        # Verifica si el juego ha terminado (jaque mate, ahogado, etc.).
        if board.is_game_over():
            # Si es jaque mate
            if board.is_checkmate():
                # Si es el turno de BLANCAS, significa que NEGRAS ha sido jaque mate por BLANCAS
                if board.turn == chess.WHITE:
                    gui.show_game_over_screen("Black is checkmated! White wins!") # Muestra mensaje de victoria de Blancas
                # Si es el turno de NEGRAS, significa que BLANCAS ha sido jaque mate por NEGRAS
                else:
                    gui.show_game_over_screen("White is checkmated! Black wins!") # Muestra mensaje de victoria de Negras
            # Si es ahogado (stalemate)
            elif board.is_stalemate():
                gui.show_game_over_screen("It's a stalemate!") # Muestra mensaje de ahogado
            # Otros casos de fin de juego (material insuficiente, repetición, etc.)
            else:
                gui.show_game_over_screen("Game Over!") # Muestra mensaje genérico de fin de juego
            
            running = False # Detiene el bucle principal del juego
            break # Sale del bucle

        # --- Turno de Blancas (IA) ---
        # Si es el turno de las piezas blancas
        if board.turn == chess.WHITE:
            print("White's turn (AI thinking)...") # Mensaje en consola indicando que la IA está pensando

            # Encuentra el mejor movimiento para BLANCAS usando el algoritmo Minimax.
            # El MAX_DEPTH determina qué tan 'profundo' busca la IA.
            best_move = find_best_move(board, MAX_DEPTH)
            
            # Si la IA encuentra un movimiento legal
            if best_move:
                board.push(best_move) # Realiza el movimiento en el tablero
                print(f"White (AI) plays: {best_move.uci()}") # Muestra el movimiento de la IA en formato UCI
            # Si la IA no tiene movimientos legales (debería ser un ahogado o jaque mate ya manejado)
            else:
                print("White (AI) has no legal moves. Game over (stalemate/no moves).")
                running = False # Detiene el juego
        # --- Turno de Negras (Usuario) ---
        # Si es el turno de las piezas negras (el usuario)
        else: 
            print("Black's turn (Your turn). Click and drag pieces on the board.") # Instrucciones para el usuario
            
            # Obtiene el movimiento del usuario a través de la interfaz gráfica.
            # Este método espera hasta que el usuario realice un movimiento válido.
            user_move = gui.get_user_move()
            
            # Si el usuario realizó un movimiento válido
            if user_move:
                board.push(user_move) # Realiza el movimiento en el tablero
                print(f"Black (You) plays: {user_move.uci()}") # Muestra el movimiento del usuario en formato UCI
            # Si el usuario cierra la ventana durante su turno
            else: 
                running = False # Detiene el juego

        # --- Manejo de Eventos de Pygame (para salir del juego) ---
        # Itera sobre los eventos de Pygame para permitir al usuario cerrar la ventana en cualquier momento.
        for event in pygame.event.get():
            # Si el usuario cierra la ventana (hace clic en la 'X')
            if event.type == pygame.QUIT:
                running = False # Detiene el bucle principal del juego
                break # Sale del bucle for, y el bucle while también terminará

    pygame.quit() # Cierra y desinicializa Pygame
    print("\n--- Game Exited ---") # Mensaje final al salir del juego

# Punto de entrada principal del programa
if __name__ == "__main__":
    main()