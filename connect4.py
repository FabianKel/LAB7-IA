import turtle
from agent import Agent
from player import Player


class Connect4:
    def __init__(self):
        self.tablero = turtle.Turtle()
        self.circulo = turtle.Turtle()
        self.espaciosY = [0] * 8
        self.player1Pos = set()
        self.player2Pos = set()
        self.coordenadasX = {i: -300 + (i - 1) * 100 for i in range(1, 8)}
        self.coordenadasY = {i: -300 + (i - 1) * 100 for i in range(1, 7)}
        self.player1 = None
        self.player2 = None
        self.jugador_actual = None  # Ahora almacena un objeto Player

    def crear_tablero(self):
        self.tablero.ht()
        self.tablero.width(10)
        self.tablero.speed(0)
        self.tablero.penup()
        self.tablero.goto(-350, 300)
        self.tablero.pendown()

        # Dibujar el contorno
        for _ in range(2):
            self.tablero.forward(700)
            self.tablero.right(90)
            self.tablero.forward(600)
            self.tablero.right(90)

        # Dibujar líneas verticales
        for i in range(6):
            self.tablero.penup()
            self.tablero.goto(-250 + i * 100, 300)
            self.tablero.pendown()
            self.tablero.goto(-250 + i * 100, -300)

        # Dibujar líneas horizontales
        for i in range(5):
            self.tablero.penup()
            self.tablero.goto(-350, 200 - i * 100)
            self.tablero.pendown()
            self.tablero.goto(350, 200 - i * 100)

        # Numerar columnas
        for i in range(7):
            self.tablero.penup()
            self.tablero.goto(-320 + i * 100, 320)
            self.tablero.write(str(i + 1), font=("Arial", 20))

    def colocar_ficha(self, columna):
        if self.espaciosY[columna] >= 6:
            print("Columna llena. Escoge otra.")
            return False

        fila = self.espaciosY[columna] + 1
        self.espaciosY[columna] += 1
        x, y = self.coordenadasX[columna], self.coordenadasY[fila]

        # Guardar posición
        if self.jugador_actual == self.player1:
            self.player1Pos.add((columna, fila))
        else:
            self.player2Pos.add((columna, fila))

        # Dibujar ficha con el color del jugador actual
        self.dibujar_ficha(x, y, self.jugador_actual.color)

        # Verificar si hay ganador
        if self.verificar_victoria(columna, fila, self.jugador_actual):
            print(f"¡Gana {self.jugador_actual.color}!")
            turtle.textinput("Mensaje", f"¡Gana {self.jugador_actual.color}!\nPresiona 'OK' para salir")
            return True

        # Cambiar turno
        self.jugador_actual = self.player2 if self.jugador_actual == self.player1 else self.player1
        return False

    def dibujar_ficha(self, x, y, color):
        self.circulo.color("black")
        self.circulo.width(5)
        self.circulo.speed(500)
        self.circulo.penup()
        self.circulo.goto(x, y)
        self.circulo.pendown()
        self.circulo.begin_fill()
        self.circulo.circle(50)
        self.circulo.color(color)
        self.circulo.end_fill()

    def verificar_victoria(self, col, fila, jugador):
        posiciones = self.player1Pos if jugador == self.player1 else self.player2Pos

        def check(dx, dy):
            count = 1
            for d in (-1, 1):
                for i in range(1, 4):
                    if (col + dx * i * d, fila + dy * i * d) in posiciones:
                        count += 1
                    else:
                        break
            return count >= 4

        return any(
            check(dx, dy) for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]
        )

    def play(self, player1=None, player2=None):
        """Función de juego que permite distintas configuraciones: IA vs IA, Humano vs IA, Humano vs Humano."""
        
        # Definir jugadores
        self.player1 = player1
        self.player2 = player2
        self.jugador_actual = self.player1

        self.crear_tablero()

        while True:
            try:
                if self.jugador_actual.agent:
                    # Si el jugador actual es un agente, elige movimiento automáticamente
                    print("jugador actual es ia")
                    print(self.get_estado_tablero())
                    columna = self.jugador_actual.agent.elegir_movimiento(self.get_estado_tablero())
                    print(columna)
                else:
                    # Si es un humano, pide entrada
                    columna = int(turtle.numinput(f"Turno {self.jugador_actual.color}", "Ingrese columna (1-7)", minval=1, maxval=7))
                    print("jugador actual es humano")
                if self.colocar_ficha(columna):
                    break
            except TypeError:
                print("Juego cancelado.")
                break

    def get_estado_tablero(self):
        """Devuelve el estado del tablero como una matriz de 6x7."""
        tablero = [[0 for _ in range(7)] for _ in range(6)]
        for (c, f) in self.player1Pos:
            tablero[6 - f][c - 1] = "1"  
        for (c, f) in self.player2Pos:
            tablero[6 - f][c - 1] = "2"  
        return tablero
