import pygame
import random
from Personnage import Personnage
from personnage_manager import PersonnageManager
from Weapon import Sword, Spear


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
player_img = pygame.image.load("personnnage1.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (main_player.get_taille()*2, main_player.get_taille()*2))

enemy_img = pygame.image.load("personnnage1.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (enemy.get_taille()*2, enemy.get_taille()*2))

enemy1_img = pygame.image.load("personnnage1.png").convert_alpha()
enemy1_img = pygame.transform.scale(enemy1_img, (enemy1.get_taille()*2, enemy1.get_taille()*2))

background = pygame.image.load("background_one_vs_one.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))




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
            pygame.draw.line(screen, pygame.Color(255,0,0), enemy.get_player_pos(), end_pos, width=5)
        enemy.check_attack_collision(pm.get_personnage_list(), end_pos)


    enemy1.auto_attaque(pm.get_personnage_list(), dt)
    if enemy1.is_attacking():
        end_pos = enemy1.get_attack_end_pos()
        if not enemy1.is_dead():
            pygame.draw.line(screen, pygame.Color(255,0,0), enemy1.get_player_pos(), end_pos, width=5)
        enemy1.check_attack_collision(pm.get_personnage_list(), end_pos)


    #####################
    # ATTAQUE DU JOUEUR #
    #####################
    if main_player.is_attacking():
        direction  = mouse_pos - main_player.get_player_pos()
        end_pos = main_player.get_attack_end_pos(direction)  
        if not main_player.is_dead():    
            pygame.draw.line(screen, pygame.Color(255, 0, 0), main_player.get_player_pos(), end_pos, width = 5)
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
    if not main_player.is_dead():
        pos = main_player.get_player_pos()
        pygame.draw.circle(screen, main_player.get_color(), pos, rayon_player, width=3)
        rect = player_img.get_rect(center=(pos.x, pos.y))
        screen.blit(player_img, rect)
    if not enemy.is_dead():
        pos = enemy.get_player_pos()
        pygame.draw.circle(screen, enemy.get_color(), pos, rayon_enemy, width=3)
        rect = enemy_img.get_rect(center=(pos.x, pos.y))
        screen.blit(enemy_img, rect)
    if not enemy1.is_dead():
        pos = enemy1.get_player_pos()
        pygame.draw.circle(screen, enemy1.get_color(), pos, rayon_enemy1, width=3)
        rect = enemy1_img.get_rect(center=(pos.x, pos.y))
        screen.blit(enemy1_img, rect)


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
