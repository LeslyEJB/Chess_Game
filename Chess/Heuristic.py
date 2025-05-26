import chess # Importa la librería python-chess para la lógica del ajedrez
import math # Importa el módulo math para usar 'inf' (infinito)

# --- Constantes de Puntuación ---
# Se utiliza un valor muy alto para el jaque mate para que la IA siempre lo priorice.
CHECKMATE_SCORE = 1000000 
# La puntuación para un ahogado (stalemate) o un empate por material insuficiente o repetición.
# Un valor de 0 indica que es un resultado neutral, ni bueno ni malo (un empate).
STALEMATE_SCORE = 0

def evaluate_board(board):
    """
    Evalúa la posición actual del tablero desde la perspectiva de las piezas Blancas.
    
    Valores positivos altos son buenos para Blancas (buscando ganar).
    Valores negativos altos son buenos para Negras (buscando evitar la derrota, lo que es malo para Blancas).
    
    Args:
        board (chess.Board): El objeto del tablero de ajedrez en su estado actual.
        
    Returns:
        int: La puntuación de la posición.
    """
    # --- Casos Base de Evaluación (Fin del Juego) ---
    # Si el juego ha terminado en jaque mate
    if board.is_checkmate():
        # Si es el turno de NEGRAS y el tablero está en jaque mate, significa que BLANCAS
        # acaba de hacer el jaque mate, lo cual es una victoria para BLANCAS.
        return CHECKMATE_SCORE
        # Si es el turno de BLANCAS y el tablero está en jaque mate, significa que NEGRAS
        # acaba de hacer el jaque mate, lo cual es una victoria para NEGRAS (y una derrota para BLANCAS).
        # Esto no debería ocurrir si la IA de Blancas juega correctamente.
    elif board.is_stalemate() or board.is_insufficient_material() or board.is_repetition():
        # Si el juego es un ahogado (stalemate), o hay material insuficiente para dar jaque mate,
        # o hay una repetición de movimientos (tres veces la misma posición).
        # En estos casos, el juego es un empate, por lo que se devuelve una puntuación neutral.
        return STALEMATE_SCORE

    # --- Heurística para el Final de Juego de Dos Torres y Rey vs. Rey Solo ---
    # El objetivo principal de esta heurística es incentivar a las Blancas a empujar
    # al Rey Negro hacia los bordes del tablero, donde es más fácil dar jaque mate.

    # Obtiene la casilla donde se encuentra el Rey Negro.
    black_king_square = board.king(chess.BLACK)
    # Esta comprobación es una salvaguarda; en un estado de juego válido, el rey siempre debería existir.
    if black_king_square is None: 
        return STALEMATE_SCORE # Si por alguna razón no se encuentra el rey negro, se considera un empate.

    # Obtiene la fila (rank) y columna (file) del Rey Negro.
    rank = chess.square_rank(black_king_square) # Fila (0-7)
    file = chess.square_file(black_king_square) # Columna (0-7)

    # --- Cálculo de la Distancia al Centro ---
    # Las casillas centrales son aproximadamente d4, d5, e4, e5.
    # Queremos que el Rey Negro esté lo más lejos posible del centro, es decir, cerca de los bordes.
    # La distancia máxima al centro (desde una esquina) es 3.5 para fila y columna.
    dist_to_center_rank = abs(rank - 3.5) # Distancia de la fila al centro (3.5 es entre filas 3 y 4)
    dist_to_center_file = abs(file - 3.5) # Distancia de la columna al centro (3.5 es entre columnas d y e)
    
    # Una combinación lineal simple para la puntuación de la posición del rey.
    # Un valor más alto significa que el Rey Negro está más cerca del borde, lo cual es bueno para Blancas.
    king_position_score = (dist_to_center_rank + dist_to_center_file) * 10 # Se multiplica por 10 para dar más peso.

    # --- Bonificación por Estar en el Borde ---
    # Añade una bonificación adicional si el Rey Negro está en la primera fila (0), última fila (7),
    # primera columna (0) o última columna (7).
    if rank == 0 or rank == 7 or file == 0 or file == 7:
        king_position_score += 50 # Bonificación significativa por estar en el borde

    # --- Perspectiva de la Evaluación ---
    # La función de evaluación siempre devuelve un valor desde la perspectiva de Blancas.
    # Es decir, un valor positivo es bueno para Blancas, y un valor negativo es malo para Blancas.
    # El algoritmo Minimax se encarga de maximizar esta puntuación para el jugador maximizador (Blancas)
    # y minimizarla para el jugador minimizador (Negras).
    return king_position_score