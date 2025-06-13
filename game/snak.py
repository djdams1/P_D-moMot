# ETML
# Author : Damien Rochat
# Date : 02/06/2025
# Description : Système de lancement des jeux par interface graphique

import pygame
import sys
import random
from pygame.locals import *
import subprocess
import os

# Init Pygame
pygame.init()
fenetre = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Polices et couleurs
font_grande = pygame.font.SysFont('Century Gothic', 33)
font_petite = pygame.font.SysFont('Century Gothic', 18)
couleur_texte_normal = (47, 6, 1)
couleur_texte_survol = (34, 87, 122)


# Taille des cases (grille)
TILE_SIZE = 20
NB_TILES_X = 800 // TILE_SIZE
NB_TILES_Y = 600 // TILE_SIZE

base_path = os.path.dirname(os.path.abspath(__file__))
pomme_image = pygame.image.load(os.path.join(base_path, "snake", "pomme.png")).convert_alpha()
pomme_image = pygame.transform.scale(pomme_image, (TILE_SIZE, TILE_SIZE))

try:
    serpent_image = pygame.image.load(os.path.join(base_path, "snake", "corps1.png")).convert_alpha()
    serpent_image = pygame.transform.scale(serpent_image, (TILE_SIZE, TILE_SIZE))
    use_serpent_texture = True
except FileNotFoundError:
    use_serpent_texture = False

try:
    tete_image = pygame.image.load(os.path.join(base_path, "snake", "tete.png")).convert_alpha()
    tete_image = pygame.transform.scale(tete_image, (TILE_SIZE, TILE_SIZE))
    use_tete_texture = True
except FileNotFoundError:
    use_tete_texture = False
1
try:
    keu_image = pygame.image.load(os.path.join(base_path, "snake", "keu.png")).convert_alpha()
    keu_image = pygame.transform.scale(keu_image, (TILE_SIZE, TILE_SIZE))
    use_keu_texture = True
except FileNotFoundError:
    use_keu_texture = False


# ... tout le début inchangé ...

