Ce projet est un jeu développé en Python avec Pygame.
Le joueur contrôle un personnage pouvant se déplacer dans une zone délimitée et effectuer des actions comme attaquer ou se défendre.

Un ennemi est également présent et possède un comportement simple :
- déplacement aléatoire
- défense déclenchée périodiquement

main_game.py
Ce fichier initialise Pygame, crée la fenêtre pygame, contient la boucle principale du jeu, appelle les fonctions de mise à jour (mouvements, actions, IA)

Personnage.py
Ce fichier contient la classe Personnage.

Elle gère :
- La position du personnage
- Les déplacements
- Les actions (attaque, défense)
- La gestion du temps des actions
- L’IA simple de l’ennemi


Contrôles du jeu

Z / Q / S / D ou flèches → déplacement

A → attaque

E → défense
