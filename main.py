import pygame
from pygame.locals import *
from game import pongbot

pygame.init()
fenetre = pygame.display.set_mode((640, 400))
pygame.display.set_caption("Lobby Game")

font_grande = pygame.font.Font(None, 36)  # Grande police
font_petite = pygame.font.Font(None, 18)  # Petite police

couleur_texte_normal = (47, 6, 1)  # noir
couleur_texte_survol = (34, 87, 122)  # bleu

# Textes
textes = [
    "Bienvenue dans le lobby",
    "Pierre-Papier-Ciseaux",
    "Snake",
    "Pong",
    "Tetris",
    "Morpion",
    "Pendu",
    "BlackJack",
    "Memoir",
    "Jeux aléatoires"
]

# Position de chaque texte
positions = [
    (155, 10),
    (155, 100),
    (155, 130),
    (155, 160),
    (155, 190),
    (155, 220),
    (155, 250),
    (155, 280),
    (155, 310),
    (155, 370)
]

continuer = True

fenetre.fill((243, 232, 238))
pygame.display.flip()


def main():
    global fenetre  # Assurer l'utilisation de la variable globale fenetre
    global continuer
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
                if pygame.mouse.get_pressed()[0]:
                    texte_clique = texte

                    if texte == "Pierre-Papier-Ciseaux":
                        
                        pygame.display.set_mode((800, 600))
                        # pongbot.main() 
                        print("PFC") 
                        continuer = True  

                    if texte == "Snake":
                        
                        pygame.display.set_mode((800, 600))
                        # pongbot.main()  
                        print("Snake")
                        continuer = True

                    if texte == "Pong":
                        
                        pygame.display.set_mode((800, 600))
                        pongbot.main()  
                        continuer = False  

                    if texte == "Tetris":
                        
                        pygame.display.set_mode((800, 600))
                        # pongbot.main()  
                        print("Tetris")
                        continuer = True  

                    if texte == "Morpion":
                        
                        pygame.display.set_mode((800, 600))
                        # pongbot.main()  
                        print("Morpion")
                        continuer = True  

                    if texte == "Pendu":
                        
                        pygame.display.set_mode((800, 600))
                        # pongbot.main()  
                        print("Pendu")
                        continuer = True  

                    if texte == "BlackJack":
                        
                        pygame.display.set_mode((800, 600))
                        # pongbot.main()  
                        print("BlackJack")
                        continuer = True  

                    if texte == "Memoir":
                        
                        pygame.display.set_mode((800, 600))
                        # pongbot.main()  
                        print("Memoir")
                        continuer = True

                    if texte == "Jeux aléatoires":
                        
                        pygame.display.set_mode((800, 600))
                        # pongbot.main()  
                        print("Jeux aléatoires")
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
