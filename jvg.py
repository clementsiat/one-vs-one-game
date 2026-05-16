import pygame
import random
import sys

pygame.init()

# -----------------------
# CONFIG
# -----------------------
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Combat Arena")

font = pygame.font.SysFont("arial", 24)

WHITE = (255, 255, 255)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()

# -----------------------
# CLASSES
# -----------------------

class Fighter:
    def __init__(self, name, x, y, color):
        self.name = name
        self.hp = 100
        self.max_hp = 100
        self.attack = 10
        self.rect = pygame.Rect(x, y, 80, 80)
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def draw_health(self, x, y):
        pygame.draw.rect(screen, RED, (x, y, 200, 20))
        pygame.draw.rect(screen, GREEN, (x, y, 200 * (self.hp/self.max_hp), 20))

# -----------------------
# FONCTIONS
# -----------------------

def draw_text(text, x, y):
    img = font.render(text, True, WHITE)
    screen.blit(img, (x, y))

def attack(attacker, defender):
    damage = random.randint(5, attacker.attack)
    defender.hp -= damage
    return damage

# -----------------------
# BOUTONS
# -----------------------

class Button:
    def __init__(self, text, x, y):
        self.text = text
        self.rect = pygame.Rect(x, y, 150, 40)

    def draw(self):
        pygame.draw.rect(screen, BLACK, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        draw_text(self.text, self.rect.x + 10, self.rect.y + 8)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# -----------------------
# GAME
# -----------------------

player = Fighter("Joueur", 100, 200, (0, 100, 255))
enemy = Fighter("Ennemi", 600, 200, (255, 100, 100))

attack_btn = Button("Attaquer", 100, 400)
heal_btn = Button("Soigner", 300, 400)

player_turn = True
message = ""

running = True
while running:
    screen.fill((30, 30, 30))

    # Draw fighters
    player.draw()
    enemy.draw()

    # Draw HP
    player.draw_health(50, 50)
    enemy.draw_health(550, 50)

    draw_text("Joueur", 50, 20)
    draw_text("Ennemi", 550, 20)

    # Buttons
    attack_btn.draw()
    heal_btn.draw()

    draw_text(message, 250, 350)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and player_turn:
            pos = pygame.mouse.get_pos()

            if attack_btn.is_clicked(pos):
                dmg = attack(player, enemy)
                message = f"Tu infliges {dmg} dégâts !"
                player_turn = False

            elif heal_btn.is_clicked(pos):
                heal = random.randint(10, 20)
                player.hp = min(player.max_hp, player.hp + heal)
                message = f"Tu te soignes de {heal} HP !"
                player_turn = False

    # Tour ennemi
    if not player_turn and enemy.hp > 0:
        pygame.time.delay(500)
        dmg = attack(enemy, player)
        message = f"L'ennemi attaque : {dmg} dégâts !"
        player_turn = True

    # Fin du jeu
    if player.hp <= 0:
        message = "💀 Tu as perdu !"
    elif enemy.hp <= 0:
        message = "🎉 Tu as gagné !"

    pygame.display.flip()
    clock.tick(60)