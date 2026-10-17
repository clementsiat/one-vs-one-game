import pygame
from Item import Item


class Inventory:
    def __init__(self):
        self._items = []
        self._selected_item = 0
        self._inventory_size = 10

    def add(self, item):
        if item is not None and len(self._items) < self._inventory_size:
            self._items.append(item)
            return True
        return False

    def draw(self, screen : pygame.Surface):
        init_x, y, size, marge = 400, 650, 50, 5
        step = size + marge
        largeur = self._inventory_size * size + (self._inventory_size - 1) * marge
        pygame.draw.rect(screen, (0, 0, 0),
                         (init_x - marge, y - marge, largeur + 2 * marge, size + 2 * marge))

        for i in range(self._inventory_size):
            x = init_x + step * i
            couleur = (255, 215, 0) if i == self._selected_item else (255, 255, 255)
            pygame.draw.rect(screen, couleur, (x, y, size, size), border_radius=3)
            if i >= len(self._items):
                continue
            item = self._items[i]
            image = item.get_image() if hasattr(item, "get_image") else getattr(item, "_image", None)
            if image is None:
                continue
            image_diagonale = pygame.transform.rotate(image, -45)
            taille_max = size - 12
            largeur_img, hauteur_img = image_diagonale.get_size()
            facteur = min(taille_max / max(1, largeur_img), taille_max / max(1, hauteur_img))
            nouvelle_taille = (max(1, int(largeur_img * facteur)), max(1, int(hauteur_img * facteur)))
            image_finale = pygame.transform.smoothscale(image_diagonale, nouvelle_taille)
            screen.blit(image_finale, image_finale.get_rect(center=(x + size // 2, y + size // 2)))

    def remove(self, item):
        if item not in self._items:
            return
        index = self._items.index(item)
        self._items.remove(item)
        if len(self._items) == 0:
            self._selected_item = 0
        elif index < self._selected_item:
            self._selected_item -= 1
        elif self._selected_item >= len(self._items):
            self._selected_item = len(self._items) - 1

    def select(self, index):
        if isinstance(index, int) and 0 <= index and index < self._inventory_size:
            self._selected_item = index

    def select_item(self, item):
        """Aligne le sélecteur sur l'objet effectivement équipé."""
        if item in self._items:
            self._selected_item = self._items.index(item)

    def get_selected_item(self):
        if 0 <= self._selected_item < len(self._items):
            return self._items[self._selected_item]
        return None

    def get_items(self):
        return self._items


inv_dict = {
    pygame.K_1: 0,
    pygame.K_2: 1,
    pygame.K_3: 2,
    pygame.K_4: 3,
    pygame.K_5: 4,
    pygame.K_6: 5,
    pygame.K_7: 6,
    pygame.K_8: 7,
    pygame.K_9: 8,
    pygame.K_0: 9,
}
