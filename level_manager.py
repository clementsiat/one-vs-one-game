import random
import personnage_manager
from config import WIDTH, HEIGHT
from weapon_manager import wm

class LevelManager:
    def __init__(self, niv):
        self._niv = niv
        self._pm = personnage_manager.PersonnageManager.get_instance()


    def nombre_enemies(self):
        nb_enemy = random.randint(self._niv +1, self._niv +2)
        return nb_enemy

    def get_level(self):
        return self._niv

    def next_level(self):
        self._niv += 1

    def is_level_finished(self, player_list, main_player):
        res = all(
            p.is_dead()
            for p in player_list
            if p != main_player
        )
        return res

level_manager = LevelManager(1)
        