import pygame
import random
from Personnage import Personnage
from personnage_manager import PersonnageManager
from weapon_manager import WeaponManager
from Weapon import Sword, Spear, Dagger, Axe
import math

WIDTH = 1280
HEIGHT = 720

# ---------- INITIALISATION PYGAME ----------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True
dt = 0

# ---------- CHARGEMENT DES IMAGES ----------
starting_screen = pygame.image.load("Images/starting_screen.png").convert()
starting_screen = pygame.transform.scale(starting_screen, (WIDTH, HEIGHT))

background = pygame.image.load("Images/background_one_vs_one.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

sword_img = pygame.image.load("Images/sword.png").convert_alpha()
sword_img = pygame.transform.scale(sword_img, (33, 70))
dagger_img = pygame.image.load("Images/dagger.png").convert_alpha()
dagger_img = pygame.transform.scale(dagger_img, (28, 50))
spear_img = pygame.image.load("Images/spear.png").convert_alpha()
spear_img = pygame.transform.scale(spear_img, (12, 130))
axe_img = pygame.image.load("Images/axe.png").convert_alpha()
axe_img = pygame.transform.scale(axe_img, (37, 100))
sword_rect = sword_img.get_rect(center=(150, 150))
dagger_rect = dagger_img.get_rect(center=(WIDTH - 150, 150))
spear_rect = spear_img.get_rect(center=(150, HEIGHT - 150))
axe_rect = axe_img.get_rect(center=(WIDTH - 150, HEIGHT - 150))
# ---------- CREATION DES PERSONNAGES ----------
weapon_image_list = {
    "spear": spear_img,
    "dagger": dagger_img,
    "sword": sword_img,
    "axe": axe_img
}

wm : 'WeaponManager' = WeaponManager(weapon_image_list)
pm  : 'PersonnageManager'= PersonnageManager.get_instance()

game_started = False
selected_weapon = None
main_player = pm.add_personnage(wm.create_axe())
main_player.set_player_pos(pygame.Vector2(200, 360))





# ---------- RAYONS DES CERCLES ----------
rayon_player = int(main_player.get_taille() * 0.2)


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

def affichage_weapon(screen, player : "Personnage", target_pos):
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
    weapon_width = 40
    weapon_height = int(distance)

    scaled_weapon = pygame.transform.scale(
        player.get_player_weapon().get_image(),
        (weapon_width, weapon_height)
    )

    # rotation
    rotated_weapon = pygame.transform.rotate(scaled_weapon, angle)

    # milieu entre départ et arrivée
    center_pos = start_pos + direction * (distance / 2)

    rect = rotated_weapon.get_rect(
        center=(center_pos.x, center_pos.y)
    )

    screen.blit(rotated_weapon, rect)


# character = Personnage(XXXXX, pos_x, pos_y)
while running:
    if not game_started:

        screen.blit(starting_screen, (0, 0))

        screen.blit(sword_img, sword_rect)
        screen.blit(dagger_img, dagger_rect)
        screen.blit(spear_img, spear_rect)
        screen.blit(axe_img, axe_rect)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                if sword_rect.collidepoint(event.pos):
                    selected_weapon = wm.create_sword()

                elif dagger_rect.collidepoint(event.pos):
                    selected_weapon = wm.create_dagger()

                elif spear_rect.collidepoint(event.pos):
                    selected_weapon = wm.create_spear()

                elif axe_rect.collidepoint(event.pos):
                    selected_weapon = wm.create_axe()

                if selected_weapon is not None:

                    main_player = pm.add_personnage(selected_weapon)
                    main_player.set_player_pos(pygame.Vector2(200, 360))

                    pm.generate_wave((WIDTH, HEIGHT), wm)

                    game_started = True

        pygame.display.flip()
        continue

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

    for enemy in pm.get_personnage_list():
        if enemy == main_player:
            continue

    ######################
    # DEFENSE DE L'ENEMY #
    ######################
        enemy.auto_defense(dt)


    ######################
    # ATTAQUE DE L'ENEMY #
    ######################
        enemy.auto_attaque(pm.get_personnage_list(), dt)
        if enemy.is_attacking():
            end_pos = enemy.get_attack_end_pos()
            direction = enemy.get_attack_direction()
            if not enemy.is_dead():
                affichage_weapon(screen, enemy, end_pos)
            enemy.is_colliding(direction, pm.get_personnage_list())
        enemy.check_action_duration(dt)
        enemy.bot_move(dt, WIDTH, HEIGHT)
    
    
    
    
    
    
    
    #######################
    # GESTION DES ACTIONS #
    #######################
    
    main_player.handle_actions(keys, dt)
    main_player.check_action_duration(dt)
    #####################
    # ATTAQUE DU JOUEUR #
    #####################
    if main_player.is_attacking():
        direction  = mouse_pos - main_player.get_player_pos()
        if not main_player.is_dead():    
            affichage_weapon(screen, main_player, main_player.get_attack_end_pos(direction))
        main_player.is_colliding(direction, pm.get_personnage_list())

    
    ##########################
    # GESTION DES MOUVEMENTS #
    ##########################
    main_player.handle_mouvements(keys, dt, WIDTH, HEIGHT)

  

    




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
