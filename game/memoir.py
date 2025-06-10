import pygame
import sys
import random
import os
import time
import subprocess
from pygame.locals import *

pygame.init()

# Constantes
LARGEUR_FENETRE = 800
HAUTEUR_FENETRE = 800
LIGNES = 4
COLONNES = 6
TAILLE_CARTE = (100, 140)
MARGE = 20
TEMPS_RETOUR = 0.5  # secondes
DUREE_JEU = 180  # secondes

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
VERT = (50, 200, 50)
ROUGE = (200, 50, 50)

# Chargement des images de cartes
def chemin_absolu_relatif(relatif):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS  # dossier temporaire utilisé par PyInstaller
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relatif)

chemin_cartes = chemin_absolu_relatif(os.path.join("game", "cards"))


cartes_faces = [f for f in os.listdir(chemin_cartes) if f.endswith(".png") and f.upper() != "BACK.PNG"]
cartes_faces = cartes_faces[:12]  # 12 paires
cartes_faces *= 2
random.shuffle(cartes_faces)

cartes = []
for i, nom in enumerate(cartes_faces):
    image = pygame.image.load(os.path.join(chemin_cartes, nom))
    image = pygame.transform.scale(image, TAILLE_CARTE)
    cartes.append({
        "nom": nom,
        "image": image,
        "rect": pygame.Rect(
            MARGE + (TAILLE_CARTE[0] + MARGE) * (i % COLONNES),
            MARGE + (TAILLE_CARTE[1] + MARGE) * (i // COLONNES),
            *TAILLE_CARTE
        ),
        "visible": False,
        "trouvee": False
    })

# Charger le dos de carte
back_image = pygame.image.load(os.path.join(chemin_cartes, "BACK.png"))
back_image = pygame.transform.scale(back_image, TAILLE_CARTE)

# Fenêtre
fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
pygame.display.set_caption("Jeu de Memory")

# Police
police = pygame.font.SysFont(None, 36)

def afficher_cartes():
    for carte in cartes:
        if carte["visible"] or carte["trouvee"]:
            fenetre.blit(carte["image"], carte["rect"])
        else:
            fenetre.blit(back_image, carte["rect"])

def afficher_infos(score, temps_restant):
    texte_score = police.render(f"Score: {score}", True, NOIR)
    texte_temps = police.render(f"Temps: {int(temps_restant)}s", True, NOIR)
    fenetre.blit(texte_score, (10, HAUTEUR_FENETRE - 40))
    fenetre.blit(texte_temps, (LARGEUR_FENETRE - 150, HAUTEUR_FENETRE - 40))

def afficher_fin(victoire):
    texte = "Bravo, tu as gagné !" if victoire else "Temps écoulé..."
    couleur = VERT if victoire else ROUGE
    message = police.render(texte, True, couleur)
    fenetre.fill(BLANC)
    fenetre.blit(message, (LARGEUR_FENETRE // 2 - message.get_width() // 2, HAUTEUR_FENETRE // 2))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    relancer_main()

def relancer_main():
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
        main_path = os.path.join(base_path, "main.exe")
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
        main_path = os.path.abspath(os.path.join(base_path, "..", "main.py"))
    
    subprocess.Popen([sys.executable, main_path])

def jeu_memory():
    score = 0
    premiere_carte = None
    attente = False
    temps_attente = 0
    horloge = pygame.time.Clock()
    debut = time.time()
    continuer = True

    while continuer:
        temps_restant = DUREE_JEU - (time.time() - debut)
        if temps_restant <= 0:
            afficher_fin(False)
            return

        fenetre.fill(BLANC)
        afficher_cartes()
        afficher_infos(score, temps_restant)
        pygame.display.flip()

        if attente and time.time() >= temps_attente:
            for carte in cartes:
                if not carte["trouvee"]:
                    carte["visible"] = False
            attente = False
            premiere_carte = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_DELETE:
                continuer = False
                pygame.quit()
                relancer_main()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not attente:
                pos = pygame.mouse.get_pos()
                for carte in cartes:
                    if carte["rect"].collidepoint(pos) and not carte["visible"] and not carte["trouvee"]:
                        carte["visible"] = True
                        if premiere_carte is None:
                            premiere_carte = carte
                        else:
                            if carte["nom"] == premiere_carte["nom"]:
                                carte["trouvee"] = True
                                premiere_carte["trouvee"] = True
                                score += 1
                                premiere_carte = None
                            else:
                                attente = True
                                temps_attente = time.time() + TEMPS_RETOUR
                        break

        if all(c["trouvee"] for c in cartes):
            afficher_fin(True)
            return

        horloge.tick(30)

# Si jamais tu veux tester en solo
if __name__ == "__main__":
    jeu_memory()
