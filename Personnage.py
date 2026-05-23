from random import choice, randint
from time import sleep
import pygame, math
from enum import Enum
from Weapon import Sword, Spear, Weapon


class Action(Enum):
    IDLE = {"action": "idle", "duration": 0, "couleur": "black"}
    ATTAQUE = {"action": "attack", "duration": 4, "couleur": "red"}
    DEFENSE = {"action": "defense", "duration": 6, "couleur": "blue"}
    INVULNERABLE = {"action": "invulnerable", "duration": 0.7, "couleur": "white"}

class Personnage:


    def __init__(self, name, max_health, max_energy, damage, defense, dodge, doubleAttaque, player_pos, taille, player_image, weapon = None):
        """
        __init__ : Fonction d'initialisation d'un personnage
        -----
        Args:
            name (str): Nom du personnage
            max_health (int): Points de vie maximaux du personnage
            max_energy (int): Points d'énergie maximaux du personnage
            damage (int): Points de dégâts du personnage
            defense (int): Points de défense du personnage
        -----
        Returns:
            None
        """
        self._name: str = name
        self._attack_timer = 0
        self._next_attack_time = randint(10, 15)
        self._defense_timer = 0
        self._next_defense_time = randint(10, 20)
        self._ai_move_timer = 0
        self._ai_move_duration = 1.0
        self._ai_direction = pygame.Vector2(0, 0)
        self._current_action: Action = Action.IDLE
        self._current_action_duration: float = 0.0
        self._attack_direction = pygame.Vector2(0, 0)
        self._taille: int = taille
        self._player_pos = player_pos
        self._max_health = max_health
        self._health = max_health # variable qui va changer
        self._max_energy = max_energy # capacité maximale ( qui change pas ou avec un potion )
        self._energy = max_energy # variable qui va changer
        self._weapon : Weapon  = weapon
        self._damage = damage
        self._defense = defense
        self._dodge = dodge
        self._doubleAttaque = doubleAttaque
        self._compteurDoubleAttaque = 0
        self._compteurDodge = 0
        self._compteurKill = 0
        self._target = None
        self._ai_escape_direction = pygame.Vector2(0, 0)
        self._damaged_by = None
        self._flee_direction = None
        self._player_image = player_image



    ######################################
    #####  METHODES DE INTERACTIONS  #####
    ######################################

    def touch_wall(self, world_width, world_height):
        """
        touch_wall: regarde si le personnage touche le mur
        ----
        Args : self, world_width, world_height
        ----
        Return : 
            list des murs touchée
            list vide sinon
        """
        touched_walls = []
        if self._player_pos.x - self.get_taille() == 0:
            touched_walls.append("Gauche")
        if self._player_pos.x + self.get_taille() == world_width:
            touched_walls.append("Droite")
        if self._player_pos.y - self.get_taille() == 0:
            touched_walls.append("Haut")
        if self._player_pos.y + self.get_taille() == world_height:
            touched_walls.append("Bas")
        return touched_walls


    def check_attack_collision(self, personnage_list : list['Personnage'], end_pos):
        for p in personnage_list:
            if p != self and not p.is_dead():
                if self.is_colliding(end_pos, p):
                    self.attack(p)
                    self._target = p

                    
                                

    def bot_move(self, dt, world_width, world_height):
        # Si on est mort - on fait rien    
        if self.is_dead():
            return
        # timer pour le changement de direction
        self._ai_move_timer += dt
        
        # Si le timer atteint son "timeout" on change de direction
        if self._ai_move_timer >= self._ai_move_duration:
            # On reset
            self._ai_move_timer = 0
            AI_choice = randint(1, 4)

            if AI_choice == 1:
                self._ai_direction = pygame.Vector2(1, 0)
            elif AI_choice == 2:
                self._ai_direction = pygame.Vector2(-1, 0)
            elif AI_choice == 3:
                self._ai_direction = pygame.Vector2(0, -1)
            else:
                self._ai_direction = pygame.Vector2(0, 1)

        if self._current_action == Action.INVULNERABLE:

            if self._current_action == Action.INVULNERABLE:

                if self._flee_direction is None and self._damaged_by:
                    self._flee_direction = self._player_pos - self._damaged_by.get_player_pos()

                    walls = self.touch_wall(world_width, world_height)

                    if "Gauche" in walls:
                        self._flee_direction.x = abs(self._flee_direction.x)
                    if "Droite" in walls:
                        self._flee_direction.x = -abs(self._flee_direction.x)
                    if "Haut" in walls:
                        self._flee_direction.y = abs(self._flee_direction.y)
                    if "Bas" in walls:
                        self._flee_direction.y = -abs(self._flee_direction.y)

                    if self._flee_direction.length() > 0:
                        self._ai_escape_direction = self._flee_direction.normalize()

                self._player_pos += self._ai_escape_direction * 500 * dt
        else:
            self._flee_direction = None
            self._ai_escape_direction = pygame.Vector2(0, 0)
            self._player_pos += self._ai_direction * 100 * dt


        self._player_pos.x = max(self.get_taille(), min(self._player_pos.x, world_width - self.get_taille()))
        self._player_pos.y = max(self.get_taille(), min(self._player_pos.y, world_height - self.get_taille()))

    def auto_attaque(self, player_list : list['Personnage'], dt):
        if self._current_action != Action.IDLE:
            return
        self._attack_timer += dt
        if self._attack_timer >= self._next_attack_time:
            new_target_list = [x for x in player_list if x != self and not x.is_dead()]
            if len(new_target_list) == 0:
                return
            self._target = choice(new_target_list)
            direction = self._target.get_player_pos() - self._player_pos
            if direction.length() == 0:
                return
            direction = direction.normalize()
            self.set_attack_direction(direction)
            self.launch_action(Action.ATTAQUE)
            self._attack_timer = 0
            self._next_attack_time = randint(10, 15)

            
    def auto_defense(self,dt):
        if self._current_action != Action.IDLE:
            return

        self._defense_timer += dt

        if self._defense_timer >= self._next_defense_time:
            self.launch_action(Action.DEFENSE)
            self._defense_timer = 0.0
            self._next_defense_time = randint(10, 20)

    def get_attack_end_pos(self, direction = None):
        """
        get_attack_end_pos:
            Calcul la position finale de la range d'attaque
        ----
        Args:
            direction, self
        ----
        Return:
            Vector2 : position finale de la range d'attaque
        """

        direction = direction or self._target.get_player_pos() - self.get_player_pos()
        player_x = self._player_pos.x
        player_y = self._player_pos.y

        direction_x = direction.x
        direction_y = direction.y

        vecteur_normalise = math.sqrt(direction_x**2 + direction_y**2)

        vecteur_normalise_x = direction_x / vecteur_normalise
        vecteur_normalise_y = direction_y / vecteur_normalise

        end_x = player_x + vecteur_normalise_x * self._weapon.get_attack_range()
        end_y = player_y + vecteur_normalise_y * self._weapon.get_attack_range()

        return pygame.Vector2(end_x, end_y)

    def is_colliding(self, direction, enemy_list : list["Personnage"]):
        """
        Docstring for is_colliding
        ----
        Args:
            self, attack_end_pos, enemy
            ----
        Returns:

        """
        weapon : Weapon = self._weapon
        enemy_touched_list = weapon.is_colliding(self._player_pos, direction, enemy_list, self)
        for enemy in enemy_touched_list:
            self.attack(enemy)
        
    def is_idling(self):
        return self._current_action == Action.IDLE

    def is_attacking(self):
        return self._current_action == Action.ATTAQUE

    def is_defending(self):
        return self._current_action == Action.DEFENSE

    def handle_mouvements(self, keys, dt, world_width, world_height):
        """
        Docstring for handle_mouvements
        
        ----
        Args :
            self, keys, dt, world_width, world_height
        ----
        Returns:
            Vector2 : new_player.pos
        """

        if keys[pygame.K_z] or keys[pygame.K_UP]: 
            self._player_pos.y -= 300 * dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self._player_pos.y += 300 * dt
        if keys[pygame.K_q] or keys[pygame.K_LEFT]:
            self._player_pos.x -= 300 * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self._player_pos.x += 300 * dt
    
        
        self._player_pos.x = max(self.get_taille(), min(self._player_pos.x, world_width - self.get_taille()))
        self._player_pos.y = max(self.get_taille(), min(self._player_pos.y, world_height - self.get_taille()))


        return self._player_pos
   
    def handle_actions(self, keys, dt):
        """
        Docstring for handle_actions
        
        :param self: Description
        :param keys: Description
        :param dt: Description
        ----
        Args :
            self, keys, dt
        ----
        Returns : 
            current action
        """
        if self._current_action == Action.IDLE and keys[pygame.K_a]:
            self.launch_action(Action.ATTAQUE)
        if self._current_action == Action.IDLE and keys[pygame.K_e]:
            self.launch_action(Action.DEFENSE)

    def check_action_duration(self, dt):
        if self._current_action != Action.IDLE:
            self._current_action_duration += dt
            if self._current_action_duration >= self._current_action.value["duration"]:
                self._current_action = Action.IDLE
                self._current_action_duration = 0.0 

    def launch_action(self, action):
        """
        Docstring for launch_action
        
        :param self: Description
        :param action: Description
        :param dt: Description
        """
        self._current_action = action
        self._current_action_duration = 0.0  

        



    ################################
    #####  METHODES DE CLASSE  #####
    ################################

    def choose_target(self, other_personnages: list["Personnage"]) -> "Personnage":
        """
        choose_target : Fonction qui choisit le personnage cible parmi la liste des personnages
        -----
        Args:
            other_personnages (list): Liste des personnages
        -----
        Returns:
            Personnage: Personnage cible
        """
        # TODO: Implement the choose_target method
        valid_targets = []
        for personnage in other_personnages:
            if personnage != self and not personnage.is_dead():
                valid_targets.append(personnage)
        # valid_targets = [p for p in other_personnages if p != self and not p.is_dead()]
        target = choice(valid_targets)
        return target
        

    def attack(self, to_target: "Personnage"):
        """
        attack : Fonction qui attaque le personnage cible
        -----
        Args:
            to_target (Personnage): Personnage cible
        -----
        Returns:
            None
        """
        if self.is_dead() or to_target.is_dead() or to_target.get_current_action() == Action.INVULNERABLE:
            return
        total_damage = self._damage

        if self._weapon:
            total_damage += self._weapon.get_damage()
        to_target.get_hit(total_damage,  source = self)
        chanceDeDoubleAttaque = randint(0, 100)
        if chanceDeDoubleAttaque < self._doubleAttaque:
            to_target.get_hit(total_damage, bypass = True, source = self)
            self._compteurDoubleAttaque += 1
            print(f"{self.get_name()} a effectué une double attaque")
        if to_target.is_dead():
            self._compteurKill += 1

        direction_to_target = to_target.get_player_pos() - self._player_pos
        if direction_to_target.length() == 0:
            return
        direction_to_target = direction_to_target.normalize()
        if self._attack_direction.dot(direction_to_target) < 0.5:
            return 

    def handle_attack_direction(self, mouse_pos):
        mouse_vector = mouse_pos - self._player_pos
        if mouse_vector.length() > 0:
            direction = mouse_vector

        self.set_attack_direction(direction)


 
    def get_hit(self, damage, bypass = False, source = None):
        """
        get_damage : Fonction qui retourne les dégâts du personnage
        -----
        Args:
            None
        -----
        Returns:
            int: Dégâts du personnage
        """
        if self._current_action == Action.INVULNERABLE and bypass == False:
            return
        chanceDeDodge = randint(0, 100)
        current_defense = self._defense if self._current_action == Action.DEFENSE else 0
        self._damaged_by = source
        if current_defense >= damage:
            return
        elif chanceDeDodge < self._dodge:
            self._compteurDodge += 1
            print(f"{self.get_name()} a esquivé une attaque.{self._dodge}/100 il a roll {chanceDeDodge}")
            self.launch_action(Action.INVULNERABLE)
            return
        else:
            damage -= current_defense
            print(f"{self.get_name()} a pris {damage} dégats. {self._dodge}/100 il a roll {chanceDeDodge}")
            self.launch_action(Action.INVULNERABLE)
        self._health -= damage
        if self.is_dead():
            print(f"{self.get_name()} est mort!!!  :(  ")
            print(self)


    def rest(self):
        """
        rest : Fonction qui permet au personnage de regagner de l'energie
        -----
        Args:
            None
        -----
        Returns:
            None
        """
        # Implement the rest method
        self.sleep(5)
        self._energy = self._max_energy
        return self._energy
       




    def is_dead(self):
        """
        is_dead : Fonction qui retourne True si le personnage est mort, sinon False
        -----
        Args:
            None
        -----
        Returns:
            bool: True si le personnage est mort, sinon False
        """
        # : Implement the is_dead method
        if self._health <= 0:
            return True
        else:
            return False












    ###########################
    #####     SETTERS     #####
    ###########################

    def set_weapon(self, weapon):
        """
        set_weapon : Donnes le weapon du joueur
        -----
        Args:
        None
        -----
        Returns:
            None
        """
        self._weapon : Weapon = weapon

    def set_attackRange(self, attackRange):
        """
        set_attackRange : Donnes la longueur d'attaque du joueur
        -----
        Args:
        None
        -----
        Returns:
            None
        """
        self._attackRange = attackRange

    def set_attack_direction(self, attack_direction):
        """
        set_attack_direction : Donnes la direction d'attaque du joueur
        -----
        Args:
        None
        -----
        Returns:
            None
        """
        self._attack_direction = attack_direction

    def set_color(self, color):
        """
        set_color : Donnes la couleur du joueur
        -----
        Args:
        None
        -----
        Returns:
            None
        """
        self._color = color

    def set_taille(self, taille):
        """
        set_taille : Donnes la taille du joueur
        -----
        Args:
        None
        -----
        Returns:
            None
        """
        self._taille = taille


    def set_player_pos(self, player_pos):
        """
        set_pos_x : Donnes la position du joueur
        -----
        Args:
        None
        -----
        Returns:
            None
        """
        self._player_pos = player_pos



    def set_dodge(self, dodge):
        """
        set_dodge : Modifie le dodge du personnage
        -----
        Args:
            dodge (str): Nouveau dodge du personnage
        -----
        Returns:
            None
        """
        self._dodge = dodge
   
    def set_doubleAttaque(self, doubleAttaque):
        """
        set_doubleAttaque : Modifie le doubleAttaque du personnage
        -----
        Args:
            doubleAttaque (str): Nouveau doubleAttaque du personnage
        -----
        Returns:
            None
        """
        self._doubleAttaque = doubleAttaque




    def set_name(self, name):
        """
        set_name : Modifie le nom du personnage
        -----
        Args:
            name (str): Nouveau nom du personnage
        -----
        Returns:
            None
        """
        self._name = name




    def set_max_health(self, max_health):
        """
        set_max_health : Modifie les points de vie maximaux du personnage
        -----
        Args:
            max_health (int): Nouveaux points de vie maximaux
        -----
        Returns:
            None
        """
        self._max_health = max_health




    def set_health(self, health):
        """
        set_health : Modifie les points de vie actuels du personnage
        -----
        Args:
            health (int): Points de vie à assigner
        -----
        Returns:
            None
        """
        self._health = health




    def set_max_energy(self, max_energy):
        """
        set_max_energy : Modifie les points d'énergie maximaux du personnage
        -----
        Args:
            max_energy (int): Nouveaux points d'énergie maximaux
        -----
        Returns:
            None
        """
        self._max_energy = max_energy




    def set_energy(self, energy):
        """
        set_energy : Modifie les points d'énergie actuels du personnage
        -----
        Args:
            energy (int): Points d'énergie à assigner
        -----
        Returns:
            None
        """
        self._energy = energy




    def set_damage(self, damage):
        """
        set_damage : Modifie les dégâts du personnage
        -----
        Args:
            damage (int): Nouveaux dégâts
        -----
        Returns:
            None
        """
        self._damage = damage




    def set_defense(self, defense):
        """
        set_defense : Modifie la défense du personnage
        -----
        Args:
            defense (int): Nouvelle défense
        -----
        Returns:
            None
        """
        self._defense = defense








    ###########################
    #####     GETTERS     #####
    ###########################

    def get_player_weapon(self):
        """
        get_player_weapon : Fonction qui retourne le weapon du personnage
        -----
        Args:
            None
        -----
        Returns:
            
        """
        return self._weapon

    def get_player_image(self):
        """
        get_player_image : Fonction qui retourne l'image du personnage
        -----
        Args:
            None
        -----
        Returns:
            
        """
        return self._player_image
    
    def get_current_action(self):
        """
        get_current_action : Fonction qui retourne l'Action en cour du personnage
        -----
        Args:
            None
        -----
        Returns:
            
        """
        return self._current_action

    def get_attackRange(self):
        """
        get_attackRange : Fonction qui retourne la longueur d'attaque du personnage
        -----
        Args:
            None
        -----
        Returns:
            
        """
        return self._attackRange

    def get_attack_direction(self):
        """
        get_attack_direction : Fonction qui retourne la direction d'attaque du personnage
        -----
        Args:
            None
        -----
        Returns:
            
        """
        return self._attack_direction
    
    def get_color(self):
        """
        get_color : Fonction qui retourne la couleur du personnage
        -----
        Args:
            None
        -----
        Returns:
            str: Nom du personnage
        """
        current_color = self._current_action.value.get("couleur")
        return current_color

    def get_taille(self):
        """
        get_taille : Fonction qui retourne la taille du personnage
        -----
        Args:
            None
        -----
        Returns:
            str: Nom du personnage
        """
        return self._taille
    
    def get_player_pos(self):
        """
        get_player_pos : Fonction qui retourne la position du personnage
        -----
        Args:
            None
        -----
        Returns:
            str: Nom du personnage
        """
        return self._player_pos
           

    def get_dodge(self):
        """
        get_dodge : Fonction qui retourne le nom du personnage
        -----
        Args:
            None
        -----
        Returns:
            str: Nom du personnage
        """
        return self._dodge
   
    def get_doubleAttaque(self):
        """
        get_doubleAttaque : Fonction qui retourne le nom du personnage
        -----
        Args:
            None
        -----
        Returns:
            str: Nom du personnage
        """
        return self._doubleAttaque
   
    def get_name(self):
        """
        get_name : Fonction qui retourne le nom du personnage
        -----
        Args:
            None
        -----
        Returns:
            str: Nom du personnage
        """
        return self._name




    def get_max_health(self):
        """
        get_max_health : Fonction qui retourne les points de vie maximaux du personnage
        -----
        Args:
            None
        -----
        Returns:
            int: Points de vie maximaux du personnage
        """
        return self._max_health




    def get_health(self):
        """
        get_health : Fonction qui retourne les points de vie actuels du personnage
        -----
        Args:
            None
        -----
        Returns:
            int: Points de vie actuels du personnage
        """
        return self._health




    def get_max_energy(self):
        """
        get_max_energy : Fonction qui retourne les points d'énergie maximaux du personnage
        -----
        Args:
            None
        -----
        Returns:
            int: Points d'énergie maximaux du personnage
        """
        return self._max_energy




    def get_energy(self):
        """
        get_energy : Fonction qui retourne les points d'énergie actuels du personnage
        -----
        Args:
            None
        -----
        Returns:
            int: Points d'énergie actuels du personnage
        """
        return self._energy




    def get_damage(self):
        """
        get_damage : Fonction qui retourne les dégâts du personnage
        -----
        Args:
            None
        -----
        Returns:
            int: Dégâts du personnage
        """
        return self._damage




    def get_defense(self):
        """
        get_defense : Fonction qui retourne la défense du personnage
        -----
        Args:
            None
        -----
        Returns:
            int: Défense du personnage
        """
        return self._defense
   
    def __str__(self):
        desc = "-----------\n"
        desc += "His name is " + self._name + ". \n"
        desc += "His health is down to " + str(self._health) + " out of " + str(self._max_health) + ".\n"
        desc += "His attack is " + str(self._damage) + ".\n"
        desc += "His defense is " + str(self._defense) + ".\n"
        desc += "He did " + str(self._compteurDodge) + " dodges, and his dodge chance is " + str(self.get_dodge()) +"%, \n"
        desc +=  str(self._compteurDoubleAttaque) + " double attacks, while his doubleAttaque chance is " + str(self._doubleAttaque) +"%\n"
        desc += "And his kill score is " + str(self._compteurKill) + ".\n"
        desc += "----------"
        return desc



