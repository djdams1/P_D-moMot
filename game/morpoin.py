# ETML
# Author : Damien Rochat
# Date : 19/06/2025
# Description : Morpion avec ou sans bot (case à cocher + délai bot)

import pygame
import sys
import subprocess
import os
import random
from pygame.locals import *

# Init
pygame.init()
WIDTH, HEIGHT = 800, 600
fenetre = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Morpion")

# Polices et couleurs
font_grande = pygame.font.SysFont('Century Gothic', 33)
font_petite = pygame.font.SysFont('Century Gothic', 18)
COULEUR_TEXTE = (47, 6, 1)
COULEUR_FOND = (243, 232, 238)

# Grille
largeur_case, hauteur_case = 100, 100
epaisseur_ligne = 4
marge_x = (WIDTH - 3 * largeur_case) // 2
marge_y = 120

# Checkbox (centrée)
checkbox_rect = pygame.Rect(WIDTH // 2 - 150, 70, 20, 20)
jouer_contre_bot = True

# Fonctions
def dessiner_grille():
    for i in range(1, 3):
        x = marge_x + i * largeur_case
        pygame.draw.line(fenetre, COULEUR_TEXTE, (x, marge_y), (x, marge_y + 3 * hauteur_case), epaisseur_ligne)
        y = marge_y + i * hauteur_case
        pygame.draw.line(fenetre, COULEUR_TEXTE, (marge_x, y), (marge_x + 3 * largeur_case, y), epaisseur_ligne)

def dessiner_symboles(plateau):
    decalage = 20
    for ligne in range(3):
        for col in range(3):
            centre_x = marge_x + col * largeur_case + largeur_case // 2
            centre_y = marge_y + ligne * hauteur_case + hauteur_case // 2
            symbole = plateau[ligne][col]
            if symbole == 'X':
                pygame.draw.line(fenetre, COULEUR_TEXTE,
                                 (centre_x - largeur_case//2 + decalage, centre_y - hauteur_case//2 + decalage),
                                 (centre_x + largeur_case//2 - decalage, centre_y + hauteur_case//2 - decalage), 5)
                pygame.draw.line(fenetre, COULEUR_TEXTE,
                                 (centre_x + largeur_case//2 - decalage, centre_y - hauteur_case//2 + decalage),
                                 (centre_x - largeur_case//2 + decalage, centre_y + hauteur_case//2 - decalage), 5)
            elif symbole == 'O':
                pygame.draw.circle(fenetre, COULEUR_TEXTE, (centre_x, centre_y), largeur_case//2 - decalage, 5)

def checkwin(plateau):
    for ligne in range(3):
        if plateau[ligne][0] and plateau[ligne][0] == plateau[ligne][1] == plateau[ligne][2]:
            return plateau[ligne][0]
    for col in range(3):
        if plateau[0][col] and plateau[0][col] == plateau[1][col] == plateau[2][col]:
            return plateau[0][col]
    if plateau[0][0] and plateau[0][0] == plateau[1][1] == plateau[2][2]:
        return plateau[0][0]
    if plateau[0][2] and plateau[0][2] == plateau[1][1] == plateau[2][0]:
        return plateau[0][2]
    return None

def plateau_est_plein(plateau):
    return all(case is not None for ligne in plateau for case in ligne)

def bot_joue_O(plateau):
    for ligne in range(3):
        for col in range(3):
            if plateau[ligne][col] is None:
                plateau[ligne][col] = 'O'
                if checkwin(plateau) == 'O':
                    return True
                plateau[ligne][col] = None
    for ligne in range(3):
        for col in range(3):
            if plateau[ligne][col] is None:
                plateau[ligne][col] = 'X'
                if checkwin(plateau) == 'X':
                    plateau[ligne][col] = 'O'
                    return True
                plateau[ligne][col] = None
    cases_vides = [(l, c) for l in range(3) for c in range(3) if plateau[l][c] is None]
    if cases_vides:
        l, c = random.choice(cases_vides)
        plateau[l][c] = 'O'
        return True
    return False

def update_clic(tour, ligne, col, plateau):
    if plateau[ligne][col] is None:
        plateau[ligne][col] = 'X' if tour % 2 == 0 else 'O'
        return True
    return False

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
    global jouer_contre_bot
    plateau = [[None for _ in range(3)] for _ in range(3)]
    tour = 0
    gagnant = None
    continuer = True
    temps_fin = 0
    bot_pending = False
    bot_start_time = 0

    while continuer:
        fenetre.fill(COULEUR_FOND)
        fenetre.blit(font_grande.render("Morpion", True, COULEUR_TEXTE), (WIDTH // 2 - 70, 10))
        fenetre.blit(font_petite.render("Touche DELETE pour revenir au lobby", True, (245, 133, 73)), (WIDTH // 2 - 140, 40))

        # Affichage case + texte
        pygame.draw.rect(fenetre, COULEUR_TEXTE, checkbox_rect, 2)
        if jouer_contre_bot:
            pygame.draw.line(fenetre, COULEUR_TEXTE, checkbox_rect.topleft, checkbox_rect.bottomright, 2)
            pygame.draw.line(fenetre, COULEUR_TEXTE, checkbox_rect.topright, checkbox_rect.bottomleft, 2)
        fenetre.blit(font_petite.render("Jouer contre le bot", True, COULEUR_TEXTE), (checkbox_rect.right + 10, checkbox_rect.top - 2))

        dessiner_grille()
        dessiner_symboles(plateau)

        if gagnant:
            texte = "Match nul !" if gagnant == "Personne" else f"Le joueur {gagnant} a gagné !"
            fenetre.blit(font_grande.render(texte, True, COULEUR_TEXTE), (WIDTH // 2 - 150, 520))
            if pygame.time.get_ticks() - temps_fin > 3000:
                pygame.quit()
                relancer_main()

        current_time = pygame.time.get_ticks()
        if bot_pending and current_time - bot_start_time > 1500:
            if bot_joue_O(plateau):
                tour += 1
                gagnant = checkwin(plateau)
                if gagnant or plateau_est_plein(plateau):
                    temps_fin = pygame.time.get_ticks()
                    if not gagnant:
                        gagnant = "Personne"
            bot_pending = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_DELETE:
                pygame.quit()
                relancer_main()
            elif event.type == MOUSEBUTTONDOWN and not gagnant:
                pos = pygame.mouse.get_pos()
                if checkbox_rect.collidepoint(pos) and tour == 0:
                    jouer_contre_bot = not jouer_contre_bot
                else:
                    col = (pos[0] - marge_x) // largeur_case
                    lig = (pos[1] - marge_y) // hauteur_case
                    if 0 <= col < 3 and 0 <= lig < 3:
                        if update_clic(tour, lig, col, plateau):
                            tour += 1
                            gagnant = checkwin(plateau)
                            if gagnant or plateau_est_plein(plateau):
                                temps_fin = pygame.time.get_ticks()
                                if not gagnant:
                                    gagnant = "Personne"
                            elif jouer_contre_bot and tour % 2 == 1:
                                bot_pending = True
                                bot_start_time = pygame.time.get_ticks()

        pygame.display.update()

if __name__ == "__main__":
    main()
    pygame.quit()
