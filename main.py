import pygame
from pygame.locals import *
from game import pongbot
from game import fpc
from game import morpoin
from game import pendu
from game import blackjack
from game import tetris
from game import pong2
from game import memoir

import random


pygame.init()
fenetre = pygame.display.set_mode((640, 500))
pygame.display.set_caption("Lobby Game")

font_grande = pygame.font.SysFont('Century Gothic', 33)
font_petite = pygame.font.SysFont('Century Gothic', 18)  # Petite police

couleur_texte_normal = (47, 6, 1)  # noir
couleur_texte_survol = (34, 87, 122)  # bleu

# Textes
textes = [
    "Bienvenue dans le lobby",
    "Shi-Fu-Mi",
    "Snake",
    "Pong",
    "Pong 1V1",
    "Tetris",
    "Morpion",
    "Pendu",
    "BlackJack",
    "Memoir",
    "Jeux aléatoires"
]

CHOIX = [
    "Pierre-Papier-Ciseaux",
    "Snake",
    "Pong",
    "Pong1V1",
    "Tetris",
    "Morpion",
    "Pendu",
    "BlackJack",
    "Memoir"
    ]

# Position de chaque texte
positions = [
    (120, 10),
    (120, 100),
    (120, 130),
    (120, 160),
    (120, 190),
    (120, 220),
    (120, 250),
    (120, 280),
    (120, 310),
    (120, 340),
    (120, 450)
]

continuer = True

fenetre.fill((243, 232, 238))
pygame.display.flip()


def main():
    logo = pygame.image.load("textures/logo.png")  # Assurez-vous que le fichier existe
    pygame.display.set_icon(logo)

    global fenetre  # Assurer l'utilisation de la variable globale fenetre
    global continuer
    select = 0
    # Boucle infinie du lobby
    while continuer:
        fenetre.fill((243, 232, 238))

        # Récupérer la position de la souris
        pos_souris = pygame.mouse.get_pos()

        # Affichage du texte avec survol
        for i, (texte, position) in enumerate(zip(textes, positions)):

            if i == 0:
                couleur_texte = couleur_texte_normal
            else:
                # Créer l'objet texte
                if position[1] <= pos_souris[1] <= position[1] + 20:

                    couleur_texte = couleur_texte_survol
                else:
                    couleur_texte = couleur_texte_normal

            # Afficher le texte
            fenetre.blit(font_grande.render(texte, True, couleur_texte), position)

            # Séction pour exécuter les mini-jeux en fonction de où est la souris
            if position[1] <= pos_souris[1] <= position[1] + 20 and couleur_texte == couleur_texte_survol:
                if pygame.mouse.get_pressed()[0] or select != 0:
                    

                    if texte == "Shi-Fu-Mi" or select == 1:
                        
                        pygame.display.set_mode((800, 600))
                        fpc.main() 
                        continuer = False  

                    if texte == "Snake" or select == 2:
                        
                        pygame.display.set_mode((800, 600))
                        # pongbot.main()  
                        print("Snake")
                        continuer = True

                    if texte == "Pong" or select == 3:
                        
                        pygame.display.set_mode((800, 600))
                        pongbot.main()  
                        continuer = False  

                    if texte == "Tetris" or select == 4:
                        
                        pygame.display.set_mode((800, 600))
                        tetris.main()  
                        continuer = True  

                    if texte == "Morpion" or select == 5:
                        
                        pygame.display.set_mode((800, 600))
                        morpoin.main()  
                        continuer = False  

                    if texte == "Pendu" or select == 6:
                        pygame.display.set_mode((800, 600))
                        pendu.main()  
                        continuer = False  

                    if texte == "BlackJack" or select == 7:
                        
                        pygame.display.set_mode((800, 600))
                        blackjack.main()  
                        
                        continuer = False  

                    if texte == "Memoir" or select == 8:
                        
                        pygame.display.set_mode((800, 800))
                        memoir.jeu_memory()  
                        
                        continuer = False

                    if texte == "Pong 1V1" or select == 9:
                        
                        pygame.display.set_mode((800, 600))
                        pong2.main()  
                        
                        continuer = True

                    if texte == "Jeux aléatoires":
                        
                        select = random.uniform(0, 9)
                        select = round(select)
                        print(select)
                        continuer = True


        fenetre.blit(font_petite.render("Touche DELETE pour quitter", True, (245, 133, 73)), (155, 40))

        pygame.display.update()

        # Événements
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_DELETE or event.type == pygame.QUIT:
                continuer = False
                pygame.quit()


if __name__ == "__main__":
    main()
