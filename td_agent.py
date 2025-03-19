import numpy as np
import random
import math
import pickle
from collections import defaultdict

class TDAgent:
    def __init__(self, player_id, epsilon=0.1, alpha=0.1, gamma=0.9, load_file=None):
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
                return -0.5
        
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
            return random.choice(acciones_validas) + 1  # +1 para ajustar a numeración de connect4.py
        
        # Explotación
        q_valores = self.q_values[clave_estado]
        # Filtrar solo acciones válidas
        valores_validos = [(accion, q_valores[accion]) for accion in acciones_validas]
        mejor_accion = max(valores_validos, key=lambda x: x[1])[0]
        
        return mejor_accion + 1  # +1 para ajustar a numeración de connect4.py

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
        """Entrena al agente jugando contra sí mismo."""
        for episodio in range(episodios):
            if episodio % 100 == 0:
                print(f"Entrenando episodio {episodio}/{episodios}")
                
            # Inicializar tablero
            tablero = [[0 for _ in range(7)] for _ in range(6)]
            turno = 0
            jugador_actual = self.id
            
            while True:
                # Seleccionar acción con epsilon-greedy
                clave_estado = self.estado_a_clave(tablero)
                acciones_validas = self.movimientos_validos(tablero)
                
                if not acciones_validas:  # Empate
                    break
                
                if random.random() < self.epsilon:
                    accion = random.choice(acciones_validas)
                else:
                    valores_q = [(a, self.q_values[clave_estado][a]) for a in acciones_validas]
                    accion = max(valores_q, key=lambda x: x[1])[0]
                
                # Ejecutar acción
                nuevo_tablero = self.simular_movimiento(tablero, accion, jugador_actual)
                
                # Calcular recompensa
                recompensa = 0
                game_over = False
                
                if self.check_victoria(nuevo_tablero, jugador_actual):
                    recompensa = 1.0 if jugador_actual == self.id else -1.0
                    game_over = True
                elif not self.movimientos_validos(nuevo_tablero):  # Empate
                    recompensa = 0.1
                    game_over = True
                
                # Actualizar Q-values
                if jugador_actual == self.id:
                    self.actualizar_q(tablero, accion, recompensa, nuevo_tablero)
                
                # Verificar fin del juego
                if game_over:
                    break
                
                # Cambiar turno
                tablero = nuevo_tablero
                jugador_actual = self.opponent_id if jugador_actual == self.id else self.id
                turno += 1
            
            # Ajustar epsilon (disminuir exploración con el tiempo)
            self.epsilon = max(0.05, self.epsilon * 0.99)
        
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