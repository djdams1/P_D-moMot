# ETML
# Author : Damien Rochat
# Date : 03/06/2025
# Description : Jeu du pendu avec dictionaire de 50000 mots
import pygame
import sys
import random
from pygame.locals import *
import subprocess
import os
import unicodedata
import time

# Initialiser pygame
pygame.init()

# Polices et couleurs
font_grande = pygame.font.SysFont('Century Gothic', 48)
font_moyenne = pygame.font.SysFont('Century Gothic', 36)
font_petite = pygame.font.SysFont('Century Gothic', 18)
couleur_texte_normal = (47, 6, 1)
couleur_texte_survol = (34, 87, 122)
couleur_fond = (243, 232, 238)

# Fenêtre
fenetre = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pendu")

# Nettoyage mot
def nettoyer_mot(mot):
    mot = mot.strip().split(" ")[0]
    mot = unicodedata.normalize('NFD', mot)
    mot = ''.join(c for c in mot if unicodedata.category(c) != 'Mn')
    if not mot.isalpha() or 'œ' in mot or 'Œ' in mot:
        return None
    return mot.lower()

def get_random_french_word_local():
    base_dir = os.path.dirname(__file__)
    filepath = os.path.join(base_dir, "french.txt")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lignes = f.read().splitlines()
    except FileNotFoundError:
        print(f"Fichier non trouvé : {filepath}")
        return None

    mots = []
    for ligne in lignes:
        mot = nettoyer_mot(ligne)
        if mot and 3 <= len(mot) <= 50:
            mots.append(mot)
    if not mots:
        print("Liste vide après filtrage.")
        return None
    return random.choice(mots)


def dessiner_pendu(nb_erreurs):
    x_base = 600
    y_base = 450
    
    # Base - 0 erreur
    if nb_erreurs >= 0:
        pygame.draw.line(fenetre, couleur_texte_normal, (x_base, y_base), (x_base + 100, y_base), 5)
    
    # Poteau vertical - 1 erreur
    if nb_erreurs >= 1:
        pygame.draw.line(fenetre, couleur_texte_normal, (x_base + 50, y_base), (x_base + 50, y_base - 300), 5)
    
    # Poteau horizontal - 2 erreurs
    if nb_erreurs >= 2:
        pygame.draw.line(fenetre, couleur_texte_normal, (x_base + 50, y_base - 300), (x_base + 150, y_base - 300), 5)
    
    # Corde - 3 erreurs
    if nb_erreurs >= 3:
        pygame.draw.line(fenetre, couleur_texte_normal, (x_base + 150, y_base - 300), (x_base + 150, y_base - 250), 5)
    
    # Tête - 4 erreurs
    if nb_erreurs >= 4:
        pygame.draw.circle(fenetre, couleur_texte_normal, (x_base + 150, y_base - 230), 20, 3)
    
    # Corps - 5 erreurs
    if nb_erreurs >= 5:
        pygame.draw.line(fenetre, couleur_texte_normal, (x_base + 150, y_base - 210), (x_base + 150, y_base - 150), 3)
    
    # Bras gauche - 6 erreurs
    if nb_erreurs >= 6:
        pygame.draw.line(fenetre, couleur_texte_normal, (x_base + 150, y_base - 200), (x_base + 120, y_base - 180), 3)
    
    # Bras droit - 7 erreurs
    if nb_erreurs >= 7:
        pygame.draw.line(fenetre, couleur_texte_normal, (x_base + 150, y_base - 200), (x_base + 180, y_base - 180), 3)
    
    # Jambe gauche - 8 erreurs
    if nb_erreurs >= 8:
        pygame.draw.line(fenetre, couleur_texte_normal, (x_base + 150, y_base - 150), (x_base + 120, y_base - 120), 3)
    
    # Jambe droite - 9 erreurs
    if nb_erreurs >= 9:
        pygame.draw.line(fenetre, couleur_texte_normal, (x_base + 150, y_base - 150), (x_base + 180, y_base - 120), 3)

