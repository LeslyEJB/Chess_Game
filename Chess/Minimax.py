import chess # Importa la librería python-chess para la representación del tablero y movimientos
import math # Importa el módulo math para usar 'inf' (infinito)
from Heuristic import evaluate_board, CHECKMATE_SCORE # Importa la función de evaluación y la constante de puntuación de jaque mate

def minimax(board, depth, alpha, beta, maximizing_player):
    """
    Implementa el algoritmo Minimax con poda Alpha-Beta.

    Este algoritmo busca el mejor movimiento posible para el jugador actual
    asumiendo que ambos jugadores juegan de forma óptima.

    Args:
        board (chess.Board): El objeto del tablero de ajedrez en su estado actual.
        depth (int): La profundidad actual en el árbol de búsqueda.
                     Determina cuántos movimientos hacia adelante se simulan.
        alpha (float): El valor alpha para la poda Alpha-Beta.
                       Representa la mejor puntuación que el jugador maximizador
                       (Blancas) puede garantizar hasta el momento.
        beta (float): El valor beta para la poda Alpha-Beta.
                      Representa la mejor puntuación que el jugador minimizador
                      (Negras) puede garantizar hasta el momento.
        maximizing_player (bool): True si es el turno del jugador maximizador (Blancas),
                                  False si es el turno del jugador minimizador (Negras).

    Returns:
        tuple: Una tupla que contiene:
               - best_score (float): La mejor puntuación encontrada para la posición.
               - best_move (chess.Move): El mejor movimiento correspondiente a esa puntuación.
    """
    # --- Casos Base para la Recursión ---
    # La recursión se detiene si:
    # 1. Se alcanza la profundidad límite (depth == 0).
    # 2. El juego ha terminado (jaque mate, ahogado, etc.), lo cual se verifica con board.is_game_over().
    if depth == 0 or board.is_game_over():
        # En los casos base, se evalúa la posición final y se devuelve la puntuación
        # junto con None para el movimiento, ya que no hay más movimientos que hacer.
        return evaluate_board(board), None

    # --- Lógica para el Jugador Maximizador (Blancas) ---
    # Este jugador intenta obtener la puntuación más alta posible.
    if maximizing_player:
        max_eval = -math.inf # Inicializa la mejor evaluación con un valor muy bajo (infinito negativo)
        best_move = None # Inicializa el mejor movimiento como None

        # Itera sobre todos los movimientos legales disponibles desde la posición actual
        for move in board.legal_moves:
            board.push(move) # Realiza el movimiento en el tablero (simula el movimiento)
            
            # Llama recursivamente a minimax para el siguiente nivel del árbol de búsqueda.
            # El siguiente jugador será el minimizador (False).
            # Se pasan los valores alpha y beta actualizados.
            eval, _ = minimax(board, depth - 1, alpha, beta, False) 
            
            board.pop() # Deshace el movimiento para restaurar el tablero a su estado anterior (backtracking)

            # Si la evaluación de este movimiento es mejor que la mejor evaluación encontrada hasta ahora
            if eval > max_eval:
                max_eval = eval # Actualiza la mejor evaluación
                best_move = move # Actualiza el mejor movimiento
            
            # --- Poda Alpha-Beta (Alpha Cut-off) ---
            # Actualiza el valor alpha: es el máximo entre el alpha actual y la evaluación de este movimiento.
            alpha = max(alpha, eval)
            # Si el valor beta es menor o igual al valor alpha, significa que el jugador minimizador
            # ya tiene una opción mejor en una rama anterior y no explorará esta rama más a fondo.
            if beta <= alpha: 
                break # Poda la rama (corta la búsqueda)
        return max_eval, best_move # Devuelve la mejor evaluación y el mejor movimiento para el maximizador
    
    # --- Lógica para el Jugador Minimizador (Negras) ---
    # Este jugador intenta obtener la puntuación más baja posible (desde la perspectiva del maximizador).
    else:  
        min_eval = math.inf # Inicializa la mejor evaluación con un valor muy alto (infinito positivo)
        best_move = None # Inicializa el mejor movimiento como None

        # Itera sobre todos los movimientos legales disponibles
        for move in board.legal_moves:
            board.push(move) # Realiza el movimiento en el tablero (simula el movimiento)
            
            # Llama recursivamente a minimax para el siguiente nivel del árbol de búsqueda.
            # El siguiente jugador será el maximizador (True).
            # Se pasan los valores alpha y beta actualizados.
            eval, _ = minimax(board, depth - 1, alpha, beta, True) 
            
            board.pop() # Deshace el movimiento

            # Si la evaluación de este movimiento es peor que la mejor evaluación encontrada hasta ahora
            if eval < min_eval:
                min_eval = eval # Actualiza la mejor evaluación
                best_move = move # Actualiza el mejor movimiento
            
            # --- Poda Alpha-Beta (Beta Cut-off) ---
            # Actualiza el valor beta: es el mínimo entre el beta actual y la evaluación de este movimiento.
            beta = min(beta, eval)
            # Si el valor beta es menor o igual al valor alpha, significa que el jugador maximizador
            # ya tiene una opción mejor en una rama anterior y no explorará esta rama más a fondo.
            if beta <= alpha: 
                break # Poda la rama (corta la búsqueda)
        return min_eval, best_move # Devuelve la mejor evaluación y el mejor movimiento para el minimizador

def find_best_move(board, depth):
    """
    Función envoltorio para iniciar la búsqueda Minimax para el jugador Blanco (maximizador).

    Args:
        board (chess.Board): El objeto del tablero de ajedrez en su estado actual.
        depth (int): La profundidad máxima a la que el algoritmo debe buscar.

    Returns:
        chess.Move: El mejor movimiento que la IA (Blancas) debe realizar.
    """
    # Inicia la búsqueda Minimax con los valores iniciales de alpha (-inf) y beta (+inf).
    # Se indica que el jugador actual es el maximizador (True) porque es el turno de Blancas.
    score, move = minimax(board, depth, -math.inf, math.inf, True)
    return move # Devuelve solo el mejor movimiento