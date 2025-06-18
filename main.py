# ETML
# Author : Damien Rochat
# Date : 02/06/2025
# Description : Système de lancement des jeux par interface graphique

import pygame
import os
import sys
import random
from pygame.locals import *
from game import pongbot, fpc, morpoin, pendu, blackjack, tetris, pong2, memoir, snak

pygame.init()
fenetre = pygame.display.set_mode((640, 550))
pygame.display.set_caption("Lobby Game")

font_grande = pygame.font.SysFont('Century Gothic', 33)
font_petite = pygame.font.SysFont('Century Gothic', 18)

couleur_texte_normal = (47, 6, 1)
couleur_texte_survol = (34, 87, 122)

textes = [
    "Bienvenue dans le lobby",
    "Shi-Fu-Mi", "Snake", "Pong", "Pong 1V1", "Tetris",
    "Morpion", "Pendu", "BlackJack", "Memoir",
    "Jeux aléatoires", "Quitter"
]

positions = [
    (120, 10), (120, 100), (120, 130), (120, 160), (120, 190),
    (120, 220), (120, 250), (120, 280), (120, 310), (120, 340),
    (120, 450), (120, 480)
]

index_selection = 1
continuer = True

def lancer_jeu(index):
    pygame.display.set_mode((800, 600))
    if index == 1: fpc.main()
    elif index == 2: snak.main()
    elif index == 3: pongbot.main()
    elif index == 4: pong2.main()
    elif index == 5: tetris.main()
    elif index == 6: morpoin.main()
    elif index == 7: pendu.main()
    elif index == 8: blackjack.main()
    elif index == 9:
        pygame.display.set_mode((800, 800))
        memoir.jeu_memory()
    elif index == 10:
        return random.randint(1, 9)
    elif index == 11:
        fenetre = pygame.display.set_mode((640, 550))
        fenetre.fill((243, 232, 238))

        texte1 = font_grande.render("Merci d'avoir joué", True, (200, 0, 0))
        texte2 = font_petite.render("La fenêtre va se fermer", True, (200, 0, 0))
        fenetre.blit(texte1, (320 - texte1.get_width() // 2, 250))
        fenetre.blit(texte2, (320 - texte2.get_width() // 2, 285))

        pygame.display.update()  # ← Important pour afficher avant d'attendre
        pygame.time.wait(3000)

        pygame.quit()
        sys.exit()
    return 0  # Reset `select` après

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def main():
    global index_selection, continuer

    try:
        logo_path = resource_path("textures/logo.png")
        logo = pygame.image.load(logo_path)
        pygame.display.set_icon(logo)
    except Exception as e:
        print(f"Logo non trouvé ou erreur de chargement : {e}")

    select = 0

    while continuer:
        fenetre.fill((243, 232, 238))
        pos_souris = pygame.mouse.get_pos()
        # Juste avant la boucle, ajoute :
        survol_index = None
        for i, (texte, position) in enumerate(zip(textes, positions)):
            if i == 0:
                continue  # On skip le titre
            texte_surface = font_grande.render(texte, True, (0, 0, 0))
            rect = texte_surface.get_rect(topleft=position)
            if rect.collidepoint(pos_souris):
                survol_index = i
                break



        

        for i, (texte, position) in enumerate(zip(textes, positions)):
            if i == 0:
                couleur_texte = couleur_texte_normal
            elif i == survol_index:
                couleur_texte = couleur_texte_survol
            elif i == index_selection and survol_index is None:
                couleur_texte = couleur_texte_survol

            else:
                couleur_texte = couleur_texte_normal

            fenetre.blit(font_grande.render(texte, True, couleur_texte), position)

        fenetre.blit(font_petite.render("Touche DELETE pour quitter", True, (245, 133, 73)), (120, 40))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                continuer = False
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_DELETE:
                    continuer = False
                    pygame.quit()
                    sys.exit()
                elif event.key == K_DOWN:
                    index_selection += 1
                    if index_selection >= len(textes) :
                        index_selection = 1
                elif event.key == K_UP:
                    index_selection -= 1
                    if index_selection < 1:
                        index_selection = len(textes) - 1
                elif event.key == K_RETURN:
                    select = index_selection
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                for i, (_, position) in enumerate(zip(textes, positions)):
                    if i != 0 and position[1] <= pos_souris[1] <= position[1] + 30:
                        select = i

        if select != 0:
            select = lancer_jeu(select)

if __name__ == "__main__":
    main()
