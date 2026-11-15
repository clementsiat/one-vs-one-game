import math, random
import pygame
from config import weapon_name_list
from enum import Enum
from Item import Item

class Mutation(Enum):
    BRONZE = 0.8
    SILVER = 1.2
    GOLD = 2
    DIAMANT = 5
    PLATINE = 7
    GOD = 10

MUTATION_COLORS = {
    Mutation.BRONZE: (205, 127, 50),
    Mutation.SILVER: (192, 192, 192),
    Mutation.GOLD: (255, 215, 0),
    Mutation.DIAMANT: (0, 220, 255),
    Mutation.PLATINE: (180, 100, 255),
    Mutation.GOD: (255, 40, 180)
}


class Weapon(Item):
    def __init__(self, damage, attack_range, attack_speed, durability, weapon_type, image):
        """
        Weapon : classe représentant une arme

        Args:
            name (str) : nom de l'arme
            damage (int) : dégâts
            attack_range (float) : portée de l'attaque
            attack_speed (float) : vitesse d'attaque
            durability (int) : durabilité de l'arme
            weapon_type (str) : type d'arme (ex: "sword", "spear", "axe")
        """

        super().__init__(image, stackable = False)
        self._base_image = image.copy() if image is not None else None
        self._name = random.choice(weapon_name_list)
        self._damage = damage
        self._attack_range = attack_range
        self._attack_speed = attack_speed
        self._durability = durability
        self._weapon_type = weapon_type
        self._mutation = Mutation.BRONZE


    def mutate(self):

        nombre = random.randint(1, 100)

        if nombre <= 40:
            self._mutation = Mutation.BRONZE
        elif nombre <= 70:
            self._mutation = Mutation.SILVER
        elif nombre <= 85:
            self._mutation = Mutation.GOLD
        elif nombre <= 90:
            self._mutation = Mutation.DIAMANT
        elif nombre <= 99:
            self._mutation = Mutation.PLATINE
        else:
            self._mutation = Mutation.GOD

        multiplicateur = self._mutation.value

        self._damage *= multiplicateur
        self._durability *= multiplicateur

        # Changer la couleur de l'image
        if self._base_image is not None:
            self._image = self._base_image.copy()
            couleur = MUTATION_COLORS[self._mutation]

            largeur, hauteur = self._image.get_size()

            for x in range(largeur):
                for y in range(hauteur):
                    pixel = self._base_image.get_at((x, y))

                    if pixel.a > 0:
                        luminosite = (pixel.r + pixel.g + pixel.b) / 3
                        facteur = 0.4 + 0.6 * luminosite / 255

                        self._image.set_at((x, y), (
                            int(couleur[0] * facteur),
                            int(couleur[1] * facteur),
                            int(couleur[2] * facteur),
                            pixel.a
                        ))

        print(f"Nouvelle rareté : {self._mutation.name}")
    
    def is_colliding(self, start_pos, direction, personnages, owner):
        raise NotImplementedError("Your is_colliding method is not written")      

     


   
    ###########
    # GETTERS #
    ###########

    def get_mutation(self):
        return self._mutation

    def get_end_pos(self, init_pos, direction):
        if direction.length() == 0:
            return init_pos
        direction = direction.normalize()
        end_pos = init_pos + direction * self._attack_range
        return end_pos
    
    def get_name(self):
        return self._name

    def get_damage(self):
        return self._damage

    def get_attack_range(self):
        return self._attack_range

    def get_attack_speed(self):
        return self._attack_speed

    def get_durability(self):
        return self._durability

    def get_weapon_type(self):
        return self._weapon_type
    
    def get_image(self) -> pygame.Surface: 
        return self._image

class Sword(Weapon):

    def __init__(self, damage, attack_range, attack_speed, durability, image):
        super().__init__(
            damage,
            attack_range,
            attack_speed,
            durability,
            "sword",
            image
        )
        

    def is_colliding(self, start_pos, direction, personnages, owner):
        

        touched = []

        # sécurité
        if direction.length() == 0:
            return touched

        # normalisation
        direction = direction.normalize()

        # position finale de l'épée
        end_pos = self.get_end_pos(start_pos, direction)

        # coordonnées du segment
        x1 = start_pos.x
        y1 = start_pos.y

        x2 = end_pos.x
        y2 = end_pos.y

        # vecteur du segment
        dx = x2 - x1
        dy = y2 - y1

        # test sur tous les personnages
        for enemy in personnages:

            # ignore soi-même et morts
            if enemy == owner or enemy.is_dead():
                continue

            # centre du cercle ennemi
            cx = enemy.get_player_pos().x
            cy = enemy.get_player_pos().y

            # rayon du joueur
            radius = enemy.get_taille()

            # cas segment = point
            if dx == 0 and dy == 0:
                distance = math.hypot(cx - x1, cy - y1)

            else:
                # projection sur le segment
                t = ((cx - x1) * dx + (cy - y1) * dy) / (dx * dx + dy * dy)

                # clamp entre 0 et 1
                t = max(0, min(1, t))

                # point le plus proche
                closest_x = x1 + t * dx
                closest_y = y1 + t * dy

                # distance finale
                distance = math.hypot(cx - closest_x, cy - closest_y)

            # collision
            if distance <= radius:
                touched.append(enemy)

        return touched





