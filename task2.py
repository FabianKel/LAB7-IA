from connect4 import Connect4
from agent import Agent
from player import Player

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
        alpha_beta = elegir_alpha_beta(2)
        depth = int(input("Ingrese la profundidad para la IA (ejemplo: 4): "))
        agent2 = Agent(depth=depth, alpha_beta=alpha_beta, player_id=2)
        player1 = Player("Red")
        player2 = Player("Purple", agent2)
    
    else:
        # IA vs IA
        alpha_beta1 = elegir_alpha_beta(1)
        depth1 = int(input("Ingrese la profundidad para la IA 1 (ejemplo: 4): "))
        alpha_beta2 = elegir_alpha_beta(2)
        depth2 = int(input("Ingrese la profundidad para la IA 2 (ejemplo: 4): "))

        agent1 = Agent(depth=depth1, alpha_beta=alpha_beta1, player_id=1)
        agent2 = Agent(depth=depth2, alpha_beta=alpha_beta2, player_id=2)

        player1 = Player("Red", agent1)
        player2 = Player("Purple", agent2)
        
    game = Connect4()
    game.play(player1, player2)
