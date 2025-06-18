# ETML
# Author : Damien Rochat
# Date : 02/06/2025
# Description : Système de lancement des jeux par interface graphique - Snake optimisé

import pygame
import sys
import random
from pygame.locals import *
import subprocess
import os

# --- Constantes et initialisations ---
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TILE_SIZE = 20
NB_TILES_X = SCREEN_WIDTH // TILE_SIZE
NB_TILES_Y = SCREEN_HEIGHT // TILE_SIZE

fenetre = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

font_grande = pygame.font.SysFont('Century Gothic', 33)
font_petite = pygame.font.SysFont('Century Gothic', 18)

COULEUR_TEXTE_NORMAL = (47, 6, 1)
COULEUR_TEXTE_SURVOL = (34, 87, 122)
COULEUR_SCORE = (245, 133, 73)
COULEUR_GAMEOVER = (200, 0, 0)

base_path = os.path.dirname(os.path.abspath(__file__))
snake_folder = os.path.join(base_path, "snake")

# --- Chargement des images avec fallback ---
def charger_image(nom_fichier, taille=(TILE_SIZE, TILE_SIZE)):
    try:
        img = pygame.image.load(os.path.join(snake_folder, nom_fichier)).convert_alpha()
        return pygame.transform.scale(img, taille)
    except FileNotFoundError:
        return None

pomme_image = charger_image("pomme.png")
serpent_image = charger_image("corps1.png")
tete_image = charger_image("tete.png")
keu_image = charger_image("keu.png")
angle_image = charger_image("angle.png")
bg_image = charger_image("bg.jpg")
bg1_image = charger_image("bg1.jpg")

use_bg = bg_image is not None
use_bg1 = bg1_image is not None
use_tete_texture = tete_image is not None
use_serpent_texture = serpent_image is not None
use_keu_texture = keu_image is not None
use_angle_texture = angle_image is not None

# --- Fonctions utilitaires ---

def get_angle(direction):
    """Retourne l'angle de rotation en fonction de la direction du segment."""
    dx, dy = direction
    if (dx, dy) == (1, 0):    # droite
        return 270
    if (dx, dy) == (-1, 0):   # gauche
        return 90
    if (dx, dy) == (0, -1):   # haut
        return 0
    if (dx, dy) == (0, 1):    # bas
        return 180
    return 0

def dessiner_fond():
    """Dessine le fond en damier ou uni selon les images disponibles."""
    if use_bg and use_bg1:
        for i in range(NB_TILES_X):
            for j in range(NB_TILES_Y):
                img = bg_image if (i + j) % 2 == 0 else bg1_image
                fenetre.blit(img, (i * TILE_SIZE, j * TILE_SIZE))
    elif use_bg:
        for i in range(NB_TILES_X):
            for j in range(NB_TILES_Y):
                fenetre.blit(bg_image, (i * TILE_SIZE, j * TILE_SIZE))
    else:
        fenetre.fill((240, 240, 240))

def dessiner_snake(snake, direction):
    """Dessine le serpent avec ses textures et rotations."""
    for i, segment in enumerate(snake):
        x, y = segment[0] * TILE_SIZE, segment[1] * TILE_SIZE

        # Tête
        if i == 0:
            dir_tete = (snake[0][0] - snake[1][0], snake[0][1] - snake[1][1]) if len(snake) > 1 else direction
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
                prev_seg = snake[i - 1]
                next_seg = snake[i + 1]
                dx1, dy1 = segment[0] - prev_seg[0], segment[1] - prev_seg[1]
                dx2, dy2 = next_seg[0] - segment[0], next_seg[1] - segment[1]

                if (dx1 == dx2 and dy1 == dy2):
                    # Ligne droite
                    angle = (get_angle((dx1, dy1)) + 180) % 360
                    image = pygame.transform.rotate(serpent_image, angle)
                else:
                    # Angle
                    if use_angle_texture:
                        # Cas d'angles précis
                        if ((dx1, dy1), (dx2, dy2)) in [((0, -1), (1, 0)), ((-1, 0), (0, 1))]:
                            angle = 0
                        elif ((dx1, dy1), (dx2, dy2)) in [((0, -1), (-1, 0)), ((1, 0), (0, 1))]:
                            angle = 270
                        elif ((dx1, dy1), (dx2, dy2)) in [((0, 1), (-1, 0)), ((1, 0), (0, -1))]:
                            angle = 180
                        elif ((dx1, dy1), (dx2, dy2)) in [((0, 1), (1, 0)), ((-1, 0), (0, -1))]:
                            angle = 90
                        else:
                            angle = 0
                        image = pygame.transform.rotate(angle_image, angle)
                    else:
                        image = serpent_image  # fallback
                fenetre.blit(image, (x, y))
            else:
                pygame.draw.rect(fenetre, (109, 118, 91), (x, y, TILE_SIZE, TILE_SIZE))

