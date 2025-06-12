# ETML
# Author : Damien Rochat
# Date : 03/06/2025
# Description : Jeu du Morpion à 2 joueurs

import pygame
import sys
import subprocess
from pygame.locals import *
import os

# Initialisation
pygame.init()

# Fenêtre
WIDTH, HEIGHT = 800, 600
fenetre = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Morpion")

# Polices et couleurs
font_grande = pygame.font.SysFont('Century Gothic', 33)
font_petite = pygame.font.SysFont('Century Gothic', 18)

# Couleurs
COULEUR_TEXTE = (47, 6, 1)       # Couleur texte et symboles
COULEUR_FOND = (243, 232, 238)   # Couleur fond

# Grille
largeur_case = 100
hauteur_case = 100
epaisseur_ligne = 4
marge_x = (WIDTH - 3 * largeur_case) // 2
marge_y = 100

def dessiner_grille():
    # Lignes verticales
    for i in range(1, 3):
        x = marge_x + i * largeur_case
        pygame.draw.line(fenetre, COULEUR_TEXTE, (x, marge_y), (x, marge_y + 3 * hauteur_case), epaisseur_ligne)

    # Lignes horizontales
    for i in range(1, 3):
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
                # Croix
                pygame.draw.line(fenetre, COULEUR_TEXTE,
                                 (centre_x - largeur_case//2 + decalage, centre_y - hauteur_case//2 + decalage),
                                 (centre_x + largeur_case//2 - decalage, centre_y + hauteur_case//2 - decalage), 5)
                pygame.draw.line(fenetre, COULEUR_TEXTE,
                                 (centre_x + largeur_case//2 - decalage, centre_y - hauteur_case//2 + decalage),
                                 (centre_x - largeur_case//2 + decalage, centre_y + hauteur_case//2 - decalage), 5)
            elif symbole == 'O':
                # Cercle
                pygame.draw.circle(fenetre, COULEUR_TEXTE, (centre_x, centre_y), largeur_case//2 - decalage, 5)

def update_clic(tour, ligne, colonne, plateau):
    if plateau[ligne][colonne] is None:
        plateau[ligne][colonne] = 'X' if tour % 2 == 0 else 'O'
        return True
    return False

def checkwin(plateau):
    # Vérifier les lignes
    for ligne in range(3):
        if plateau[ligne][0] is not None and plateau[ligne][0] == plateau[ligne][1] == plateau[ligne][2]:
            return plateau[ligne][0]

    # Vérifier les colonnes
    for col in range(3):
        if plateau[0][col] is not None and plateau[0][col] == plateau[1][col] == plateau[2][col]:
            return plateau[0][col]

    # Vérifier diagonales
    if plateau[0][0] is not None and plateau[0][0] == plateau[1][1] == plateau[2][2]:
        return plateau[0][0]

    if plateau[0][2] is not None and plateau[0][2] == plateau[1][1] == plateau[2][0]:
        return plateau[0][2]

    # Pas de gagnant
    return None


def main():
    plateau = [[None, None, None],
               [None, None, None],
               [None, None, None]]
    tour = 0
    continuer = True
    gagnant = None
    temps_fin = 0  # pour gérer le délai après victoire

    while continuer:
        fenetre.fill(COULEUR_FOND)

        # Texte
        fenetre.blit(font_grande.render("Morpion", True, COULEUR_TEXTE), (155, 10))
        fenetre.blit(font_petite.render("Touche DELETE pour revenir au lobby", True, (245, 133, 73)), (155, 40))

        dessiner_grille()
        dessiner_symboles(plateau)

        # Si un joueur a gagné, afficher message
        if gagnant is not None:
            texte_gagnant = font_grande.render(f"Le joueur {gagnant} a gagné !", True, COULEUR_TEXTE)
            fenetre.blit(texte_gagnant, (155, 520))

            # Après 3 secondes, quitter ou reset
            if pygame.time.get_ticks() - temps_fin > 3000:
                pygame.quit()
                relancer_main()
                sys.exit()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                continuer = False
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_DELETE:
                pygame.quit()
                relancer_main()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and gagnant is None:  # bloquer clic si déjà gagné
                pos = pygame.mouse.get_pos()
                colonne = (pos[0] - marge_x) // largeur_case
                ligne = (pos[1] - marge_y) // hauteur_case
                if 0 <= colonne < 3 and 0 <= ligne < 3:
                    if update_clic(tour, ligne, colonne, plateau):
                        tour += 1

                        gagnant = checkwin(plateau)
                        if gagnant is not None:
                            print(f"Le joueur {gagnant} a gagné !")
                            temps_fin = pygame.time.get_ticks()  # démarre le chrono de la pause

        pygame.display.update()

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

if __name__ == "__main__":
    main()
    pygame.quit()
