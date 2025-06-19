# ETML
# Author : Damien Rochat
# Date : 19/06/2025
# Description : Shi-Fu-Mi sans image mais propre et animé

import pygame
import sys
import random
import os
import subprocess

# Init
pygame.init()
WIDTH, HEIGHT = 840, 500
fenetre = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shi-Fu-Mi")

# Couleurs
COUL_FOND = (243, 232, 238)
COUL_BOUTON = (253, 242, 248)
COUL_TEXTE = (47, 6, 1)
COUL_RESULTAT = (47, 6, 1)

# Fonts
font_grande = pygame.font.SysFont('Century Gothic', 40)
font_moyenne = pygame.font.SysFont('Century Gothic', 28)
font_petite = pygame.font.SysFont('Century Gothic', 20)

# Choix
CHOIX = ["Kayou", "Papier", "Ciseaux"]
rects = {
    "Kayou": pygame.Rect(120, 180, 180, 80),
    "Papier": pygame.Rect(330, 180, 180, 80),
    "Ciseaux": pygame.Rect(540, 180, 180, 80),
}
zone_resultat = pygame.Rect(0, 90, WIDTH, 40)

def afficher_texte_centre(texte, font, couleur, y):
    surf = font.render(texte, True, couleur)
    rect = surf.get_rect(center=(WIDTH // 2, y))
    fenetre.blit(surf, rect)

def dessiner_interface():
    fenetre.fill(COUL_FOND)
    afficher_texte_centre("Shi-Fu-Mi", font_grande, COUL_TEXTE, 40)
    afficher_texte_centre("Touche DELETE pour quitter", font_petite, COUL_RESULTAT, 70)

    for nom, rect in rects.items():
        pygame.draw.rect(fenetre, COUL_BOUTON, rect, border_radius=12)
        texte = font_moyenne.render(nom, True, COUL_TEXTE)
        texte_rect = texte.get_rect(center=rect.center)
        fenetre.blit(texte, texte_rect)

def animation_rebours():
    for chiffre in ["1", "2", "3"]:
        pygame.draw.rect(fenetre, COUL_FOND, zone_resultat)
        afficher_texte_centre(chiffre, font_grande, COUL_TEXTE, 110)
        pygame.display.flip()
        pygame.time.wait(400)

def afficher_resultat(msg):
    pygame.draw.rect(fenetre, COUL_FOND, zone_resultat)
    afficher_texte_centre(msg, font_petite, COUL_RESULTAT, 110)
    pygame.display.flip()

def checkwin(choix_joueur):
    choix_pc = random.choice(CHOIX)
    print(f"Vous : {choix_joueur}, AI : {choix_pc}")

    if choix_joueur == choix_pc:
        afficher_resultat(f"Égalité ! AI : {choix_pc}")
    elif (choix_joueur == "Kayou" and choix_pc == "Ciseaux") or \
         (choix_joueur == "Papier" and choix_pc == "Kayou") or \
         (choix_joueur == "Ciseaux" and choix_pc == "Papier"):
        afficher_resultat(f"Gagné ! AI : {choix_pc}")
    else:
        afficher_resultat(f"Perdu ! AI : {choix_pc}")

def relancer_main():
    if getattr(sys, 'frozen', False):
        path = os.path.join(os.path.dirname(sys.executable), "main.exe")
    else:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "main.py"))
    subprocess.run([sys.executable, path])
    sys.exit()

def main():
    continuer = True
    dessiner_interface()
    pygame.display.flip()

    while continuer:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    pygame.quit()
                    relancer_main()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for nom, rect in rects.items():
                    if rect.collidepoint(pos):
                        animation_rebours()
                        checkwin(nom)
                        break

        pygame.display.update()

if __name__ == "__main__":
    main()