def main():
    snake = [(5, 5)]
    direction = (1, 0)
    pommes = [(random.randint(0, NB_TILES_X - 1), random.randint(0, NB_TILES_Y - 1)) for _ in range(800)]
    score = 0
    continuer = True
    direction_changed = False

    while continuer:
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer = False
            elif event.type == KEYDOWN and not direction_changed:
                if event.key == K_DELETE:
                    continuer = False
                elif event.key == K_UP and direction != (0, 1):
                    direction = (0, -1)
                    direction_changed = True
                elif event.key == K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                    direction_changed = True
                elif event.key == K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                    direction_changed = True
                elif event.key == K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)
                    direction_changed = True

        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        direction_changed = False

        if head in snake or head[0] < 0 or head[1] < 0 or head[0] >= NB_TILES_X or head[1] >= NB_TILES_Y:
            continuer = False

        snake.insert(0, head)

        if head in pommes:
            score += 1
            index = pommes.index(head)
            while True:
                nouvelle_pomme = (random.randint(0, NB_TILES_X - 1), random.randint(0, NB_TILES_Y - 1))
                if nouvelle_pomme not in snake and nouvelle_pomme not in pommes:
                    pommes[index] = nouvelle_pomme
                    break
        else:
            snake.pop()

        # --- DESSIN ---
        fenetre.fill((243, 232, 238))
        fenetre.blit(font_grande.render("Snake Game", True, couleur_texte_normal), (155, 10))
        fenetre.blit(font_petite.render("Touche DELETE pour revenir au lobby", True, (245, 133, 73)), (155, 40))
        fenetre.blit(font_petite.render(f"Score: {score}", True, couleur_texte_survol), (10, 570))

        for pomme in pommes:
            fenetre.blit(pomme_image, (pomme[0]*TILE_SIZE, pomme[1]*TILE_SIZE))

        for i, segment in enumerate(snake):
            x, y = segment[0] * TILE_SIZE, segment[1] * TILE_SIZE

            # Tête
            if i == 0:
                if len(snake) > 1:
                    dir_tete = (snake[0][0] - snake[1][0], snake[0][1] - snake[1][1])
                else:
                    dir_tete = direction
                angle = (get_angle(dir_tete) + 180) % 360
                if use_tete_texture:
                    image = pygame.transform.rotate(tete_image, angle)
                    fenetre.blit(image, (x, y))
                elif use_serpent_texture:
                    image = pygame.transform.rotate(serpent_image, angle)
                    fenetre.blit(image, (x, y))
                else:
                    pygame.draw.rect(fenetre, (150, 180, 120), (x, y, TILE_SIZE, TILE_SIZE))

            # Queue
            elif i == len(snake) - 1:
                if len(snake) > 1:
                    dir_queue = (snake[-2][0] - snake[-1][0], snake[-2][1] - snake[-1][1])
                    angle = (get_angle(dir_queue) + 180) % 360
                else:
                    angle = 0
                if use_keu_texture:
                    image = pygame.transform.rotate(keu_image, angle)
                    fenetre.blit(image, (x, y))
                elif use_serpent_texture:
                    image = pygame.transform.rotate(serpent_image, angle)
                    fenetre.blit(image, (x, y))
                else:
                    pygame.draw.rect(fenetre, (90, 110, 80), (x, y, TILE_SIZE, TILE_SIZE))

            # Corps
            else:
                if use_serpent_texture:
                    prev_segment = snake[i - 1]
                    next_segment = snake[i + 1]

                    dx1 = segment[0] - prev_segment[0]
                    dy1 = segment[1] - prev_segment[1]
                    dx2 = next_segment[0] - segment[0]
                    dy2 = next_segment[1] - segment[1]

                    # Si en ligne droite
                    if (dx1 == dx2 and dy1 == dy2):
                        angle = get_angle((dx1, dy1)) + 180
                        image = pygame.transform.rotate(serpent_image, angle % 360)
                    else:
                        # Angle, donc on va afficher le corps tourné pour une courbe
                        if (dx1, dy1) == (0, -1) and (dx2, dy2) == (1, 0) or (dx1, dy1) == (-1, 0) and (dx2, dy2) == (0, 1):
                            angle = 0  # haut -> droite ou gauche -> bas
                        elif (dx1, dy1) == (0, -1) and (dx2, dy2) == (-1, 0) or (dx1, dy1) == (1, 0) and (dx2, dy2) == (0, 1):
                            angle = 90
                        elif (dx1, dy1) == (0, 1) and (dx2, dy2) == (-1, 0) or (dx1, dy1) == (1, 0) and (dx2, dy2) == (0, -1):
                            angle = 180
                        elif (dx1, dy1) == (0, 1) and (dx2, dy2) == (1, 0) or (dx1, dy1) == (-1, 0) and (dx2, dy2) == (0, -1):
                            angle = 270
                        else:
                            angle = 0  # fallback

                        image = pygame.transform.rotate(serpent_image, angle)

                    fenetre.blit(image, (x, y))
                else:
                    pygame.draw.rect(fenetre, (109, 118, 91), (x, y, TILE_SIZE, TILE_SIZE))



        pygame.display.update()
        clock.tick(10)

    # Game Over
    fenetre.blit(font_grande.render("Game Over", True, (200, 0, 0)), (320, 250))
    pygame.display.update()
    pygame.time.wait(2000)
    pygame.quit()
    
    relancer_main()

def get_angle(direction):
    if direction == (1, 0):   # droite
        return 270
    elif direction == (-1, 0):  # gauche
        return 90
    elif direction == (0, -1):  # haut
        return 0
    elif direction == (0, 1):  # bas
        return 180
    return 0


def relancer_main():
    base_path = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))
    main_path = os.path.join(base_path, "main.exe" if getattr(sys, 'frozen', False) else os.path.abspath(os.path.join(base_path, "..", "main.py")))
    subprocess.run([sys.executable, main_path])


if __name__ == "__main__":
    main()
