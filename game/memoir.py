import pygame
import sys
import random
import os
import time
import subprocess
import math
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
DUREE_ANIMATION = 0.2  # secondes pour l'animation de retournement

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
VERT = (50, 200, 50)
ROUGE = (200, 50, 50)

# Chargement des images de cartes
def chemin_absolu_relatif(relatif):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relatif)

chemin_cartes = chemin_absolu_relatif("game/cards")

if not os.path.exists(chemin_cartes):
    raise FileNotFoundError(f"Le dossier des cartes n'existe pas : {chemin_cartes}")

cartes_faces = [f for f in os.listdir(chemin_cartes) if f.endswith(".png") and f.upper() != "BACK.PNG"]

# Sélection aléatoire de 12 cartes, puis duplication pour faire les paires
cartes_faces = random.sample(cartes_faces, 12)
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
        "trouvee": False,
        "animation_debut": 0,
        "animation_type": None  # "retourner" ou "cacher"
    })

# Dos de carte
back_image = pygame.image.load(os.path.join(chemin_cartes, "BACK.png"))
back_image = pygame.transform.scale(back_image, TAILLE_CARTE)

# Fenêtre
fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
pygame.display.set_caption("Jeu de Memory")

# Police
police = pygame.font.SysFont(None, 36)

def dessiner_carte_animee(carte, temps_actuel):
    """Dessine une carte avec animation de retournement"""
    if carte["animation_type"] is None:
        # Pas d'animation, affichage normal
        if carte["visible"] or carte["trouvee"]:
            fenetre.blit(carte["image"], carte["rect"])
        else:
            fenetre.blit(back_image, carte["rect"])
        return
    
    # Calcul du pourcentage d'animation (0 à 1)
    temps_ecoule = temps_actuel - carte["animation_debut"]
    progression = min(temps_ecoule / DUREE_ANIMATION, 1.0)
    
    # Animation terminée ?
    if progression >= 1.0:
        carte["animation_type"] = None
        if carte["visible"] or carte["trouvee"]:
            fenetre.blit(carte["image"], carte["rect"])
        else:
            fenetre.blit(back_image, carte["rect"])
        return
    
    # Calcul de l'effet de rotation (effet de retournement)
    # On fait une rotation de 0° à 180° puis de 180° à 360°
    angle = progression * math.pi  # 0 à π radians
    
    # Largeur de la carte selon l'angle (effet 3D)
    largeur_originale = TAILLE_CARTE[0]
    largeur_actuelle = int(abs(math.cos(angle)) * largeur_originale)
    
    # Éviter une largeur de 0
    if largeur_actuelle < 1:
        largeur_actuelle = 1
    
    # Déterminer quelle image afficher
    if angle < math.pi / 2:  # Première moitié : on voit encore l'image actuelle
        if carte["animation_type"] == "retourner":
            # On retourne vers la face
            image_a_afficher = back_image if not carte["visible"] else carte["image"]
        else:  # "cacher"
            # On retourne vers le dos
            image_a_afficher = carte["image"] if carte["visible"] else back_image
    else:  # Deuxième moitié : on voit la nouvelle image
        if carte["animation_type"] == "retourner":
            # On retourne vers la face
            image_a_afficher = carte["image"] if carte["visible"] else back_image
        else:  # "cacher"
            # On retourne vers le dos
            image_a_afficher = back_image if not carte["visible"] else carte["image"]
    
    # Redimensionner l'image selon la largeur calculée
    image_redimensionnee = pygame.transform.scale(image_a_afficher, (largeur_actuelle, TAILLE_CARTE[1]))
    
    # Position centrée
    x_centre = carte["rect"].centerx - largeur_actuelle // 2
    y_centre = carte["rect"].centery - TAILLE_CARTE[1] // 2
    
    # Afficher l'image animée
    fenetre.blit(image_redimensionnee, (x_centre, y_centre))

def afficher_cartes(temps_actuel):
    for carte in cartes:
        dessiner_carte_animee(carte, temps_actuel)

def afficher_infos(score, temps_restant):
    texte_score = police.render(f"Score: {score}", True, NOIR)
    texte_temps = police.render(f"Temps: {int(temps_restant)}s", True, NOIR)
    fenetre.blit(texte_score, (10, HAUTEUR_FENETRE - 40))
    fenetre.blit(texte_temps, (LARGEUR_FENETRE - 150, HAUTEUR_FENETRE - 40))

def afficher_fin(victoire, temps_restant):
    if victoire:
        temps_utilise = DUREE_JEU - int(temps_restant)
        minutes = temps_utilise // 60
        secondes = temps_utilise % 60
        texte = f"Bravo, tu as gagné ! Tu as pris {minutes:02d}:{secondes:02d}"
    else:
        texte = "Temps écoulé..."

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
    
    subprocess.run([sys.executable, main_path])
    sys.exit()

def demarrer_animation_retourner(carte, temps_actuel):
    """Démarre l'animation de retournement d'une carte"""
    carte["animation_debut"] = temps_actuel
    carte["animation_type"] = "retourner"

def demarrer_animation_cacher(carte, temps_actuel):
    """Démarre l'animation pour cacher une carte"""
    carte["animation_debut"] = temps_actuel
    carte["animation_type"] = "cacher"

def animation_en_cours():
    """Vérifie si une animation est en cours"""
    return any(carte["animation_type"] is not None for carte in cartes)

def jeu_memory():
    score = 0
    premiere_carte = None
    attente = False
    temps_attente = 0
    horloge = pygame.time.Clock()
    debut = time.time()
    continuer = True

    while continuer:
        temps_actuel = time.time()
        temps_restant = DUREE_JEU - (temps_actuel - debut)
        
        if temps_restant <= 0:
            afficher_fin(False, 0)
            return

        fenetre.fill(BLANC)
        afficher_cartes(temps_actuel)
        afficher_infos(score, temps_restant)
        pygame.display.flip()

        # Gestion de l'attente après deux cartes non-matching
        if attente and temps_actuel >= temps_attente and not animation_en_cours():
            for carte in cartes:
                if not carte["trouvee"] and carte["visible"]:
                    demarrer_animation_cacher(carte, temps_actuel)
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
            elif event.type == pygame.MOUSEBUTTONDOWN and not attente and not animation_en_cours():
                pos = pygame.mouse.get_pos()
                for carte in cartes:
                    if carte["rect"].collidepoint(pos) and not carte["visible"] and not carte["trouvee"]:
                        carte["visible"] = True
                        demarrer_animation_retourner(carte, temps_actuel)
                        
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
                                temps_attente = temps_actuel + TEMPS_RETOUR + DUREE_ANIMATION
                        break

        if all(c["trouvee"] for c in cartes):
            afficher_fin(True, temps_restant)
            return

        horloge.tick(60)  # Augmenté à 60 FPS pour des animations plus fluides

if __name__ == "__main__":
    jeu_memory()