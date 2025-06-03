import pygame
import sys
import random
from pygame.locals import *
import subprocess

# Initialiser pygame
pygame.init()

font_grande = pygame.font.Font(None, 36)  # Grande police
font_petite = pygame.font.Font(None, 18)  # Petite police

couleur_texte_normal = (47, 6, 1)  # noir
couleur_texte_survol = (34, 87, 122)  # bleu

fenetre = pygame.display.set_mode((800, 600))

fenetre.fill((243, 232, 238))
pygame.display.flip()


def main():
    fenetre.blit(font_grande.render("Pierre-Papier-Ciseaux", True, couleur_texte_normal), (155, 10))
    
        
    continuer = True
    while continuer:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_DELETE or event.type == pygame.QUIT:
                continuer = False  
                pygame.quit()
                subprocess.run(["python", ".//main.py"])
                sys.exit()

        pygame.display.update()  


if __name__ == "__main__":
    main()
    pygame.quit()  
