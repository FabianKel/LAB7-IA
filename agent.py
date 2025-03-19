import math
import random

class Agent:
    def __init__(self, depth, player_id, alpha_beta=False):
        self.id = str(player_id)  
        self.opponent_id = '2' if self.id == '1' else '1'  
        self.alpha_beta = alpha_beta
        self.depth = depth if not alpha_beta else depth+1

    def evaluar_tablero(self, tablero):
        """Evalúa el tablero considerando agrupaciones y posición."""
        score = 0
        center_column = [fila[3] for fila in tablero]
        score += center_column.count(self.id) * 3
        score -= center_column.count(self.opponent_id) * 3

        for row in range(6):
            for col in range(7):
                if tablero[row][col] == self.id:
                    score += self.evaluar_posicion(tablero, row, col, self.id)
                elif tablero[row][col] == self.opponent_id:
                    score -= self.evaluar_posicion(tablero, row, col, self.opponent_id)

        return score

    def evaluar_posicion(self, tablero, row, col, player):
        """Evalúa posibles líneas de 4 desde una posición."""
        value = 0
        direcciones = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        for dx, dy in direcciones:
            count = 1
            vacios = 0
            for d in (1, -1):
                paso = 1
                while True:
                    x = col + dx * d * paso
                    y = row + dy * d * paso
                    if 0 <= x < 7 and 0 <= y < 6:
                        if tablero[y][x] == player:
                            count += 1
                        elif tablero[y][x] in ('0', 0):
                            vacios += 1
                            break
                        else:
                            break
                        paso += 1
                    else:
                        break
            if count >= 4:
                value += 1000  # Victoria
            elif count == 3 and vacios >= 1:
                value += 10
            elif count == 2 and vacios >= 2:
                value += 3
        return value

    def ordenar_movimientos(self, tablero, movimientos):
        """Ordena movimientos según su evaluación heurística."""
        return sorted(movimientos, key=lambda col: self.evaluar_tablero(self.simular_movimiento(tablero, col, self.id)), reverse=True)

    def minimax(self, tablero, profundidad, alpha, beta, maximizando):
        if profundidad == 0 or self.juego_terminado(tablero):
            return self.evaluar_tablero(tablero), None

        mejor_columna = None
        movimientos_validos = [c for c in range(7) if self.movimiento_valido(tablero, c)]
        if not movimientos_validos:
            return 0, None

        movimientos_ordenados = self.ordenar_movimientos(tablero, movimientos_validos)

        if maximizando:
            max_eval = -math.inf
            for columna in movimientos_ordenados:
                nuevo_tablero = self.simular_movimiento(tablero, columna, self.id)
                evaluacion, _ = self.minimax(nuevo_tablero, profundidad-1, alpha, beta, False)
                if evaluacion > max_eval:
                    max_eval = evaluacion
                    mejor_columna = columna
                if self.alpha_beta:
                    alpha = max(alpha, evaluacion)
                    if beta <= alpha:
                        break
            return max_eval, mejor_columna
        else:
            min_eval = math.inf
            for columna in movimientos_ordenados:
                nuevo_tablero = self.simular_movimiento(tablero, columna, self.opponent_id)
                evaluacion, _ = self.minimax(nuevo_tablero, profundidad-1, alpha, beta, True)
                if evaluacion < min_eval:
                    min_eval = evaluacion
                    mejor_columna = columna
                if self.alpha_beta:
                    beta = min(beta, evaluacion)
                    if beta <= alpha:
                        break
            return min_eval, mejor_columna

    def elegir_movimiento(self, tablero):
        _, movimiento = self.minimax(tablero, self.depth, -math.inf, math.inf, True)
        if movimiento is None:
            movimientos_validos = [c for c in range(7) if self.movimiento_valido(tablero, c)]
            return random.choice(movimientos_validos) if movimientos_validos else None
        
        return movimiento + 1  # Ajustar a la numeración del connect4.py

    def movimiento_valido(self, tablero, columna):
        return tablero[0][columna] in (0, '0')

    def simular_movimiento(self, tablero, columna, player_id):
        nuevo_tablero = [list(fila) for fila in tablero]
        for fila in range(5, -1, -1):
            if nuevo_tablero[fila][columna] in (0, '0'):
                nuevo_tablero[fila][columna] = player_id
                break
        return nuevo_tablero

    def juego_terminado(self, tablero):
        for row in range(6):
            for col in range(7):
                if tablero[row][col] not in (0, '0') and self.check_victoria(tablero, row, col):
                    return True
        return False

    def check_victoria(self, tablero, row, col):
        player = tablero[row][col]
        direcciones = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        for dx, dy in direcciones:
            count = 1
            for d in (1, -1):
                paso = 1
                while True:
                    x = col + dx * d * paso
                    y = row + dy * d * paso
                    if 0 <= x < 7 and 0 <= y < 6 and tablero[y][x] == player:
                        count += 1
                        paso += 1
                    else:
                        break
            if count >= 4:
                return True
        return False
