import numpy as np
import random
import math
import pickle
from collections import defaultdict
from agent import Agent

class TDAgent:
    def __init__(self, player_id, epsilon=1.0, alpha=0.005, gamma=0.9, load_file=None):
        self.id = str(player_id)
        self.opponent_id = '2' if self.id == '1' else '1'
        self.epsilon = epsilon  # Probabilidad de exploración
        self.alpha = alpha      # Tasa de aprendizaje
        self.gamma = gamma      # Factor de descuento
        self.q_values = defaultdict(lambda: np.zeros(7))  # Valores Q para cada par estado-acción
        
        if load_file:
            try:
                with open(load_file, 'rb') as f:
                    self.q_values = pickle.load(f)
            except FileNotFoundError:
                print(f"No se encontró el archivo {load_file}, iniciando con valores Q por defecto.")

    def estado_a_clave(self, tablero):
        """Convierte el estado del tablero en una clave para el diccionario de valores Q."""
        return tuple(tuple(row) for row in tablero)

    def movimiento_valido(self, tablero, columna):
        """Verifica si un movimiento es válido."""
        return tablero[0][columna] in (0, '0')

    def movimientos_validos(self, tablero):
        """Devuelve una lista de columnas disponibles."""
        return [col for col in range(7) if self.movimiento_valido(tablero, col)]

    def simular_movimiento(self, tablero, columna, player_id):
        """Simula un movimiento y devuelve el nuevo estado del tablero."""
        columna -= 1 
        nuevo_tablero = [list(fila) for fila in tablero]

        for fila in range(5, -1, -1):
            if nuevo_tablero[fila][columna] in (0, '0'):
                nuevo_tablero[fila][columna] = player_id
                break
        return nuevo_tablero

    def calcular_recompensa(self, tablero, accion, player_id):
        """Calcula la recompensa para un movimiento."""
        nuevo_tablero = self.simular_movimiento(tablero, accion, player_id)
        
        # Verifica victoria
        if self.check_victoria(nuevo_tablero, player_id):
            return 1.0
        
        # Verifica derrota (victoria del oponente en su próximo movimiento)
        for col in self.movimientos_validos(nuevo_tablero):
            tablero_oponente = self.simular_movimiento(nuevo_tablero, col, self.opponent_id)
            if self.check_victoria(tablero_oponente, self.opponent_id):
                return -1.0
        
        # Posición de amenaza (victoria en el próximo movimiento)
        for col in self.movimientos_validos(nuevo_tablero):
            tablero_amenaza = self.simular_movimiento(nuevo_tablero, col, player_id)
            if self.check_victoria(tablero_amenaza, player_id):
                return 0.5
        
        # Recompensa por control del centro
        centro = [fila[3] for fila in nuevo_tablero]
        recompensa_centro = 0.1 * centro.count(player_id) / 6
        
        return recompensa_centro

    def elegir_movimiento(self, tablero):
        """Elige una acción usando la política epsilon-greedy."""
        clave_estado = self.estado_a_clave(tablero)
        acciones_validas = self.movimientos_validos(tablero)
        
        if not acciones_validas:
            return None
        
        # Exploración
        if random.random() < self.epsilon:
            return random.choice(acciones_validas) + 1  
        
        # Explotación
        q_valores = self.q_values[clave_estado]
        # Filtrar solo acciones válidas
        valores_validos = [(accion, q_valores[accion]) for accion in acciones_validas]
        mejor_accion = max(valores_validos, key=lambda x: x[1])[0]
        
        return mejor_accion + 1  

    def actualizar_q(self, estado, accion, recompensa, nuevo_estado):
        """Actualiza los valores Q usando TD Learning."""
        clave_estado = self.estado_a_clave(estado)
        clave_nuevo_estado = self.estado_a_clave(nuevo_estado)
        
        # Obtener el valor Q máximo para el nuevo estado
        q_max_nuevo = max(self.q_values[clave_nuevo_estado]) if self.movimientos_validos(nuevo_estado) else 0
        
        # Actualizar el valor Q para el par estado-acción actual
        q_actual = self.q_values[clave_estado][accion]
        self.q_values[clave_estado][accion] = q_actual + self.alpha * (
            recompensa + self.gamma * q_max_nuevo - q_actual
        )

    def aprender(self, episodios=1000):
        minimax = Agent(depth=3, player_id=self.opponent_id, alpha_beta=False)

        for episodio in range(episodios):
            if episodio % 100 == 0:
                print(f"Episodio {episodio}/{episodios}")

            tablero = [[0 for _ in range(7)] for _ in range(6)]
            jugador_actual = self.id
            game_over = False

            while not game_over:
                acciones_validas = self.movimientos_validos(tablero)
                if not acciones_validas:
                    break  # empate

                if jugador_actual == self.id:
                    clave_estado = self.estado_a_clave(tablero)

                    if random.random() < self.epsilon:
                        accion = random.choice(acciones_validas)
                    else:
                        valores_q = [(a, self.q_values[clave_estado][a]) for a in acciones_validas]
                        accion = max(valores_q, key=lambda x: x[1])[0]

                    accion_jugada = accion + 1  # +1 porque usarás columna 1-7
                    nuevo_tablero = self.simular_movimiento(tablero, accion_jugada, self.id)

                    if self.check_victoria(nuevo_tablero, self.id):
                        recompensa = 1.0
                        self.actualizar_q(tablero, accion, recompensa, nuevo_tablero)
                        game_over = True
                        continue
                    elif not self.movimientos_validos(nuevo_tablero):
                        recompensa = 0.0
                        self.actualizar_q(tablero, accion, recompensa, nuevo_tablero)
                        game_over = True
                        continue

                    recompensa = self.calcular_recompensa(tablero, accion_jugada, self.id)
                    self.actualizar_q(tablero, accion, recompensa, nuevo_tablero)

                    tablero = nuevo_tablero
                    jugador_actual = self.opponent_id

                else:
                    accion_minimax = minimax.elegir_movimiento(tablero)
                    tablero = self.simular_movimiento(tablero, accion_minimax, self.opponent_id)

                    if self.check_victoria(tablero, self.opponent_id):
                        recompensa = -1.0
                        self.actualizar_q(tablero, accion_minimax - 1, recompensa, tablero)
                        game_over = True
                        continue

                    jugador_actual = self.id

            self.epsilon = max(0.2, self.epsilon * 0.995)

        print("Entrenamiento completado.")


    def guardar_modelo(self, filename):
        """Guarda el modelo de valores Q en un archivo."""
        with open(filename, 'wb') as f:
            pickle.dump(dict(self.q_values), f)
        print(f"Modelo guardado en {filename}")

    def cargar_modelo(self, filename):
        """Carga el modelo de valores Q desde un archivo."""
        try:
            with open(filename, 'rb') as f:
                self.q_values = defaultdict(lambda: np.zeros(7), pickle.load(f))
            print(f"Modelo cargado desde {filename}")
        except FileNotFoundError:
            print(f"No se encontró el archivo {filename}")

    def check_victoria(self, tablero, player_id):
        """Verifica si hay victoria para un jugador."""
        # Verificar horizontal
        for fila in range(6):
            for col in range(4):
                if all(tablero[fila][col+i] == player_id for i in range(4)):
                    return True
        
        # Verificar vertical
        for fila in range(3):
            for col in range(7):
                if all(tablero[fila+i][col] == player_id for i in range(4)):
                    return True
        
        # Verificar diagonal ascendente
        for fila in range(3, 6):
            for col in range(4):
                if all(tablero[fila-i][col+i] == player_id for i in range(4)):
                    return True
        
        # Verificar diagonal descendente
        for fila in range(3):
            for col in range(4):
                if all(tablero[fila+i][col+i] == player_id for i in range(4)):
                    return True
        
        return False