import math

class Weapon:
    def __init__(self, name, damage, attack_range, attack_speed, durability, weapon_type, weapon_pos):
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

        self._name = name
        self._damage = damage
        self._attack_range = attack_range
        self._attack_speed = attack_speed
        self._durability = durability
        self._weapon_type = weapon_type
        self._weapon_pos = weapon_pos
        


   
    ###########
    # GETTERS #
    ###########
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
    

class Sword(Weapon):

    def __init__(self, name, damage, attack_range, attack_speed, durability, weapon_pos):
        super().__init__(
            name,
            damage,
            attack_range,
            attack_speed,
            durability,
            "sword",
            weapon_pos
        )
        print("A new sword has been forged")

    def is_colliding(self, start_pos, direction, personnages, owner):
        print("USING SWORD COLLISION")

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

    def __init__(self, name, damage, attack_range, attack_speed, durability, weapon_pos):
        super().__init__(name, damage, attack_range, attack_speed, durability, "spear", weapon_pos)
        print("A new spear has been forged")

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