def relancer_main():
    """Relance le programme main.py ou main.exe selon le contexte."""
    base_path = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))
    if getattr(sys, 'frozen', False):
        main_path = os.path.join(base_path, "main.exe")
        subprocess.run([main_path])
    else:
        main_path = os.path.abspath(os.path.join(base_path, "..", "main.py"))
        subprocess.run([sys.executable, main_path])

def main():
    snake = [(5, 5), (4, 5), (3, 5)]
    direction = (1, 0)
    pommes = []
    score = 0
    direction_changed = False
    continuer = True

    vitesse_snake = 75  # ms entre déplacements du serpent
    temps_derniere_mise_a_jour = pygame.time.get_ticks()

    # Génération initiale des pommes sans collision avec le serpent
    while len(pommes) < 10:
        pos = (random.randint(0, NB_TILES_X - 1), random.randint(0, NB_TILES_Y - 1))
        if pos not in snake and pos not in pommes:
            pommes.append(pos)

    while continuer:
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer = False
            elif event.type == KEYDOWN and not direction_changed:
                if event.key == K_DELETE:
                    continuer = False
                keys = pygame.key.get_pressed()
                if keys[K_UP] and direction != (0, 1):
                    direction = (0, -1)
                    direction_changed = True
                elif keys[K_DOWN] and direction != (0, -1):
                    direction = (0, 1)
                    direction_changed = True
                elif keys[K_LEFT] and direction != (1, 0):
                    direction = (-1, 0)
                    direction_changed = True
                elif keys[K_RIGHT] and direction != (-1, 0):
                    direction = (1, 0)
                    direction_changed = True

        # Avancer le serpent uniquement toutes les "vitesse_snake" ms
        temps_courant = pygame.time.get_ticks()
        if temps_courant - temps_derniere_mise_a_jour > vitesse_snake:
            temps_derniere_mise_a_jour = temps_courant

            # Calcul nouvelle tête
            head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
            direction_changed = False

            # Conditions de fin
            if head in snake or not (0 <= head[0] < NB_TILES_X) or not (0 <= head[1] < NB_TILES_Y):
                continuer = False
                continue

            snake.insert(0, head)

            if head in pommes:
                score += 1
                index = pommes.index(head)
                # Nouvelle pomme sans collision
                while True:
                    nouvelle_pomme = (random.randint(0, NB_TILES_X - 1), random.randint(0, NB_TILES_Y - 1))
                    if nouvelle_pomme not in snake and nouvelle_pomme not in pommes:
                        pommes[index] = nouvelle_pomme
                        break
            else:
                snake.pop()

        # --- Dessin ---
        dessiner_fond()

        fenetre.blit(font_grande.render("Snake Game", True, COULEUR_TEXTE_NORMAL), (155, 10))
        fenetre.blit(font_petite.render("Touche DELETE pour revenir au lobby", True, COULEUR_SCORE), (155, 40))
        fenetre.blit(font_petite.render(f"Score: {score}", True, COULEUR_TEXTE_SURVOL), (10, 570))

        # Pommes
        if pomme_image:
            for pomme in pommes:
                fenetre.blit(pomme_image, (pomme[0] * TILE_SIZE, pomme[1] * TILE_SIZE))
        else:
            # fallback pommes rouges
            for pomme in pommes:
                pygame.draw.rect(fenetre, (255, 0, 0), (pomme[0] * TILE_SIZE, pomme[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        # Serpent
        dessiner_snake(snake, direction)

        pygame.display.update()
        clock.tick(60)

    # Game Over
    fenetre.fill((243, 232, 238))
    fenetre.blit(font_grande.render("Game Over", True, COULEUR_GAMEOVER), (320, 250))
    fenetre.blit(font_petite.render(f"Score: {score}", True, COULEUR_GAMEOVER), (375, 280))
    pygame.display.update()
    pygame.time.wait(2000)
    pygame.quit()

    relancer_main()


if __name__ == "__main__":
    main()
