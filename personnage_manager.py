from random import randint
from Personnage import Personnage
from config import name_list
import pygame

class PersonnageManager():
    _instance = None
    def get_instance() -> 'PersonnageManager':
        if PersonnageManager._instance is None:
            PersonnageManager._instance  = PersonnageManager()
        return PersonnageManager._instance
    
    def __init__(self):
        self.increment = 0
        self._personnage_list = []

    def add_personnage(self):
        P = Personnage(name=name_list[self.increment], max_health=randint(100, 200), max_energy=randint(100, 200), damage=randint(10, 20), defense=randint(1, 10), dodge=randint(0, 50), doubleAttaque=randint(0, 20), player_pos = pygame.Vector2(0, 0))
        self._personnage_list.append(P)
        self.increment += 1
        return P

pm : PersonnageManager = PersonnageManager.get_instance()


