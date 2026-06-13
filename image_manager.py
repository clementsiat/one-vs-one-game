import pygame
from config import WIDTH, HEIGHT

class ImageManager:

    def __init__(self):
        self.weapon_image_list = {}
        self.weapon_rect_list = {}
        self.environnement_image_list = {}

    def load_images(self):
        # ---------- CHARGEMENT DES IMAGES ----------
        starting_screen = pygame.image.load("Images/starting_screen.png").convert()
        starting_screen = pygame.transform.scale(starting_screen, (WIDTH, HEIGHT))

        background = pygame.image.load("Images/background_one_vs_one.png").convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))

        sword_img = pygame.image.load("Images/sword.png").convert_alpha()
        sword_img = pygame.transform.scale(sword_img, (40, 70))
        dagger_img = pygame.image.load("Images/dagger.png").convert_alpha()
        dagger_img = pygame.transform.scale(dagger_img, (24, 75))
        spear_img = pygame.image.load("Images/spear.png").convert_alpha()
        spear_img = pygame.transform.scale(spear_img, (25, 130))
        axe_img = pygame.image.load("Images/axe.png").convert_alpha()
        axe_img = pygame.transform.scale(axe_img, (37, 100))
        self.environnement_image_list = {
            "background": background,
            "starting_screen": starting_screen
        }
        self.weapon_image_list = {
            "spear": spear_img,
            "dagger": dagger_img,
            "sword": sword_img,
            "axe": axe_img
        }
        self.weapon_rect_list = {
            "sword_rect": sword_img.get_rect(center=(150, 150)),
            "dagger_rect": dagger_img.get_rect(center=(WIDTH - 150, 150)),
            "spear_rect": spear_img.get_rect(center=(150, HEIGHT - 150)),
            "axe_rect": axe_img.get_rect(center=(WIDTH - 150, HEIGHT - 150))
        }

    def get_weapon_image(self): return self.weapon_image_list
    def get_rect(self): return self.weapon_rect_list
    def get_environnement(self): return self.environnement_image_list

im = ImageManager()