# ETML
# Author : Damien Rochat
# Date : 10/06/2025
# Description : Jeux de Snake sur toute la fenêtre

import pygame
import sys
import random
from pygame.locals import *
import subprocess
import os

pygame.init()

font_grande = pygame.font.Font(None, 36)
font_petite = pygame.font.Font(None, 18)

couleur_texte_normal = (47, 6, 1)
couleur_texte_survol = (34, 87, 122)

fenetre = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

TILE_SIZE = 20
NB_TILES_X = 800 // TILE_SIZE
NB_TILES_Y = 600 // TILE_SIZE

def main():
    snake = [(5, 5)]
    direction = (1, 0)
    apple = (random.randint(0, NB_TILES_X - 1), random.randint(0, NB_TILES_Y - 1))
    score = 0
    continuer = True

    while continuer:
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

        # Move snake
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        if (
            head in snake
            or head[0] < 0
            or head[1] < 0
            or head[0] >= NB_TILES_X
            or head[1] >= NB_TILES_Y
        ):
            continuer = False  # Game Over

        snake.insert(0, head)

        if head == apple:
            score += 1
            apple = (random.randint(0, NB_TILES_X - 1), random.randint(0, NB_TILES_Y - 1))
        else:
            snake.pop()

        # Draw
        fenetre.fill((243, 232, 238))
        fenetre.blit(font_grande.render("Snake Game", True, couleur_texte_normal), (155, 10))
        fenetre.blit(font_petite.render("Touche DELETE pour revenir au lobby", True, (245, 133, 73)), (155, 40))
        fenetre.blit(font_petite.render(f"Score: {score}", True, couleur_texte_survol), (10, 570))

        # Draw apple
        pygame.draw.rect(fenetre, (255, 0, 0), (apple[0]*TILE_SIZE, apple[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))

        # Draw snake
        for segment in snake:
            pygame.draw.rect(fenetre, (0, 255, 0), (segment[0]*TILE_SIZE, segment[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))

        pygame.display.update()
        clock.tick(10)

    # Afficher "Game Over"
    fenetre.blit(font_grande.render("Game Over", True, (200, 0, 0)), (320, 250))
    pygame.display.update()
    pygame.time.wait(2000)
    pygame.quit()
    relancer_main()

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
