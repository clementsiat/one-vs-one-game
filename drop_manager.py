import pygame
from drops import Drops


class DropManager:

    def __init__(self):
        self._dropable = []

    def new_drops(self, drop: Drops):
        if drop is not None:
            self._dropable.append(drop)

    def draw_drops(self, screen):
        for drop in self._dropable:
            drop.draw(screen)

    def get_drops(self):
        return self._dropable

    def remove_drop(self, drop):
        if drop in self._dropable:
            self._dropable.remove(drop)


dm = DropManager()
