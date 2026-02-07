# Example file showing a circle moving on screen
import pygame
from Personnage import Personnage
from personnage_manager import PersonnageManager


WIDTH = 1280
HEIGHT = 720   



# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0

pm = PersonnageManager.get_instance()
main_player = pm.add_personnage()
enemy = pm.add_personnage()

main_player.set_player_pos(pygame.Vector2(200, 360))

enemy.set_player_pos(pygame.Vector2(800, 360))


# character = Personnage(XXXXX, pos_x, pos_y)
while running:
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("yellow")
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

    #####################
    # ATTAQUE DU JOUEUR #
    #####################
    if main_player.is_attacking():
        direction  = mouse_pos - main_player.get_player_pos()
        end_pos = main_player.get_attack_end_pos(direction)  
        pygame.draw.line(screen, pygame.Color(255, 0, 0), main_player.get_player_pos(), end_pos, width = 5)
        # Si l'attaque touche
        if main_player.is_colliding(end_pos, enemy):
            main_player.attack(enemy)
    
    ##########################
    # GESTION DES MOUVEMENTS #
    ##########################
    main_player.handle_mouvements(keys, dt, WIDTH, HEIGHT)

    #######################
    # GESTION DES ACTIONS #
    #######################
    main_player.handle_actions(keys, dt)
    enemy.bot_move(dt)


    ##########################
    # DESSIN DES PERSONNAGES #
    ##########################
    pygame.draw.circle(screen, main_player.get_color(), main_player.get_player_pos(), main_player.get_taille())
    pygame.draw.circle(screen, enemy.get_color(), enemy.get_player_pos(), enemy.get_taille())



    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
