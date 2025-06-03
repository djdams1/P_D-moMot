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
couleur_fond =(243, 232, 238)

fenetre = pygame.display.set_mode((800, 600))

fenetre.fill(couleur_fond)
pygame.display.flip()


CHOIX = ["Pierre","Papier","Ciseaux"]



pygame.draw.rect(fenetre, couleur_texte_normal,[150, 150, 70, 70])
pygame.draw.rect(fenetre, couleur_texte_normal,[250, 150, 70, 70])
pygame.draw.rect(fenetre, couleur_texte_normal,[350, 150, 70, 70])

fenetre.blit(font_petite.render("Pierre", True, couleur_fond), (165, 180))
fenetre.blit(font_petite.render("Papier", True, couleur_fond), (265, 180))
fenetre.blit(font_petite.render("Ciseaux", True, couleur_fond), (360, 180))



def main():
    fenetre.blit(font_grande.render("Pierre-Papier-Ciseaux", True, couleur_texte_normal), (155, 10))
    
    
    continuer = True
    while continuer:
        
        choix_pc = random.choice(CHOIX)
        print(choix_pc)





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
