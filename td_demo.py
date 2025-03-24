from connect4 import Connect4
from agent import Agent
from td_agent import TDAgent
from player import Player
import time
import os

os.environ["DEMO_MODE"] = "1"

def jugar_demostracion(game, player1, player2, delay=0.5):
    """Juega una partida entre dos jugadores con visualización."""
    
    game.crear_tablero()
    
    game.play(player1,player2)

def main():
    # Cargar agente TD entrenado
    print("Cargando agente TD Learning...")
    td_agent = TDAgent(player_id=1)
    try:
        td_agent.cargar_modelo("td_model.pkl")
    except:
        print("No se encontró un modelo guardado. Entrenando nuevo modelo...")
        td_agent.aprender(episodios=1000)
        td_agent.guardar_modelo("td_model.pkl")
    
    # Crear agentes Minimax y Alpha-Beta
    minimax_agent = Agent(depth=3, player_id=2, alpha_beta=False)
    alpha_beta_agent = Agent(depth=3, player_id=2, alpha_beta=True)
    
    # Crear jugadores
    player_td = Player("Red", td_agent)
    player_minimax = Player("Blue", minimax_agent)
    player_alpha_beta = Player("Purple", alpha_beta_agent)
    
    # Jugar demostraciones
    print("\n--- Demostración 1: TD Learning vs Minimax ---")
    game1 = Connect4()
    jugar_demostracion(game1, player_td, player_minimax, delay=0.3)

    game2 = Connect4()
    print("\n--- Demostración 2: TD Learning vs Alpha-Beta ---")
    jugar_demostracion(game2, player_td, player_alpha_beta, delay=0.3)
    
    game3 = Connect4()
    print("\n--- Demostración 3: Minimax vs Alpha-Beta ---")
    jugar_demostracion(game3, player_minimax, player_alpha_beta, delay=0.3)

if __name__ == "__main__":
    main()