import pygame
from Item import Item


class Drops:
    """Un objet posé au sol, représenté par son image et sa position."""

    def __init__(self, objet: Item, position, pos_y=None):
        self._objet = objet
        if pos_y is None:
            self._position = pygame.Vector2(position)
        else:
            self._position = pygame.Vector2(position, pos_y)

    def get_item(self):
        return self._objet

    def get_position(self):
        return self._position

    def draw(self, screen):
        image = self._objet.get_image() if hasattr(self._objet, "get_image") else getattr(self._objet, "_image", None)
        if image is None:
            return
        # Taille maximale 36x36 en conservant les proportions de l'image.
        largeur, hauteur = image.get_size()
        if largeur <= 0 or hauteur <= 0:
            return
        facteur = min(36 / largeur, 36 / hauteur)
        taille = (max(1, int(largeur * facteur)), max(1, int(hauteur * facteur)))
        image_sol = pygame.transform.smoothscale(image, taille)
        rect = image_sol.get_rect(center=(round(self._position.x), round(self._position.y)))
        # Petit contour pour mieux distinguer l'objet du décor.
        pygame.draw.rect(screen, (255, 215, 0), rect.inflate(6, 6), 1, border_radius=4)
        screen.blit(image_sol, rect)

    def is_near(self, position, distance=42):
        return self._position.distance_to(pygame.Vector2(position)) <= distance
