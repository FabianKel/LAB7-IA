# LAB7-IA
# Aprendizaje por TD Learning en Connect Four

* [Enlace al repositorio](https://github.com/FabianKel/LAB7-IA)

* [Enlace al video de demostración](https://youtu.be/qCpKukzBzZQ)


## Integrantes del equipo
- [Mónica Salvatierra - 22249](https://github.com/alee2602)
- [Paula Barillas - 22764](https://github.com/paulabaal12)
- [Derek Arreaga - 22537](https://github.com/FabianKel) 

## Descripción del Proyecto
Este laboratorio implementa un agente basado en aprendizaje por diferencias temporales (TD Learning) para el juego Connect Four. Su desempeño se evalúa en comparación con un agente basado en Minimax y otro con poda Alpha-Beta.

## Requisitos
- Python 3.x
- Bibliotecas necesarias:
  - `numpy`
  - `matplotlib`
  - `tensorflow` (opcional, para utilizar una red neuronal en la función de valor)

## Implementación
### 1. Representación del Estado
El tablero se modela como una matriz 6x7 con los siguientes valores:
- `0`: Espacio vacío
- `1`: Fichas del jugador 1
- `-1`: Fichas del jugador 2

### 2. Espacio de Acción
Las acciones disponibles corresponden a las columnas donde el agente puede colocar una ficha.

### 3. Algoritmo de Aprendizaje TD
Se implementa **Q-learning**, con actualización de la función de valor según la ecuación:

``` 
\[ Q(s,a) \leftarrow Q(s,a) + \alpha [r + \gamma \max_{a'} Q(s',a') - Q(s,a)] \]
```

Opcionalmente, se puede emplear una red neuronal para aproximar la función de valor en lugar de una tabla de valores.

### 4. Definición de Recompensas
Las recompensas asignadas al agente se definen como:
- `+1`: Victoria del agente
- `-1`: Derrota del agente
- `+0.5`: Empate
- `+0.1`: Jugada que acerca al agente a la victoria
- `-0.1`: Jugada que acerca al oponente a la victoria

### 5. Estrategia de Exploración
Se utiliza la estrategia **ε-greedy**, en la cual ε disminuye gradualmente a medida que el agente aprende, reduciendo la exploración a favor de la explotación de las mejores jugadas conocidas.

### 6. Ciclo de Entrenamiento
El agente se entrena jugando contra sí mismo o contra oponentes con estrategias fijas. Durante cada episodio, actualiza sus valores de estado-acción en función de los resultados obtenidos.

### 7. Evaluación y Pruebas
Se realizaron **150 juegos** para evaluar el rendimiento del agente:
- **50 juegos** contra el agente Minimax
- **50 juegos** contra Minimax con poda Alpha-Beta
- **50 juegos** jugando contra sí mismo

Los resultados se representaron gráficamente para analizar la cantidad de victorias de cada agente.

## Video de Demostración
El video de demostración muestra 3 partidas aceleradas:
1. TD Learning vs. Minimax
2. TD Learning vs. Minimax con poda Alpha-Beta
3. TD Learning vs. sí mismo

### Contenido del Video
- Explicación general del agente TD Learning
- Análisis de las estrategias utilizadas en cada partida
- Discusión sobre los factores que influyeron en los resultados

## Resultados
Se adjunta un gráfico en formato PDF con el número de victorias obtenidas por cada agente en los 150 juegos de prueba.

## Autores
[Tu nombre o equipo]

