import matplotlib.pyplot as plt
import numpy as np
from connect4 import Connect4
from agent import Agent
from td_agent import TDAgent
from player import Player
import time

def jugar_partida(player1, player2, verbose=False):
    """Juega una partida entre dos jugadores y devuelve el resultado."""
    game = Connect4(usar_turtle= False)
    game.player1 = player1
    game.player2 = player2
    game.jugador_actual = player1
    
    #game.crear_tablero()
    
    while True:
        try:
            if verbose:
                print(f"Turno de {game.jugador_actual.color}")
            
            if game.jugador_actual.agent:
                columna = game.jugador_actual.agent.elegir_movimiento(game.get_estado_tablero())
                if verbose:
                    print(f"Columna elegida: {columna}")
            else:
                raise ValueError("Este script requiere jugadores con agentes.")
            
            resultado = game.colocar_ficha(columna)
            if resultado:
                return "player1" if game.jugador_actual == player1 else "player2"
            
            if all(game.espaciosY[i] >= 6 for i in range(1, 8)):
                if verbose:
                    print("¡Empate!")
                return "empate"
                
        except Exception as e:
            if verbose:
                print(f"Error: {e}")
            return "error"

def entrenar_agente_td(jugador_id=1, episodios=5000, guardar_en="td_model.pkl"):
    """Entrena un agente TD Learning y lo guarda en disco."""
    print(f"Entrenando agente TD Learning para el jugador {jugador_id}...")
    td_agent = TDAgent(player_id=jugador_id)
    td_agent.aprender(episodios=episodios)
    td_agent.guardar_modelo(guardar_en)
    return td_agent

def evaluar_agentes(td_agent, minimax_agent, alpha_beta_agent, num_partidas=50):
    """Evalúa el rendimiento de TD Learning contra Minimax y Alpha-Beta."""
    resultados = {
        "TD vs Minimax": {"td_win": 0, "minimax_win": 0, "empate": 0},
        "TD vs Alpha-Beta": {"td_win": 0, "alpha_beta_win": 0, "empate": 0},
        "Minimax vs Alpha-Beta": {"minimax_win": 0, "alpha_beta_win": 0, "empate": 0}
    }
    
    player_td = Player("Red", td_agent, nombre_agente="TD Learning")
    player_minimax = Player("Blue", minimax_agent, nombre_agente="Minimax")
    player_alpha_beta = Player("Purple", alpha_beta_agent, nombre_agente="MinimaxAB")
    
    print(f"Evaluando TD vs Minimax ({num_partidas} partidas)...")
    resultados = jugar_y_registrar_partidas(player_td, player_minimax, num_partidas, resultados, "TD vs Minimax", "td_win", "minimax_win")
    
    print(f"Evaluando TD vs Alpha-Beta ({num_partidas} partidas)...")
    resultados = jugar_y_registrar_partidas(player_td, player_alpha_beta, num_partidas, resultados, "TD vs Alpha-Beta", "td_win", "alpha_beta_win")
    
    print(f"Evaluando Minimax vs Alpha-Beta ({num_partidas} partidas)...")
    resultados = jugar_y_registrar_partidas(player_minimax, player_alpha_beta, num_partidas, resultados, "Minimax vs Alpha-Beta", "minimax_win", "alpha_beta_win")
    
    return resultados

def jugar_y_registrar_partidas(player1, player2, num_partidas, resultados, key, win_key1, win_key2):
    """Juega y registra los resultados de las partidas."""
    for i in range(num_partidas):
        if i % 10 == 0:
            print(f"Partida {i}/{num_partidas}")
        
        resultado = jugar_partida(player1, player2)
        if resultado == "player1":
            resultados[key][win_key1] += 1
        elif resultado == "player2":
            resultados[key][win_key2] += 1
        else:
            resultados[key]["empate"] += 1
    return resultados

def crear_graficas(resultados):
    """Crea gráficas de los resultados y las guarda en disco."""
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
    
    # Resultados TD vs Minimax
    labels = ['TD Wins', 'Minimax Wins', 'Empates']
    values = [resultados["TD vs Minimax"]["td_win"], 
            resultados["TD vs Minimax"]["minimax_win"], 
            resultados["TD vs Minimax"]["empate"]]
    ax1.bar(labels, values, color=['red', 'blue', 'gray'])
    ax1.set_title('TD Learning vs Minimax')
    ax1.set_ylabel('Número de partidas')
    
    # Resultados TD vs Alpha-Beta
    labels = ['TD Wins', 'Alpha-Beta Wins', 'Empates']
    values = [resultados["TD vs Alpha-Beta"]["td_win"], 
            resultados["TD vs Alpha-Beta"]["alpha_beta_win"], 
            resultados["TD vs Alpha-Beta"]["empate"]]
    ax2.bar(labels, values, color=['red', 'purple', 'gray'])
    ax2.set_title('TD Learning vs Alpha-Beta')
    
    # Resultados Minimax vs Alpha-Beta
    labels = ['Minimax Wins', 'Alpha-Beta Wins', 'Empates']
    values = [resultados["Minimax vs Alpha-Beta"]["minimax_win"], 
            resultados["Minimax vs Alpha-Beta"]["alpha_beta_win"], 
            resultados["Minimax vs Alpha-Beta"]["empate"]]
    ax3.bar(labels, values, color=['blue', 'purple', 'gray'])
    ax3.set_title('Minimax vs Alpha-Beta')
    
    plt.tight_layout()
    plt.savefig('resultados_connect4.png')
    plt.close()

def main():
    """Función principal para configurar y evaluar los agentes."""
    depth_minimax = 3
    depth_alpha_beta = 3
    episodios_td = 800
    num_partidas = 50 
    
    print("Creando agentes...")
    td_agent = entrenar_agente_td(jugador_id=1, episodios=episodios_td)
    minimax_agent = Agent(depth=depth_minimax, player_id=2, alpha_beta=False)
    alpha_beta_agent = Agent(depth=depth_alpha_beta, player_id=2, alpha_beta=True)
    
    resultados = evaluar_agentes(
        td_agent=td_agent,
        minimax_agent=minimax_agent,
        alpha_beta_agent=alpha_beta_agent,
        num_partidas=num_partidas
    )
    
    print("\nResultados:")
    print(f"TD vs Minimax: TD gana {resultados['TD vs Minimax']['td_win']}, Minimax gana {resultados['TD vs Minimax']['minimax_win']}, Empates {resultados['TD vs Minimax']['empate']}")
    print(f"TD vs Alpha-Beta: TD gana {resultados['TD vs Alpha-Beta']['td_win']}, Alpha-Beta gana {resultados['TD vs Alpha-Beta']['alpha_beta_win']}, Empates {resultados['TD vs Alpha-Beta']['empate']}")
    print(f"Minimax vs Alpha-Beta: Minimax gana {resultados['Minimax vs Alpha-Beta']['minimax_win']}, Alpha-Beta gana {resultados['Minimax vs Alpha-Beta']['alpha_beta_win']}, Empates {resultados['Minimax vs Alpha-Beta']['empate']}")
    
    crear_graficas(resultados)
    print("\nGráficas guardadas en 'resultados_connect4.png'")

if __name__ == "__main__":
    main()