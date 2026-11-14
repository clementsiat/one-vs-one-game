import pygame

class Item:
    def __init__(self, image, stackable, max_stack = 1, current_stack = 1):
        """
        __init__ : Fonction d'initialisation d'un Item
        """

        self._image = image
        self._stackable = stackable
        self._max_stack = max_stack
        self._current_stack = current_stack

    def draw(self, screen, position: tuple):
        if self._image is None:
            return

        rect = self._image.get_rect(center=position)
        screen.blit(self._image, rect)
        if self.is_stackable():
            my_font = pygame.font.SysFont('Comic Sans MS', 10)
            text_surface = my_font.render(
                self._current_stack,
                True,
                (0, 0, 0)
            )
            screen.blit(
                text_surface,
                position
            )

    def stack(self):
        if self._stackable == False:
            return

    def is_stackable(self):
        return self._stackable
        