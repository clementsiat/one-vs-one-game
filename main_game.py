import pygame
import random
from Personnage import Personnage
from personnage_manager import PersonnageManager
from Weapon import Sword, Spear
import math

WIDTH = 1280
HEIGHT = 720

# ---------- INITIALISATION PYGAME ----------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True
dt = 0

# ---------- CREATION DES PERSONNAGES ----------

pm  : 'PersonnageManager'= PersonnageManager.get_instance()
main_player = pm.add_personnage()
enemy : 'Personnage' = pm.add_personnage()
enemy1 : 'Personnage' = pm.add_personnage()

main_player.set_player_pos(pygame.Vector2(200, 360))

enemy.set_player_pos(pygame.Vector2(800, 360))
enemy1.set_player_pos(pygame.Vector2(800, 360))

# ---------- RAYONS DES CERCLES ----------
rayon_player = int(main_player.get_taille() * 0.2)
rayon_enemy = int(enemy.get_taille() * 0.2)
rayon_enemy1 = int(enemy1.get_taille() * 0.2)


# ---------- CHARGEMENT DES IMAGES ----------
background = pygame.image.load("Images/background_one_vs_one.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

sword_img = pygame.image.load("Images/Sword.png").convert_alpha()
sword_img = pygame.transform.scale(sword_img, (20, 70))
#redimensionner l'épée
#sword = pygame.transform.scale(sword, (WIDTH, HEIGHT))

def affichage_player(player : Personnage):
    if not player.is_dead():
        pos = player.get_player_pos()
        pygame.draw.circle(screen, player.get_color(), pos, rayon_player, width=3)
        rect = player.get_player_image().get_rect(center=(pos.x, pos.y))
        screen.blit(player.get_player_image(), rect)
        pp = player.get_player_pos()
        pt = player.get_taille()
        pygame.draw.line(screen, (255, 0, 0), (pp.x - pt, pp.y - pt*1.25), (pp.x + pt, pp.y - pt*1.25), 5)
        max_health = player.get_max_health()
        current_health = player.get_health()
        life_prg = current_health * ((pp.x + pt) - (pp.x - pt)) / max_health
        pygame.draw.line(screen, (0, 255, 0), (pp.x - pt, pp.y - pt*1.25), (life_prg + (pp.x - pt), pp.y - pt*1.25), 5)


def affichage_épée(screen, sword_img, player, target_pos):

    start_pos = player.get_player_pos()

    # direction vers la cible
    direction = target_pos - start_pos

    if direction.length() == 0:
        return

    # longueur réelle de l'attaque
    distance = direction.length()

    # normalisation
    direction = direction.normalize()

    # angle
    angle = math.degrees(math.atan2(-direction.y, direction.x)) - 90

    # ---- REDIMENSIONNEMENT ----
    sword_width = 40
    sword_height = int(distance)

    scaled_sword = pygame.transform.scale(
        sword_img,
        (sword_width, sword_height)
    )

    # rotation
    rotated_sword = pygame.transform.rotate(scaled_sword, angle)

    # milieu entre départ et arrivée
    center_pos = start_pos + direction * (distance / 2)

    rect = rotated_sword.get_rect(
        center=(center_pos.x, center_pos.y)
    )

    screen.blit(rotated_sword, rect)

# character = Personnage(XXXXX, pos_x, pos_y)
while running:
    # fill the screen with a color to wipe away anything from last frame
    screen.blit(background, (0, 0))
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ############################
    # RECUPERATION DES TOUCHES #
    ############################
    keys = pygame.key.get_pressed()    
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

    ##################
    # Attaque souris #
    ##################
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if main_player._current_action.IDLE:
            direction  = mouse_pos - main_player.get_player_pos()
            main_player._current_action = main_player._current_action.ATTAQUE

    ######################
    # DEFENSE DE L'ENEMY #
    ######################
    enemy.auto_defense(dt)
    enemy1.auto_defense(dt)

    ######################
    # ATTAQUE DE L'ENEMY #
    ######################
    enemy.auto_attaque(pm.get_personnage_list(), dt)
    if enemy.is_attacking():
        end_pos = enemy.get_attack_end_pos()
        if not enemy.is_dead():
            affichage_épée(screen, sword_img, enemy, end_pos)
            #pygame.draw.line(screen, pygame.Color(255,0,0), enemy.get_player_pos(), end_pos, width=5)
        enemy.check_attack_collision(pm.get_personnage_list(), end_pos)


    enemy1.auto_attaque(pm.get_personnage_list(), dt)
    if enemy1.is_attacking():
        end_pos = enemy1.get_attack_end_pos()
        if not enemy1.is_dead():
            affichage_épée(screen, sword_img, enemy1, end_pos)
            #pygame.draw.line(screen, pygame.Color(255,0,0), enemy1.get_player_pos(), end_pos, width=5)
        enemy1.check_attack_collision(pm.get_personnage_list(), end_pos)


    #####################
    # ATTAQUE DU JOUEUR #
    #####################
    if main_player.is_attacking():
        direction  = mouse_pos - main_player.get_player_pos()
        end_pos = main_player.get_attack_end_pos(direction)  
        if not main_player.is_dead():    
            affichage_épée(screen, sword_img, main_player, end_pos)
            #pygame.draw.line(screen, pygame.Color(255, 0, 0), main_player.get_player_pos(), end_pos, width = 5)
        # Si l'attaque touche
        if main_player.is_colliding(end_pos, enemy):
            main_player.attack(enemy)
        if main_player.is_colliding(end_pos, enemy1):
            main_player.attack(enemy1)
    
    ##########################
    # GESTION DES MOUVEMENTS #
    ##########################
    main_player.handle_mouvements(keys, dt, WIDTH, HEIGHT)

    #######################
    # GESTION DES ACTIONS #
    #######################
    main_player.handle_actions(keys, dt)
    main_player.check_action_duration(dt)
    enemy.check_action_duration(dt)
    enemy.bot_move(dt, WIDTH, HEIGHT)
    enemy1.check_action_duration(dt)
    enemy1.bot_move(dt, WIDTH, HEIGHT)

    




    ##########################
    # DESSIN DES PERSONNAGES #
    ##########################
    for element in pm.get_personnage_list():
        affichage_player(element)




    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
