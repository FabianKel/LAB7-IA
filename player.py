import random
import math
from agent import Agent

class Player:
    def __init__(self, color, agent = None):
        self.color = color  # "Red", "Yellow", etc
        self.agent = agent
    