def afficher_mot_cache(mot, lettres_trouvees):
    affichage = ""
    for lettre in mot:
        if lettre in lettres_trouvees:
            affichage += lettre + " "
        else:
            affichage += "_ "
    return affichage.strip()

def stopgame(message_fin):
    fenetre.blit(font_moyenne.render(message_fin, True, (200, 0, 0)), (50, 300))
    pygame.display.update()
    pygame.time.wait(3000)  # pause 3 secondes
    pygame.quit()
    subprocess.run(["python", ".//main.py"])
    sys.exit()

def main():
    mot = get_random_french_word_local()
    if not mot:
        print("Erreur : mot introuvable, ferme le programme.")
        pygame.quit()
        sys.exit()

    lettres_trouvees = set()
    lettres_ratees = set()
    max_erreurs = 9
    nb_erreurs = 0

    continuer = True
    message_fin = None

    while continuer:
        fenetre.fill(couleur_fond)

        # Titres
        fenetre.blit(font_grande.render("Pendu", True, couleur_texte_normal), (155, 10))
        fenetre.blit(font_petite.render("Touche DELETE pour revenir au lobby", True, (245, 133, 73)), (155, 50))

        # Afficher mot caché
        mot_cache = afficher_mot_cache(mot, lettres_trouvees)
        texte_mot = font_moyenne.render(mot_cache, True, couleur_texte_normal)
        fenetre.blit(texte_mot, (155, 150))

        # Afficher lettres ratées
        texte_erreurs = font_petite.render("Lettres ratées : " + " ".join(sorted(lettres_ratees)), True, (255, 0, 0))
        fenetre.blit(texte_erreurs, (155, 200))

        # Dessiner le pendu selon erreurs
        dessiner_pendu(nb_erreurs)

        # Si partie terminée, afficher message
        if message_fin:
            texte_fin = font_grande.render(message_fin, True, (200, 0, 0))
            fenetre.blit(texte_fin, (155, 300))

        for event in pygame.event.get():
            if event.type == QUIT:
                continuer = False
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_DELETE:
                    pygame.quit()
                    relancer_main()
                    sys.exit()

                # Si partie en cours et une lettre (a-z)
                if message_fin is None:
                    if event.unicode.isalpha() and len(event.unicode) == 1:
                        lettre = event.unicode.lower()
                        if lettre in lettres_trouvees or lettre in lettres_ratees:
                            # lettre déjà proposée, ignore
                            pass
                        elif lettre in mot:
                            lettres_trouvees.add(lettre)
                            # Victoire ?
                            if all(l in lettres_trouvees for l in mot):
                                message_fin = "Bravo, vous avez gagné !"
                                # Redessine le mot complet avant de quitter
                                fenetre.fill(couleur_fond)
                                fenetre.blit(font_grande.render("Pendu", True, couleur_texte_normal), (155, 10))
                                mot_cache = afficher_mot_cache(mot, lettres_trouvees)
                                texte_mot = font_moyenne.render(mot_cache, True, couleur_texte_normal)
                                fenetre.blit(texte_mot, (155, 150))
                                dessiner_pendu(nb_erreurs)
                                pygame.display.update()
                                pygame.time.wait(500)  # petite pause pour que ça se voie
                                stopgame(message_fin)

                        elif lettre not in mot:
                            lettres_ratees.add(lettre)
                            nb_erreurs += 1
                            if nb_erreurs >= max_erreurs:
                                lettres_trouvees.update(set(mot))  # Pour afficher le mot entier
                                message_fin = f"Perdu ! Le mot était : {mot}"
                                fenetre.fill(couleur_fond)
                                fenetre.blit(font_moyenne.render("Pendu", True, couleur_texte_normal), (155, 10))
                                mot_cache = afficher_mot_cache(mot, lettres_trouvees)
                                texte_mot = font_moyenne.render(mot_cache, True, couleur_texte_normal)
                                fenetre.blit(texte_mot, (155, 150))
                                dessiner_pendu(nb_erreurs)
                                pygame.display.update()
                                pygame.time.wait(500)  # petite pause pour bien voir le pendu complet
                                stopgame(message_fin)


                                
                                

        pygame.display.update()

    pygame.quit()

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
