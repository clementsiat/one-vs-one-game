from random import randint
from Personnage import Personnage
from config import weapon_name_list
import pygame
from Weapon import Sword, Spear


sword = Sword(
    name="Basic Sword",
    damage=10,
    attack_range=7.0,
    attack_speed=1.2,
    durability=100,
    weapon_type="sword"
)

spear = Spear(
    name="Wooden Spear",
    damage=12,
    attack_range=3.5,
    attack_speed=2,
    durability=120,
    weapon_type="spear"
)

axe = Axe(
    name="Heavy Axe",
    damage=15,
    attack_range=1.8,
    attack_speed=3,
    durability=150,
    weapon_type="axe"
)

dagger = Dagger(
    name="Small dagger",
    damage=3,
    attack_range=0.5,
    attack_speed=0.3,
    durability=70,
    weapon_type="dagger"
)