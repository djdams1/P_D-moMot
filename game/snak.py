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

def main():
    snake = [(5, 5)]
    direction = (1, 0)
    pommes = [(random.randint(0, NB_TILES_X - 1), random.randint(0, NB_TILES_Y - 1)) for _ in range(800)]
    score = 0
    continuer = True

    while continuer:
        # Gestion des événements (clavier & fermeture)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_DELETE:
                    continuer = False
                    pygame.quit()
                    relancer_main()
                    sys.exit()
                elif event.key == K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)

        # Déplacement du snake
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # Collision : mur ou soi-même = Game Over
        if head in snake or head[0] < 0 or head[1] < 0 or head[0] >= NB_TILES_X or head[1] >= NB_TILES_Y:
            continuer = False

        snake.insert(0, head)

        # Si pomme mangée
        if head in pommes:
            score += 1
            index = pommes.index(head)
            # Générer nouvelle pomme
            while True:
                nouvelle_pomme = (random.randint(0, NB_TILES_X - 1), random.randint(0, NB_TILES_Y - 1))
                if nouvelle_pomme not in snake and nouvelle_pomme not in pommes:
                    pommes[index] = nouvelle_pomme
                    break
        else:
            snake.pop()  # Sinon on avance

        # Affichage
        fenetre.fill((243, 232, 238))
        fenetre.blit(font_grande.render("Snake Game", True, couleur_texte_normal), (155, 10))
        fenetre.blit(font_petite.render("Touche DELETE pour revenir au lobby", True, (245, 133, 73)), (155, 40))
        fenetre.blit(font_petite.render(f"Score: {score}", True, couleur_texte_survol), (10, 570))
        # pmmes
        for pomme in pommes:
            pygame.draw.rect(fenetre, (255, 0, 0), (pomme[0]*TILE_SIZE, pomme[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))
        # snake
        for segment in snake:
            pygame.draw.rect(fenetre, (109,118,91) , (segment[0]*TILE_SIZE, segment[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))

        pygame.display.update()
        clock.tick(10)

    # Affichage Game Over
    fenetre.blit(font_grande.render("Game Over", True, (200, 0, 0)), (320, 250))
    pygame.display.update()
    pygame.time.wait(2000)
    pygame.quit()
    relancer_main()

""" Redémarre le launcher après le jeu"""
def relancer_main():
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
        main_path = os.path.join(base_path, "main.exe")
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
        main_path = os.path.abspath(os.path.join(base_path, "..", "main.py"))

    subprocess.run([sys.executable, main_path])
    sys.exit()

if __name__ == "__main__":
    main()
