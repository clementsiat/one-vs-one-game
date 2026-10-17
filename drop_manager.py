import pygame
from drops import Drops


class DropManager:
    """Centralise les drops au sol, leur affichage et leur ramassage."""

    def __init__(self):
        self._dropable = []
        self._dead_seen = set()

    def new_drops(self, drop: Drops):
        if drop is not None:
            self._dropable.append(drop)

    def draw_drops(self, screen):
        for drop in self._dropable:
            drop.draw(screen)

    def update_dead_personnages(self, personnages, excluded=None):
        """Crée un seul drop par personnage mort."""
        for personnage in personnages:
            identifiant = id(personnage)
            if personnage is excluded:
                continue
            if personnage.is_dead() and identifiant not in self._dead_seen:
                self._dead_seen.add(identifiant)
                # Le joueur principal ne doit pas lâcher son arme à sa mort.
                if hasattr(personnage, "get_player_weapon"):
                    arme = personnage.get_player_weapon()
                    if arme is not None:
                        self.new_drops(Drops(arme, personnage.get_player_pos()))

    def try_pickup(self, personnage, max_distance=48):
        """Ramasse le drop le plus proche si le personnage est assez près."""
        inventaire = personnage.get_inventory()
        objets = inventaire.get_items()
        limite = getattr(inventaire, "_inventory_size", 10)
        if len(objets) >= limite:
            return False

        position = personnage.get_player_pos()
        for index, drop in enumerate(self._dropable):
            if drop.is_near(position, max_distance):
                inventaire.add(drop.get_item())
                del self._dropable[index]
                return True
        return False

    def get_drops(self):
        return list(self._dropable)


dm = DropManager()
