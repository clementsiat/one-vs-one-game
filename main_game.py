import random
import pygame
from Personnage import Personnage
from personnage_manager import PersonnageManager
from weapon_manager import wm
from drop_manager import dm
from drops import Drops
import math
from config import WIDTH, HEIGHT
from image_manager import im
from level_manager import level_manager
from Potion import Potion


# ---------- INITIALISATION PYGAME ----------
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
level_display_time = 0
death_timer = 0
game_over = False

running = True
dt = 0

# Chargement des images
im.load_images()
wm.init_images()

# On récupère les éléments
env_images = im.get_environnement()
weapon_images = im.get_weapon_image()
rect_images = im.get_rect()

pm: 'PersonnageManager' = PersonnageManager.get_instance()

game_started = False
selected_weapon = None


def affichage_player(player: Personnage):
    if not player.is_dead():
        pos = player.get_player_pos()

        pygame.draw.circle(
            screen,
            player.get_color(),
            pos,
            player.get_taille(),
            width=3
        )

        rect = player.get_player_image().get_rect(
            center=(pos.x, pos.y)
        )
        screen.blit(player.get_player_image(), rect)

        pp = player.get_player_pos()
        pt = player.get_taille()

        # Barre de vie rouge
        pygame.draw.line(
            screen,
            (255, 0, 0),
            (pp.x - pt, pp.y - pt * 1.25),
            (pp.x + pt, pp.y - pt * 1.25),
            5
        )

        max_health = player.get_max_health()
        current_health = player.get_health()

        life_prg = current_health * ((pp.x + pt) - (pp.x - pt)) / max_health

        # Barre de vie verte
        pygame.draw.line(
            screen,
            (0, 255, 0),
            (pp.x - pt, pp.y - pt * 1.25),
            (life_prg + (pp.x - pt), pp.y - pt * 1.25),
            5
        )
        if player == main_player:
            player.get_inventory().draw(screen)
        


def affichage_weapon(screen, player: "Personnage", target_pos):
    if player.get_player_weapon() is None:
        return
    start_pos = player.get_player_pos()

    # Direction vers la cible
    direction = target_pos - start_pos

    if direction.length() == 0:
        return

    # Longueur réelle de l'attaque
    distance = direction.length()

    # Normalisation
    direction = direction.normalize()

    # Angle
    angle = math.degrees(math.atan2(-direction.y, direction.x)) - 90

    # Redimensionnement
    weapon_width = player.get_player_weapon().get_image().get_width()
    weapon_height = int(distance)

    if (
        player.get_taille() >= 40
        and player.get_player_weapon().get_weapon_type() == "axe"
    ):
        weapon_width *= 2
        weapon_height *= 1.5

    scaled_weapon = pygame.transform.scale(
        player.get_player_weapon().get_image(),
        (int(weapon_width), int(weapon_height))
    )

    # Rotation
    rotated_weapon = pygame.transform.rotate(
        scaled_weapon,
        angle
    )

    # Milieu entre départ et arrivée
    center_pos = start_pos + direction * (distance / 2)

    rect = rotated_weapon.get_rect(
        center=(center_pos.x, center_pos.y)
    )

    screen.blit(rotated_weapon, rect)


