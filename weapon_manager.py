from random import randint
from config import weapon_name_list
from Weapon import Sword, Spear, Dagger, Axe, AdminKnife
from image_manager import im

class WeaponManager:
    
    def __init__(self):
        """
        init : constructeur de weapon manager

        Args:
            image_list: dict : contient les images des armes
                {"sword": image_sword}
        """
        self.increment = 0
        self._weapon_list = []

    def init_images(self):
        self._image_list = im.get_weapon_image()


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
            damage=30,
            attack_range=50,
            attack_speed=1.2,
            durability=100,
            image= self._image_list.get("dagger")
        )
    def create_spear(self):
        return Spear(
            damage=12,
            attack_range=130,
            attack_speed=2,
            durability=120,
            image = self._image_list.get("spear"))

    

    def create_axe(self):
        return Axe(
            damage=20,
            attack_range=100,
            attack_speed=0.7,
            durability=200,
            image=self._image_list.get("axe")
        )
    def create_admin_knife(self):
        return AdminKnife(
            damage=1000,
            attack_range=150,
            attack_speed=0.3,
            durability=9999,
            image=self._image_list.get("admin_knife")
        )
wm = WeaponManager()