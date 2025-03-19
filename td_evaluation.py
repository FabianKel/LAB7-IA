import matplotlib.pyplot as plt
import numpy as np
from connect4 import Connect4
from agent import Agent
from td_agent import TDAgent
from player import Player
import time

def jugar_partida(player1, player2, verbose=False):
    """Juega una partida entre dos jugadores y devuelve el resultado."""
    game = Connect4()
    game.player1 = player1
    game.player2 = player2
    game.jugador_actual = player1
    
    game.crear_tablero()
    
    # Jugar en modo silencioso (sin UI)
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
            
            # Verificar empate
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
    
    player_td = Player("Red", td_agent)
    player_minimax = Player("Blue", minimax_agent)
    player_alpha_beta = Player("Purple", alpha_beta_agent)
    
    print(f"Evaluando TD vs Minimax ({num_partidas} partidas)...")
    for i in range(num_partidas):
        if i % 10 == 0:
            print(f"Partida {i}/{num_partidas}")
        
        resultado = jugar_partida(player_td, player_minimax)
        if resultado == "player1":
            resultados["TD vs Minimax"]["td_win"] += 1
        elif resultado == "player2":
            resultados["TD vs Minimax"]["minimax_win"] += 1
        else:
            resultados["TD vs Minimax"]["empate"] += 1
    
    print(f"Evaluando TD vs Alpha-Beta ({num_partidas} partidas)...")
    for i in range(num_partidas):
        if i % 10 == 0:
            print(f"Partida {i}/{num_partidas}")
        
        resultado = jugar_partida(player_td, player_alpha_beta)
        if resultado == "player1":
            resultados["TD vs Alpha-Beta"]["td_win"] += 1
        elif resultado == "player2":
            resultados["TD vs Alpha-Beta"]["alpha_beta_win"] += 1
        else:
            resultados["TD vs Alpha-Beta"]["empate"] += 1
    
    print(f"Evaluando Minimax vs Alpha-Beta ({num_partidas} partidas)...")
    for i in range(num_partidas):
        if i % 10 == 0:
            print(f"Partida {i}/{num_partidas}")
        
        resultado = jugar_partida(player_minimax, player_alpha_beta)
        if resultado == "player1":
            resultados["Minimax vs Alpha-Beta"]["minimax_win"] += 1
        elif resultado == "player2":
            resultados["Minimax vs Alpha-Beta"]["alpha_beta_win"] += 1
        else:
            resultados["Minimax vs Alpha-Beta"]["empate"] += 1
    
    return resultados

def crear_graficas(resultados):
    """Crea gráficas de los resultados y las guarda en disco."""
    # Configuración de la gráfica
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
    # Configuración de los agentes
    depth_minimax = 3
    depth_alpha_beta = 3
    episodios_td = 5000
    num_partidas = 50
    
    # Crear agentes
    print("Creando agentes...")
    td_agent = entrenar_agente_td(jugador_id=1, episodios=episodios_td)
    minimax_agent = Agent(depth=depth_minimax, player_id=2, alpha_beta=False)
    alpha_beta_agent = Agent(depth=depth_alpha_beta, player_id=2, alpha_beta=True)
    
    # Evaluar agentes
    resultados = evaluar_agentes(
        td_agent=td_agent,
        minimax_agent=minimax_agent,
        alpha_beta_agent=alpha_beta_agent,
        num_partidas=num_partidas
    )
    
    # Mostrar resultados
    print("\nResultados:")
    print(f"TD vs Minimax: TD gana {resultados['TD vs Minimax']['td_win']}, Minimax gana {resultados['TD vs Minimax']['minimax_win']}, Empates {resultados['TD vs Minimax']['empate']}")
    print(f"TD vs Alpha-Beta: TD gana {resultados['TD vs Alpha-Beta']['td_win']}, Alpha-Beta gana {resultados['TD vs Alpha-Beta']['alpha_beta_win']}, Empates {resultados['TD vs Alpha-Beta']['empate']}")
    print(f"Minimax vs Alpha-Beta: Minimax gana {resultados['Minimax vs Alpha-Beta']['minimax_win']}, Alpha-Beta gana {resultados['Minimax vs Alpha-Beta']['alpha_beta_win']}, Empates {resultados['Minimax vs Alpha-Beta']['empate']}")
    
    # Crear gráficas
    crear_graficas(resultados)
    print("\nGráficas guardadas en 'resultados_connect4.png'")

if __name__ == "__main__":
    main()