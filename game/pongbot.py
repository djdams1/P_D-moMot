# ETML
# Author : Damien Rochat
# Date : 03/06/2025
# Description : Jeu du pong comptre l'ordinateur

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
pygame.display.set_caption("Pong - 1 Joueur contre l'ordinateur")

font_grande = pygame.font.Font(None, 36)  # Grande police
font_petite = pygame.font.Font(None, 18)  # Petite police

couleur_texte_normal = (47, 6, 1)  # noir
couleur_texte_survol = (34, 87, 122)  # bleu

# Couleurs
WHITE = (47, 6, 1)
BLACK = (243, 232, 238)

PLAYER_SPEED = 13
BALL_SPEED = 7
BOT_REACTION_SPEED = 4  # Vitesse de réaction du bot (très lent)
BOT_MISSED_CHANCE = 20  # Chance que le bot rate la balle, plus bas = plus de ratés
BOT_HESITATION = 15  # Chance que le bot hésite (plus bas = plus d'hésitations)
BOT_RANDOMNESS = 20  # Plus cette valeur est élevée, plus le mouvement du bot sera erratique

# Dimensions des joueurs et de la balle
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_SIZE = 20

# Initialisation du joueur et de la balle
player = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
bot = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

ball_dx, ball_dy = BALL_SPEED, BALL_SPEED

# Score
score_player, score_bot = 0, 0
font = pygame.font.Font(None, 74)

# Boucle principale du jeu
def main():

    continuer = True
    WINDOW.blit(font_petite.render("Touche DELETE pour revenir au lobby", True, (245, 133, 73)), (155, 40))
    global ball_dx, ball_dy, score_player, score_bot
    clock = pygame.time.Clock()

    while continuer:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_DELETE:
                
                pygame.quit()
                relancer_main()
                sys.exit()
            elif event.type == pygame.QUIT:
                continuer = False
                pygame.quit()
                sys.exit()

        # Gestion des touches (le joueur)
        keys = pygame.key.get_pressed()

        # Contrôles du joueur (W, S)
        if keys[pygame.K_w] and player.top > 0:
            player.y -= PLAYER_SPEED
        if keys[pygame.K_s] and player.bottom < HEIGHT:
            player.y += PLAYER_SPEED

       
        if random.randint(0, BOT_MISSED_CHANCE) == 0:  
            bot.y += random.choice([-1, 1]) * random.randint(1, BOT_REACTION_SPEED)  

        
        if random.randint(0, BOT_HESITATION) == 0:
            bot.y += random.choice([-1, 1]) * random.randint(1, BOT_REACTION_SPEED)  
        
        if ball.centerx > WIDTH // 2:  
            
            if random.randint(0, BOT_RANDOMNESS) == 0:  
                bot.y += random.choice([-1, 1]) * random.randint(1, BOT_REACTION_SPEED)  

            # Le bot suit la balle (mais très lentement et aléatoirement)
            if bot.centery < ball.centery and bot.bottom < HEIGHT:
                bot.y += BOT_REACTION_SPEED  
            elif bot.centery > ball.centery and bot.top > 0:
                bot.y -= BOT_REACTION_SPEED  

        # Déplacement de la balle
        ball.x += ball_dx
        ball.y += ball_dy

        # Collision avec le haut et le bas
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_dy = -ball_dy

        # Collision avec les joueurs
        if ball.colliderect(player) or ball.colliderect(bot):
            ball_dx = -ball_dx

        # Si la balle sort des limites
        if ball.left <= 0:
            score_bot += 1
            reset_ball()
        if ball.right >= WIDTH:
            score_player += 1
            reset_ball()

        # Dessiner le terrain
        WINDOW.fill(BLACK)
        pygame.draw.rect(WINDOW, WHITE, player)
        pygame.draw.rect(WINDOW, WHITE, bot)
        pygame.draw.ellipse(WINDOW, WHITE, ball)
        pygame.draw.aaline(WINDOW, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        # Afficher le score
        text_player = font.render(str(score_player), True, WHITE)
        text_bot = font.render(str(score_bot), True, WHITE)
        WINDOW.blit(text_player, (WIDTH // 4, 20))
        WINDOW.blit(text_bot, (WIDTH * 3 // 4, 20))

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
