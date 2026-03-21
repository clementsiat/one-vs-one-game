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
    
