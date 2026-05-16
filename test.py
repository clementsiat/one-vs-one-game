import math

def is_colliding(player_pos, end_pos, enemy_pos):
    """
    Vérifie si le segment [player_pos -> end_pos]
    touche le cercle centré sur enemy_pos avec
    un rayon enemy_pos.get_taille().

    player_pos : tuple (x, y)
    end_pos    : tuple (x, y)
    enemy_pos  : objet avec :
                 - enemy_pos.x
                 - enemy_pos.y
                 - enemy_pos.get_taille()

    Retourne True ou False.
    """
    x1, y1 = player_pos
    x2, y2 = end_pos

    cx = enemy_pos.x
    cy = enemy_pos.y
    radius = enemy_pos.get_taille()

    # Vecteur du segment
    dx = x2 - x1
    dy = y2 - y1

    # Cas où le segment est un point
    if dx == 0 and dy == 0:
        distance = math.hypot(cx - x1, cy - y1)
        return distance <= radius

    # Projection du centre du cercle sur le segment
    t = ((cx - x1) * dx + (cy - y1) * dy) / (dx * dx + dy * dy)

    # Clamp entre 0 et 1 pour rester sur le segment
    t = max(0, min(1, t))

    # Point le plus proche sur le segment
    closest_x = x1 + t * dx
    closest_y = y1 + t * dy

    # Distance entre le cercle et le segment
    distance = math.hypot(cx - closest_x, cy - closest_y)

    return distance <= radius
