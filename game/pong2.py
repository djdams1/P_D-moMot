# ETML
# Author : Damien Rochat
# Date : 19/06/2025
# Description : Pong à 2 joueurs avec compte à rebours et collisions fixées

import pygame
import sys
import random
import subprocess
import os

# Initialisation
pygame.init()
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong à 2 joueurs")

# Polices et couleurs
font_grande = pygame.font.SysFont('Century Gothic', 60)
font_score = pygame.font.SysFont(None, 74)
BLACK = (243, 232, 238)
WHITE = (47, 6, 1)

# Vitesse
PLAYER_SPEED = 10
BALL_SPEED = 7

# Dimensions
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_SIZE = 20

# Joueurs et balle
player1 = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2 = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
ball_dx, ball_dy = BALL_SPEED, BALL_SPEED

# Score
score1, score2 = 0, 0

# --- Fonctions ---
def draw():
    WINDOW.fill(BLACK)
    pygame.draw.rect(WINDOW, WHITE, player1)
    pygame.draw.rect(WINDOW, WHITE, player2)
    pygame.draw.ellipse(WINDOW, WHITE, ball)
    pygame.draw.aaline(WINDOW, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    score_text1 = font_score.render(str(score1), True, WHITE)
    score_text2 = font_score.render(str(score2), True, WHITE)
    WINDOW.blit(score_text1, (WIDTH // 4, 20))
    WINDOW.blit(score_text2, (WIDTH * 3 // 4, 20))
    pygame.display.flip()

def reset_ball():
    global ball_dx, ball_dy
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_dx = BALL_SPEED * random.choice([-1, 1])
    ball_dy = BALL_SPEED * random.choice([-1, 1])

def countdown():
    for val in ["1", "2", "3", "GO"]:
        WINDOW.fill(BLACK)
        afficher_texte(val, font_grande, HEIGHT // 2)
        pygame.display.flip()
        pygame.time.wait(700)

def afficher_texte(texte, police, y):
    txt = police.render(texte, True, WHITE)
    rect = txt.get_rect(center=(WIDTH // 2, y))
    WINDOW.blit(txt, rect)

def relancer_main():
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
        main_path = os.path.join(base_path, "main.exe")
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
        main_path = os.path.abspath(os.path.join(base_path, "..", "main.py"))
    subprocess.run([sys.executable, main_path])
    sys.exit()

# --- Boucle principale ---
def main():
    global ball_dx, ball_dy, score1, score2
    clock = pygame.time.Clock()

    # Affichage initial + décompte
    draw()
    countdown()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE:
                pygame.quit()
                relancer_main()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player1.top > 0:
            player1.y -= PLAYER_SPEED
        if keys[pygame.K_s] and player1.bottom < HEIGHT:
            player1.y += PLAYER_SPEED
        if keys[pygame.K_UP] and player2.top > 0:
            player2.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
            player2.y += PLAYER_SPEED

        # Déplacement balle
        ball.x += ball_dx
        ball.y += ball_dy

        # Collision haut/bas
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_dy *= -1

        # Collision avec raquettes (anti-glitch avec reposition)
        if ball.colliderect(player1) and ball_dx < 0:
            ball.left = player1.right
            ball_dx *= -1
        if ball.colliderect(player2) and ball_dx > 0:
            ball.right = player2.left
            ball_dx *= -1

        # Score
        if ball.left <= 0:
            score2 += 1
            reset_ball()
            countdown()
        if ball.right >= WIDTH:
            score1 += 1
            reset_ball()
            countdown()

        draw()
        clock.tick(60)

if __name__ == "__main__":
    reset_ball()
    main()
