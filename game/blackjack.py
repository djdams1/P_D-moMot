import pygame
import sys
import random
from pygame.locals import *
import subprocess
import os

pygame.init()

# Polices
font_grande = pygame.font.Font(None, 36)  # Grande police
font_petite = pygame.font.Font(None, 18)  # Petite police

couleur_texte_normal = (47, 6, 1)  # noir
couleur_texte_survol = (34, 87, 122)  # bleu

fenetre = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Blackjack")

# Variables globales du jeu
yourcash = 1000
mise = 0
deck = []
your_hand = []
dealer_hand = []
yourAceCount = 0
dealerAceCount = 0
yourSum = 0
dealerSum = 0
hidden_card = ""
canHit = True
game_over = False
message = ""

card_images = {}
back_image = None  # Ajouté


def load_card_images():
    global card_images, back_image
    card_folder = "game/cards"

    if not os.path.exists(card_folder):
        print(f"❌ Le dossier '{card_folder}' n'existe pas !")
        return

    for value in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
        for suit in ["C", "D", "H", "S"]:
            name = f"{value}-{suit}"
            path = os.path.join(card_folder, f"{name}.png")
            if os.path.isfile(path):
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, (71, 96))
                card_images[name] = img
            else:
                print(f"⚠️ Image manquante : {name}.png")

    # Charger le dos de carte
    back_path = os.path.join(card_folder, "back.png")
    if os.path.isfile(back_path):
        back_image = pygame.image.load(back_path).convert_alpha()
        back_image = pygame.transform.scale(back_image, (71, 96))
    else:
        print("⚠️ Aucune image de dos de carte trouvée (back.png)")
        back_image = pygame.Surface((71, 96))
        back_image.fill((50, 50, 50))

load_card_images()


def build_deck():
    global deck
    values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    types = ["C", "D", "H", "S"]  # Clubs, Diamonds, Hearts, Spades
    deck = [f"{v}-{t}" for t in types for v in values]
    random.shuffle(deck)

def get_value(card):

    val = card.split("-")[0]
    if val in ["J", "Q", "K"]:
        return 10
    elif val == "A":
        return 11
    else:
        # Convertir la valeur en entier, par ex '9' -> 9
        return int(val)

def check_ace(card):
    
    val = card.split("-")[0]
    return 1 if val == "A" else 0

def reduce_ace(total, ace_count):
    
    while total > 21 and ace_count > 0:
        total -= 10
        ace_count -= 1
    return total

def draw_card():
    
    global deck
    if len(deck) == 0:
        build_deck()
    return deck.pop()

def start_game():
    global your_hand, dealer_hand, yourSum, dealerSum, yourAceCount, dealerAceCount, hidden_card, canHit, message, game_over

    build_deck()
    your_hand = []
    dealer_hand = []
    yourAceCount = 0
    dealerAceCount = 0
    yourSum = 0
    dealerSum = 0
    message = ""
    game_over = False
    canHit = True

    # Distribution des cartes
    your_hand.append(draw_card())
    your_hand.append(draw_card())
    dealer_hand.append(draw_card())
    hidden_card = draw_card()

    # Calcul du total du joueur
    for c in your_hand:
        yourSum += get_value(c)
        yourAceCount += check_ace(c)
    yourSum = reduce_ace(yourSum, yourAceCount)

    # Calcul du total du dealer (carte visible uniquement)
    dealerSum += get_value(dealer_hand[0])
    dealerAceCount += check_ace(dealer_hand[0])
    dealerSum = reduce_ace(dealerSum, dealerAceCount)

def hit():
    global yourSum, yourAceCount, canHit, game_over
    if canHit and not game_over:
        card = draw_card()

        your_hand.append(card)
        update_your_sum()

        if yourSum > 21:
            canHit = False
            stay()
def update_your_sum():
    global yourSum, yourAceCount
    yourSum = 0
    yourAceCount = 0
    for c in your_hand:
        yourSum += get_value(c)
        yourAceCount += check_ace(c)
    yourSum = reduce_ace(yourSum, yourAceCount)

def stay():
    global dealerSum, dealerAceCount, yourSum, game_over, message, yourcash, mise, canHit, hidden_card

    canHit = False
    dealer_hand.append(hidden_card)
    dealerSum += get_value(hidden_card)
    dealerAceCount += check_ace(hidden_card)
    dealerSum = reduce_ace(dealerSum, dealerAceCount)

    # Dealer pioche tant qu'il est en dessous du joueur et < 22
    while dealerSum < yourSum and dealerSum < 22:
        card = draw_card()
        dealer_hand.append(card)
        dealerSum += get_value(card)
        dealerAceCount += check_ace(card)
        dealerSum = reduce_ace(dealerSum, dealerAceCount)

    # Résultat final
    if yourSum > 21:
        message = "You Lose!"
    elif dealerSum > 21 or yourSum > dealerSum:
        message = "You Win!"
        yourcash += mise * 2
    elif yourSum == dealerSum:
        message = "Tie!"
        yourcash += mise
    else:
        message = "You Lose!"

    mise = 0
    game_over = True

def draw_hand(hand, x, y, reveal_all=True):
    for i, card in enumerate(hand):
        rect_x = x + i * 80
        rect = pygame.Rect(rect_x, y, 71, 96)

        if not reveal_all and i == 1:
            fenetre.blit(back_image, (rect_x, y))
        else:
            image = card_images.get(card)
            if image:
                fenetre.blit(image, (rect_x, y))
            else:
                pygame.draw.rect(fenetre, (200, 0, 0), rect)


def draw_screen():
    
    fenetre.fill((0, 128, 0))
    fenetre.blit(font_grande.render(f"Cash: ${yourcash}", True, (255, 255, 255)), (600, 20))
    fenetre.blit(font_grande.render(f"Bet: ${mise}", True, (255, 255, 255)), (600, 60))
    fenetre.blit(font_grande.render(f"Your Total: {yourSum}", True, (255, 255, 255)), (50, 350))

    dealer_text = f"Dealer Total: {'?' if not game_over else dealerSum}"
    fenetre.blit(font_grande.render(dealer_text, True, (255, 255, 255)), (50, 50))

    draw_hand(dealer_hand + ([hidden_card] if not game_over else []), 50, 100, reveal_all=game_over)
    draw_hand(your_hand, 50, 400)

    if game_over:
        fenetre.blit(font_grande.render(message, True, (255, 255, 255)), (300, 250))
        fenetre.blit(font_petite.render("Appuyez sur R pour recommencer", True, (255, 255, 255)), (300, 300))
        
def main():
    global mise, yourcash, nextgame


    fenetre.blit(font_grande.render("Jeux Title", True, couleur_texte_normal), (155, 10))
    fenetre.blit(font_petite.render("Touche DELETE pour revenir au lobby", True, (245, 133, 73)), (155, 40))
    pygame.display.update()  
    if mise == 0:
        fenetre.blit(font_petite.render("Tu n'as plus d'argent", True, (255, 255, 255)), (300, 300))

    mise = 100
    if yourcash < mise:
        mise = yourcash
    yourcash -= mise
    start_game()

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_DELETE:
                    # Quitte ce jeu et relance main.py (le lobby)
                    
                    pygame.quit()
                    subprocess.run(["python", ".//main.py"])
                    sys.exit()
                if not game_over:
                    if event.key == K_h:
                        hit()
                    elif event.key == K_s:
                        stay()
                else:
                    if event.key == K_r and yourcash > 0:
                        mise = 100 if yourcash >= 100 else yourcash
                        yourcash -= mise
                        
                        start_game()

        draw_screen()
        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()
