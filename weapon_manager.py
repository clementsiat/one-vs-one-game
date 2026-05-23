from random import randint
from Personnage import Personnage
from config import weapon_name_list
import pygame
from Weapon import Sword, Spear, Dagger

class WeaponManager:
    
    def __init__(self, image_list):
        """
        init : constructeur de weapon manager

        Args:
            image_list: dict : contient les images des armes
                {"sword": image_sword}
        """
        self.increment = 0
        self._image_list = image_list # dict{"dagger": any, "sword": any, "spear": any}
        self._weapon_list = []


    def create_sword(self):
        """
        """
        return Sword(
            damage=10,
            attack_range=100,
            attack_speed=1.2,
            durability=100,
            image= self._image_list.get("sword")
        )

    def create_dagger(self):
        """
        """
        return Dagger(
            damage=10,
            attack_range=50,
            attack_speed=1.2,
            durability=100,
            image= self._image_list.get("dagger")
        )

# spear = Spear(
#     damage=12,
#     attack_range=3.5,
#     attack_speed=2,
#     durability=120,
#     weapon_type="spear"
# )

# axe = Axe(
#     damage=15,
#     attack_range=1.8,
#     attack_speed=3,
#     durability=150,
#     weapon_type="axe"
# )
