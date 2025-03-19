from connect4 import Connect4
from agent import Agent
from td_agent import TDAgent
from player import Player
import time

def jugar_demostracion(player1, player2, delay=0.5):
    """Juega una partida entre dos jugadores con visualización."""
    game = Connect4()
    game.player1 = player1
    game.player2 = player2
    game.jugador_actual = player1
    
    game.crear_tablero()
    
    while True:
        try:
            print(f"Turno de {game.jugador_actual.color}")
            
            if game.jugador_actual.agent:
                columna = game.jugador_actual.agent.elegir_movimiento(game.get_estado_tablero())
                print(f"Columna elegida: {columna}")
            else:
                raise ValueError("Este script requiere jugadores con agentes.")
            
            # Pequeña pausa para ver el juego
            time.sleep(delay)
            
            resultado = game.colocar_ficha(columna)
            if resultado:
                print(f"¡Gana {game.jugador_actual.color}!")
                return game.jugador_actual.color
            
            # Verificar empate
            if all(game.espaciosY[i] >= 6 for i in range(1, 8)):
                print("¡Empate!")
                return "empate"
                
        except Exception as e:
            print(f"Error: {e}")
            return "error"

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
    jugar_demostracion(player_td, player_minimax, delay=0.3)
    
    print("\n--- Demostración 2: TD Learning vs Alpha-Beta ---")
    jugar_demostracion(player_td, player_alpha_beta, delay=0.3)
    
    print("\n--- Demostración 3: Minimax vs Alpha-Beta ---")
    jugar_demostracion(player_minimax, player_alpha_beta, delay=0.3)

if __name__ == "__main__":
    main()