# ---------- BOUCLE PRINCIPALE ----------
while running:
    if game_over:
        screen.fill((0, 0, 0))

        game_over_text = my_font.render(
            "C'EST MORT, TU AS PERDU :(, DOMMAGE",
            True,
            (255, 255, 255)
        )

        text_rect = game_over_text.get_rect(
            center=(WIDTH / 2, HEIGHT / 2)
        )

        screen.blit(game_over_text, text_rect)

        pygame.display.flip()
            

        continue
    ######################
    ##ÉCRAN DE DÉPART#####
    ######################

    if not game_started:

        screen.blit(
            env_images.get('starting_screen'),
            (0, 0)
        )

        screen.blit(
            weapon_images.get('sword'),
            rect_images.get('sword_rect')
        )

        screen.blit(
            weapon_images.get('dagger'),
            rect_images.get('dagger_rect')
        )

        screen.blit(
            weapon_images.get('spear'),
            rect_images.get('spear_rect')
        )

        screen.blit(
            weapon_images.get('axe'),
            rect_images.get('axe_rect')
        )

        events = pygame.event.get()

        for event in events:

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                if rect_images.get('sword_rect').collidepoint(event.pos):
                    selected_weapon = wm.create_sword()

                elif rect_images.get('dagger_rect').collidepoint(event.pos):
                    selected_weapon = wm.create_dagger()

                elif rect_images.get('spear_rect').collidepoint(event.pos):
                    selected_weapon = wm.create_spear()

                elif rect_images.get('axe_rect').collidepoint(event.pos):
                    selected_weapon = wm.create_axe()

                if selected_weapon is not None:

                    main_player = pm.add_personnage(selected_weapon)

                    main_player.set_player_pos(
                        pygame.Vector2(200, 360)
                    )

                    nombre = level_manager.nombre_enemies()

                    pm.generate_wave(
                        (WIDTH, HEIGHT),
                        wm,
                        nombre
                    )

                    game_started = True

        pygame.display.flip()
        continue

    #######
    ##JEU##
    #######

    # Fond
    screen.blit(
        env_images.get('background'),
        (0, 0)
    )

    # Niveau
    text_surface = my_font.render(
        'Niveau = ' + str(level_manager.get_level()),
        False,
        (255, 255, 255)
    )

    screen.blit(
        text_surface,
        (0, 0)
    )

    # Nombre de potions
    nb_potions = sum(
        isinstance(item, Potion)
        for item in main_player.get_inventory().get_items()
    )

    text_surface = my_font.render(
        'Potions = ' + str(nb_potions),
        False,
        (255, 255, 255)
    )

    screen.blit(
        text_surface,
        (0, 50)
    )

    #################
    ###ÉVÉNEMENTS####
    #################

    # IMPORTANT :
    # pygame.event.get() est appelé UNE SEULE FOIS par frame.
    events = pygame.event.get()

    for event in events:

        # Fermer le jeu
        if event.type == pygame.QUIT:
            running = False

        # Ramasser le drop le plus proche avec F.
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            if dm.try_pickup(main_player):
                print("Objet récupéré !")

        # Attaque à la souris
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            mouse_pos = pygame.Vector2(
                pygame.mouse.get_pos()
            )

            direction = (
                mouse_pos -
                main_player.get_player_pos()
            )

            main_player.set_attack_direction(direction)

            # On lance l'attaque
            main_player.launch_action(
                main_player._current_action.ATTAQUE
            )

    ##############################
    ###RÉCUPÉRATION DES TOUCHES###
    ##############################

    keys = pygame.key.get_pressed()

    mouse_pos = pygame.Vector2(
        pygame.mouse.get_pos()
    )

    ##############
    ###LEVEL UP###
    ##############

    if level_manager.is_level_finished(
        pm.get_personnage_list(),
        main_player
    ):

        level_manager.next_level()

        nb_enemies = level_manager.nombre_enemies()

        pm.generate_wave(
            (WIDTH, HEIGHT),
            wm,
            nb_enemies
        )

        text_level_up = main_player.level_up()

        text_level_surface = my_font.render(
            text_level_up,
            False,
            (255, 255, 255)
        )

        level_display_time = 5

    if level_display_time > 0:

        screen.blit(
            text_level_surface,
            (WIDTH / 4, 0)
        )

        level_display_time -= dt

    ##############
    ###ENNEMIS####
    ##############

    for enemy in pm.get_personnage_list():
        if enemy == main_player:
            continue
        enemy.auto_defense(dt)
        enemy.auto_attaque(
            pm.get_personnage_list(),
            dt
        )
        if enemy.is_attacking():
            end_pos = enemy.get_attack_end_pos()
            direction = enemy.get_attack_direction()
            if not enemy.is_dead():
                affichage_weapon(
                    screen,
                    enemy,
                    end_pos
                )
            enemy.is_colliding(
                direction,
                pm.get_personnage_list()
            )

        enemy.check_action_duration(dt)
        enemy.bot_move(
            dt,
            WIDTH,
            HEIGHT
        )

    ##################################
    ##GESTION DES ACTIONS DU JOUEUR###
    ##################################

    main_player.handle_actions(
        keys,
        events
    )
    main_player.check_action_duration(dt)

    #####################
    ##ATTAQUE DU JOUEUR##
    #####################

    if main_player.is_attacking():

        direction = (
            mouse_pos -
            main_player.get_player_pos()
        )

        if not main_player.is_dead():

            affichage_weapon(
                screen,
                main_player,
                main_player.get_attack_end_pos(direction)
            )

        enemies_touched = main_player.is_colliding(
            direction,
            pm.get_personnage_list()
        )

    dm.update_dead_personnages(pm.get_personnage_list(), excluded=main_player)

    ################
    ##MOUVEMENTS####
    ################

    if not main_player.is_dead():
        main_player.handle_mouvements(
            keys,
            dt,
            WIDTH,
            HEIGHT
        )

    if main_player.is_dead():
        death_timer += dt

        if death_timer >= 5:
            game_over = True

    ############################
    ##DESSIN DES PERSONNAGES####
    ############################

    for element in pm.get_personnage_list():
        affichage_player(element)

    # Les drops sont dessinés au-dessus du décor et sous l'interface finale.
    dm.draw_drops(screen)

    pygame.display.flip()

    # FPS
    dt = clock.tick(60) / 1000


pygame.quit()