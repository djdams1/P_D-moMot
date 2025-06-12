# ETML
# Author : Damien Rochat
# Date : 03/06/2025
# Description : jeu du Shi-Fu-Mi contre l'ordinateur

# list d'import
import pygame
import sys
import random
from pygame.locals import *
import subprocess
import os

# init la fenetre
pygame.init()
fenetre = pygame.display.set_mode((640, 500))


"""Boucle principale"""
def main():

    # deffinit les fonts
    font_grande = pygame.font.SysFont('Century Gothic', 33)
    font_petite = pygame.font.SysFont('Century Gothic', 18)  # Petite police

    # deffinit les couleures 
    couleur_texte_normal = (47, 6, 1)  # noir
    couleur_fond = (243, 232, 238)  # bleu

    CHOIX = ["Pierre", "Papier", "Ciseaux"] #choix dissponible

    # Positions des boutons
    rect_pierre = pygame.Rect(155, 150, 70, 70)
    rect_papier = pygame.Rect(255, 150, 70, 70)
    rect_ciseaux = pygame.Rect(355, 150, 70, 70)
    efface_text = pygame.Rect(150, 75, 600, 50)

    """Dessiner les boutons et texte à chaque lancement"""

    def dessiner_elements():
        fenetre.fill(couleur_fond)  # Effacer toute la fenêtre avec la couleur de fond
        pygame.draw.rect(fenetre, couleur_texte_normal, rect_pierre)
        pygame.draw.rect(fenetre, couleur_texte_normal, rect_papier)
        pygame.draw.rect(fenetre, couleur_texte_normal, rect_ciseaux)

        fenetre.blit(font_petite.render("Pierre", True, couleur_fond), (170, 180))
        fenetre.blit(font_petite.render("Papier", True, couleur_fond), (270, 180))
        fenetre.blit(font_petite.render("Ciseaux", True, couleur_fond), (365, 180))

        fenetre.blit(font_grande.render("Shi-Fu-Mi", True, couleur_texte_normal), (155, 10))
        fenetre.blit(font_petite.render("Touche DELETE pour revenir au lobby", True, (245, 133, 73)), (155, 40))

        pygame.display.flip()

    """Initialiser la fenêtre avec les éléments"""
    dessiner_elements()

    continuer = True #variable de loop

    while continuer:

        # detection du clic
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche de la souris
                pos_souris = pygame.mouse.get_pos()

                if rect_pierre.collidepoint(pos_souris):
                    choix_humain = "Pierre"
                elif rect_papier.collidepoint(pos_souris):
                    choix_humain = "Papier"
                elif rect_ciseaux.collidepoint(pos_souris):
                    choix_humain = "Ciseaux"
                else:
                    choix_humain ="Miss"
                # appelle CheckWin
                checkwin(choix_humain, fenetre, couleur_fond, efface_text, CHOIX, couleur_texte_normal, font_grande)

            # Événements pour quitté
            if event.type == KEYDOWN and event.key == K_DELETE:
                pygame.quit()
                relancer_main()
                sys.exit()
            elif event.type == pygame.QUIT:
                continuer = False
                pygame.quit()
                sys.exit()

        pygame.display.update()

    pygame.quit()

"""Permet de retrouner au lobby sasn bug"""
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
"""Sert a savoir qui gagne"""
def checkwin(choix_humain, fenetre, couleur_fond, efface_text, CHOIX, couleur_texte_normal, font_grande):
    pygame.draw.rect(fenetre, couleur_fond, efface_text)  # Effacer la zone du texte

    choix_pc = random.choice(CHOIX)

    # Debug
    print("choix Homme :" + choix_humain + " Choix PC :" + choix_pc)

    if (choix_pc == "Pierre" and choix_humain == "Pierre") or \
            (choix_pc == "Papier" and choix_humain == "Papier") or \
            (choix_pc == "Ciseaux" and choix_humain == "Ciseaux"):
        # C'est un match nul
        fenetre.blit(font_grande.render("Match nul ! l'ordinateur a choisi " + choix_pc, True, couleur_texte_normal), (155, 80))

    elif (choix_pc == "Pierre" and choix_humain == "Papier") or \
            (choix_pc == "Papier" and choix_humain == "Ciseaux") or \
            (choix_pc == "Ciseaux" and choix_humain == "Pierre"):
        # L'humain a gagné
        fenetre.blit(font_grande.render("Tu as gagné ! l'ordinateur a choisi " + choix_pc, True, couleur_texte_normal), (155, 80))

    elif (choix_pc == "Pierre" and choix_humain == "Ciseaux") or \
            (choix_pc == "Papier" and choix_humain == "Pierre") or \
            (choix_pc == "Ciseaux" and choix_humain == "Papier"):
        # L'ordinateur a gagné
        fenetre.blit(font_grande.render("L'ordinateur a gagné ! il a choisi " + choix_pc, True, couleur_texte_normal), (155, 80))
    else:
        fenetre.blit(font_grande.render("Appuies sur un des choix", True, couleur_texte_normal), (155, 80))


if __name__ == "__main__":
    main()
