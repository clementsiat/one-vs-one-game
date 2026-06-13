import random
import personnage_manager
from config import WIDTH, HEIGHT
from weapon_manager import wm

class LevelManager:
    def __init__(self, niv):
        self._niv = niv
        self._pm = personnage_manager.PersonnageManager()


    def create_enemies(self):
        nb_enemy = random.randint(self._niv +1, self._niv +2)
        self._pm.generate_wave((WIDTH, HEIGHT), wm, nb_enemy)
        