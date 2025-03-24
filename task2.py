from connect4 import Connect4
from agent import Agent
from td_agent import TDAgent
from player import Player
import os

os.environ["DEMO_MODE"] = "1"
def elegir_modo():
    print("Selecciona el modo de juego:")
    print("1. Humano vs Humano")
    print("2. Humano vs IA")
    print("3. IA vs IA")
    
    while True:
        try:
            opcion = int(input("Ingrese su elección (1-3): "))
            if opcion in [1, 2, 3]:
                return opcion
            else:
                print("Por favor, elige una opción válida (1-3).")
        except ValueError:
            print("Entrada inválida. Ingresa un número del 1 al 3.")

def elegir_tipo_ia():
    print("Selecciona el tipo de IA:")
    print("1. Minimax")
    print("2. Minimax con Alpha-Beta")
    print("3. TD Learning")
    
    while True:
        try:
            opcion = int(input("Ingrese su elección (1-3): "))
            if opcion in [1, 2, 3]:
                return opcion
            else:
                print("Por favor, elige una opción válida (1-3).")
        except ValueError:
            print("Entrada inválida. Ingresa un número del 1 al 3.")

def elegir_alpha_beta(agente_numero):
    while True:
        opcion = input(f"¿Quieres activar Alpha-Beta Pruning para el agente {agente_numero}? (si/no): ").strip().lower()
        if opcion in ['si', 'no']:
            return opcion == 'si'
        print("Por favor, ingresa una opción valida.")

if __name__ == "__main__":
    modo = elegir_modo()

    if modo == 1:
        # Humano vs Humano
        player1 = Player("Red")
        player2 = Player("Purple")
    
    elif modo == 2:
        # Humano vs IA
        tipo_ia = elegir_tipo_ia()
        
        if tipo_ia == 1:  # Minimax
            depth = int(input("Ingrese la profundidad para la IA (ejemplo: 4): "))
            agent2 = Agent(depth=depth, alpha_beta=False, player_id=2)
        elif tipo_ia == 2:  # Alpha-Beta
            depth = int(input("Ingrese la profundidad para la IA (ejemplo: 4): "))
            agent2 = Agent(depth=depth, alpha_beta=True, player_id=2)
        else:  # TD Learning
            agent2 = TDAgent(player_id=2)
            cargar = input("¿Quieres cargar un modelo pre-entrenado? (si/no): ").strip().lower()
            if cargar == 'si':
                filename = input("Introduce el nombre del archivo del modelo: ")
                agent2.cargar_modelo(filename)
            else:
                episodios = int(input("Introduce el número de episodios para entrenar (ejemplo: 1000): "))
                agent2.aprender(episodios=episodios)
        
        player1 = Player("Red")
        player2 = Player("Purple", agent2)
    
    else:
        # IA vs IA
        print("Selecciona el tipo de IA para el jugador 1:")
        tipo_ia1 = elegir_tipo_ia()
        print("Selecciona el tipo de IA para el jugador 2:")
        tipo_ia2 = elegir_tipo_ia()
        
        # Crear agente 1
        if tipo_ia1 == 1:  # Minimax
            depth1 = int(input("Ingrese la profundidad para la IA 1 (ejemplo: 4): "))
            agent1 = Agent(depth=depth1, alpha_beta=False, player_id=1)
        elif tipo_ia1 == 2:  # Alpha-Beta
            depth1 = int(input("Ingrese la profundidad para la IA 1 (ejemplo: 4): "))
            agent1 = Agent(depth=depth1, alpha_beta=True, player_id=1)
        else:  # TD Learning
            agent1 = TDAgent(player_id=1)
            cargar = input("¿Quieres cargar un modelo pre-entrenado para la IA 1? (si/no): ").strip().lower()
            if cargar == 'si':
                filename = input("Introduce el nombre del archivo del modelo: ")
                agent1.cargar_modelo(filename)
            else:
                episodios = int(input("Introduce el número de episodios para entrenar (ejemplo: 1000): "))
                agent1.aprender(episodios=episodios)
        
        # Crear agente 2
        if tipo_ia2 == 1:  # Minimax
            depth2 = int(input("Ingrese la profundidad para la IA 2 (ejemplo: 4): "))
            agent2 = Agent(depth=depth2, alpha_beta=False, player_id=2)
        elif tipo_ia2 == 2:  # Alpha-Beta
            depth2 = int(input("Ingrese la profundidad para la IA 2 (ejemplo: 4): "))
            agent2 = Agent(depth=depth2, alpha_beta=True, player_id=2)
        else:  # TD Learning
            agent2 = TDAgent(player_id=2)
            cargar = input("¿Quieres cargar un modelo pre-entrenado para la IA 2? (si/no): ").strip().lower()
            if cargar == 'si':
                filename = input("Introduce el nombre del archivo del modelo (td_evaluation.py): ")
                agent2.cargar_modelo(filename)
            else:
                episodios = int(input("Introduce el número de episodios para entrenar (ejemplo: 1000): "))
                agent2.aprender(episodios=episodios)

        player1 = Player("Red", agent1)
        player2 = Player("Purple", agent2)
        
    game = Connect4()
    game.play(player1, player2)