class Spear(Weapon):

    def __init__(self, damage, attack_range, attack_speed, durability, image):
        super().__init__(damage, attack_range, attack_speed, durability, "spear", image)


    def is_colliding(self, start_pos, direction, personnages, owner):
        touched = []

        if direction.length() == 0:
            return touched

        direction = direction.normalize()
        end_pos = self.get_end_pos(start_pos, direction)

        for p in personnages:
            if p == owner or p.is_dead():
                continue

            distance = (p.get_player_pos() - end_pos).length()

            # zone précise (lance)
            if distance < p.get_taille():
                touched.append(p)

        return touched
    
class Dagger(Weapon):

    def __init__(self, damage, attack_range, attack_speed, durability, image):
        super().__init__(
            damage,
            attack_range,
            attack_speed,
            durability,
            "dagger",
            image
        )
        

    def is_colliding(self, start_pos, direction, personnages, owner):
    

        touched = []

        # sécurité
        if direction.length() == 0:
            return touched

        # normalisation
        direction = direction.normalize()

        # position finale de l'épée
        end_pos = self.get_end_pos(start_pos, direction)

        # coordonnées du segment
        x1 = start_pos.x
        y1 = start_pos.y

        x2 = end_pos.x
        y2 = end_pos.y

        # vecteur du segment
        dx = x2 - x1
        dy = y2 - y1

        # test sur tous les personnages
        for enemy in personnages:

            # ignore soi-même et morts
            if enemy == owner or enemy.is_dead():
                continue

            # centre du cercle ennemi
            cx = enemy.get_player_pos().x
            cy = enemy.get_player_pos().y

            # rayon du joueur
            radius = enemy.get_taille()

            # cas segment = point
            if dx == 0 and dy == 0:
                distance = math.hypot(cx - x1, cy - y1)

            else:
                # projection sur le segment
                t = ((cx - x1) * dx + (cy - y1) * dy) / (dx * dx + dy * dy)

                # clamp entre 0 et 1
                t = max(0, min(1, t))

                # point le plus proche
                closest_x = x1 + t * dx
                closest_y = y1 + t * dy

                # distance finale
                distance = math.hypot(cx - closest_x, cy - closest_y)

            # collision
            if distance <= radius:
                touched.append(enemy)

        return touched

class Axe(Weapon):

    def __init__(self, damage, attack_range, attack_speed, durability, image):
        super().__init__(
            damage,
            attack_range,
            attack_speed,
            durability,
            "axe",
            image
        )

    def is_colliding(self, start_pos, direction, personnages, owner):

        touched = []

        if direction.length() == 0:
            return touched

        direction = direction.normalize()

        # centre de la tête de hache
        axe_center = start_pos + direction * (self.get_attack_range() * 0.7)

        axe_radius = 50
        if owner.get_taille() >= 40:
            axe_radius = 75
        for enemy in personnages:

            if enemy == owner or enemy.is_dead():
                continue

            distance = (
                enemy.get_player_pos() - axe_center
            ).length()

            if distance <= axe_radius + enemy.get_taille():
                touched.append(enemy)

        return touched

class AdminKnife(Weapon):

    def __init__(self, damage, attack_range, attack_speed, durability, image):
        super().__init__(
            damage,
            attack_range,
            attack_speed,
            durability,
            "admin_knife",
            image
        )

    def is_colliding(self, start_pos, direction, personnages, owner):
        touched = []

        if direction.length() == 0:
            return touched

        direction = direction.normalize()
        end_pos = self.get_end_pos(start_pos, direction)

        for enemy in personnages:
            if enemy == owner or enemy.is_dead():
                continue

            distance = (enemy.get_player_pos() - end_pos).length()

            if distance <= enemy.get_taille():
                touched.append(enemy)

        return touched