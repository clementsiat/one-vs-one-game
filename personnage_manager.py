from random import randint, choice
from Personnage import Personnage
from config import name_list
import pygame
from Weapon import Sword
from Weapon import Spear

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
        P = Personnage(
            name=choice(name_list), 
            max_health=randint(50, 500), 
            max_energy=randint(100, 200), 
            damage=randint(5, 10), 
            defense=randint(1, 10), 
            dodge=randint(0, 50), 
            doubleAttaque=randint(0, 20), 
            player_pos = pygame.Vector2(0, 0),  
            weapon = Spear("Spear", 10, 120, 1, 100, None)
        )
        self._personnage_list.append(P)
        self.increment += 1
        return P

    def get_personnage_list(self):
        """
        get_personnage_list : Fonction qui retourne la liste des personnages
        -----
        Args:
            None
        -----
        Returns:
            
        """
        return self._personnage_list
    
pm : PersonnageManager = PersonnageManager.get_instance()


