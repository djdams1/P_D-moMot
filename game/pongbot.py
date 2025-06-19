# ETML
# Author : Damien Rochat
# Date : 19/06/2025
# Description : Pong contre l'ordinateur avec fix rebond + décompte

import pygame
import sys
import random
import subprocess
import os

pygame.init()

# Fenêtre
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong - 1 Joueur contre l'ordinateur")

# Polices et couleurs
font_grande = pygame.font.SysFont('Century Gothic', 60)
font_score = pygame.font.SysFont(None, 74)
font_petite = pygame.font.SysFont('Century Gothic', 18)
WHITE = (47, 6, 1)
BLACK = (243, 232, 238)

# Constantes
PLAYER_SPEED = 13
BALL_SPEED = 7
BOT_REACTION_SPEED = 4
BOT_MISSED_CHANCE = 20
BOT_HESITATION = 15
BOT_RANDOMNESS = 20

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_SIZE = 20

# Entités
player = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
bot = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
ball_dx, ball_dy = BALL_SPEED, BALL_SPEED

score_player, score_bot = 0, 0

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

def reset_ball():
    global ball_dx, ball_dy
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_dx = BALL_SPEED * random.choice([-1, 1])
    ball_dy = BALL_SPEED * random.choice([-1, 1])

def relancer_main():
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
        main_path = os.path.join(base_path, "main.exe")
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
        main_path = os.path.abspath(os.path.join(base_path, "..", "main.py"))
    subprocess.run([sys.executable, main_path])
    sys.exit()

def main():
    global ball_dx, ball_dy, score_player, score_bot
    clock = pygame.time.Clock()

    countdown()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE:
                pygame.quit()
                relancer_main()

        # Input joueur
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player.top > 0:
            player.y -= PLAYER_SPEED
        if keys[pygame.K_s] and player.bottom < HEIGHT:
            player.y += PLAYER_SPEED

        # IA Bot
        if random.randint(0, BOT_MISSED_CHANCE) == 0:
            bot.y += random.choice([-1, 1]) * random.randint(1, BOT_REACTION_SPEED)
        if random.randint(0, BOT_HESITATION) == 0:
            bot.y += random.choice([-1, 1]) * random.randint(1, BOT_REACTION_SPEED)
        if ball.centerx > WIDTH // 2:
            if random.randint(0, BOT_RANDOMNESS) == 0:
                bot.y += random.choice([-1, 1]) * random.randint(1, BOT_REACTION_SPEED)
            if bot.centery < ball.centery and bot.bottom < HEIGHT:
                bot.y += BOT_REACTION_SPEED
            elif bot.centery > ball.centery and bot.top > 0:
                bot.y -= BOT_REACTION_SPEED

        # Déplacement balle
        ball.x += ball_dx
        ball.y += ball_dy

        # Collisions haut/bas
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_dy *= -1

        # Collision avec le joueur
        if ball.colliderect(player) and ball_dx < 0:
            ball.left = player.right
            ball_dx *= -1
        # Collision avec le bot
        if ball.colliderect(bot) and ball_dx > 0:
            ball.right = bot.left
            ball_dx *= -1

        # Score
        if ball.left <= 0:
            score_bot += 1
            reset_ball()
            countdown()
        if ball.right >= WIDTH:
            score_player += 1
            reset_ball()
            countdown()

        # Affichage
        WINDOW.fill(BLACK)
        pygame.draw.rect(WINDOW, WHITE, player)
        pygame.draw.rect(WINDOW, WHITE, bot)
        pygame.draw.ellipse(WINDOW, WHITE, ball)
        pygame.draw.aaline(WINDOW, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        txt1 = font_score.render(str(score_player), True, WHITE)
        txt2 = font_score.render(str(score_bot), True, WHITE)
        WINDOW.blit(txt1, (WIDTH // 4, 20))
        WINDOW.blit(txt2, (WIDTH * 3 // 4, 20))
        # WINDOW.blit(font_petite.render("Touche DELETE pour revenir au lobby", True, (245, 133, 73)), (155, 40))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    reset_ball()
    main()
