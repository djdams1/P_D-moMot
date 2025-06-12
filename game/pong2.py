# ETML
# Author : Damien Rochat
# Date : 06/06/2025
# Description : Jeu du pong à 2 joueurs

import pygame
import sys
import random
from pygame.locals import *
import subprocess
import os
# Initialiser pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong à 2 joueurs")

font_grande = pygame.font.Font(None, 36)  # Grande police
font_petite = pygame.font.Font(None, 18)  # Petite police


# Couleurs
BLACK = (243, 232, 238)
WHITE = (47, 6, 1)

# Vitesse des joueurs et de la balle
PLAYER_SPEED = 13
BALL_SPEED = 7

# Dimensions des joueurs et de la balle
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_SIZE = 20

# Initialisation des joueurs et de la balle
player1 = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2 = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

ball_dx, ball_dy = BALL_SPEED, BALL_SPEED

# Score
score1, score2 = 0, 0
font = pygame.font.Font(None, 74)

# Boucle principale du jeu
def main():
    
    global ball_dx, ball_dy, score1, score2
    clock = pygame.time.Clock()

    continuer = True
    while continuer:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_DELETE:
                continuer = False
                pygame.quit()
                relancer_main()
                sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()


        # Gestion des touches
        keys = pygame.key.get_pressed()

        # Contrôles du joueur 1 (W, S)
        if keys[pygame.K_w] and player1.top > 0:
            player1.y -= PLAYER_SPEED
        if keys[pygame.K_s] and player1.bottom < HEIGHT:
            player1.y += PLAYER_SPEED

        # Contrôles du joueur 2 (Flèches haut et bas)
        if keys[pygame.K_UP] and player2.top > 0:
            player2.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
            player2.y += PLAYER_SPEED

        # Déplacement de la balle
        ball.x += ball_dx
        ball.y += ball_dy

        # Collision avec le haut et le bas
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_dy = -ball_dy

        # Collision avec les joueurs
        if ball.colliderect(player1) or ball.colliderect(player2):
            ball_dx = -ball_dx

        # Si la balle sort des limites
        if ball.left <= 0:
            score2 += 1
            reset_ball()
        if ball.right >= WIDTH:
            score1 += 1
            reset_ball()

        # Dessiner le terrain
        WINDOW.fill(BLACK)
        pygame.draw.rect(WINDOW, WHITE, player1)
        pygame.draw.rect(WINDOW, WHITE, player2)
        pygame.draw.ellipse(WINDOW, WHITE, ball)
        pygame.draw.aaline(WINDOW, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        # Afficher le score
        text1 = font.render(str(score1), True, WHITE)
        text2 = font.render(str(score2), True, WHITE)
        WINDOW.blit(text1, (WIDTH // 4, 20))
        WINDOW.blit(text2, (WIDTH * 3 // 4, 20))

        # Rafraîchir l'écran
        pygame.display.flip()
        clock.tick(60)
def relancer_main():
    # Détecte si on est dans un .exe (PyInstaller)
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
        main_path = os.path.join(base_path, "main.exe")  # si compilé
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
        main_path = os.path.abspath(os.path.join(base_path, "..", "main.py"))  # si .py
    
    subprocess.run([sys.executable, main_path])
    sys.exit()

# Réinitialiser la position de la balle
def reset_ball():
    global ball_dx, ball_dy
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_dx *= -1
    ball_dy *= -1

if __name__ == "__main__":  
    main()
