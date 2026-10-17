
class Item:
    def __init__(self, image):
        """
        __init__ : Fonction d'initialisation d'un Item
        """

        self._image = image

    def draw(self, screen, position: tuple):
        if self._image is None:
            return

        rect = self._image.get_rect(center=position)
        screen.blit(self._image, rect)