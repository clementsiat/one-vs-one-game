import pygame

class Inventory:

    def __init__(self):
        self._items = []
        self._selected_item = 0
        self._inventory_size = 10

    def add(self, item):
        self._items.append(item)

    def draw(self, screen):
        init_x = 400
        y = 650
        size = 50
        marge = 5
        pygame.draw.rect(screen, (0, 0, 0), 
                         (init_x - marge, 
                          y - marge, 
                          size * self._inventory_size + (2 + self._inventory_size - 1) * marge, 
                          size + 2 * marge)
                          )
        for i in range(self._inventory_size):
            x = init_x + 50*i
            pygame.draw.rect(screen, (255, 255, 255), (x + marge*i, y, size, size))
            


    def remove(self, item):
        if item in self._items:
            self._items.remove(item)

            if len(self._items) == 0:
                self._selected_item = 0
            elif self._selected_item >= len(self._items):
                self._selected_item = len(self._items)

    def select(self, index):
        if 0 <= index < len(self._items):
            self._selected_item = index

    def get_selected_item(self):
        if len(self._items) == 0:
            return None
        print(self._selected_item)
        print(self._items[self._selected_item])
        return self._items[self._selected_item]
        

    def get_items(self):
        return self._items


inv_dict = {
    pygame.K_AMPERSAND: 0,
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