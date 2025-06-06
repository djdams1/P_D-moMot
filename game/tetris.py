import pygame
import sys
import random
from pygame.locals import *
import subprocess
import os

# Dimensions de la fenêtre
SCREEN_WIDTH = 450  # Augmenté pour accueillir la section de score à droite
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30


# Base : dossier actuel (tetris.py est dans /game)
BASE_DIR = os.path.dirname(__file__)  # -> D:/DemoMotold/Prod/P_D-moMot/game
TEXTURE_PATH = os.path.join(BASE_DIR, "../textures/red.png")  # remonter d’un dossier

# Normaliser le chemin
TEXTURE_PATH = os.path.normpath(TEXTURE_PATH)

# Chargement de l'image
image = pygame.image.load(TEXTURE_PATH)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RIGHT_PANEL_COLOR = (50, 50, 50)  # Couleur de fond de la partie droite
COLOR_LIST = [
    (255, 0, 0),   # Rouge V
    (0, 255, 0),   # Vert V
    (0, 0, 255),   # Bleu V
    (255, 255, 0), # Jaune V
    (255, 165, 0), # Orange V
    (0, 255, 255), # Cyan
    (128, 0, 128)  # Violet
]

# Formes de blocs
SHAPES = [
    # T-shape
    [[1, 1, 1],
     [0, 1, 0]],
    [[1, 1, 1],
     [0, 1, 0]],
    [[1, 1, 1],
     [0, 1, 0]],

    # O-shape (carré)
    [[1, 1],
     [1, 1]],
    [[1, 1],
     [1, 1]],

    # S-shape
    [[1, 1, 0],
     [0, 1, 1]],
    [[1, 1, 0],
     [0, 1, 1]],

    # Z-shape
    [[0, 1, 1],
     [1, 1, 0]],
    [[0, 1, 1],
     [1, 1, 0]],

    # L-shape
    [[1, 0, 0],
     [1, 1, 1]],
    [[1, 0, 0],
     [1, 1, 1]],
    [[1, 0, 0],
     [1, 1, 1]],

    # J-shape
    [[0, 0, 1],
     [1, 1, 1]],
    [[0, 0, 1],
     [1, 1, 1]],

    # I-shape
    [[1, 1, 1, 1]],
    [[1, 1, 1, 1]],
    [[1, 1, 1, 1]],
    [[1, 1, 1, 1]],
]


# Classe pour la gestion du jeu
# Dans la classe Tetris, lors du chargement des textures des blocs
class Tetris:
    def __init__(self):
        self.board = [[None] * 10 for _ in range(20)]  # Plateau de 20x10
        self.game_over = False
        self.score = 0
        self.current_piece = None
        self.current_position = [0, 0]
        
        # Initialisation de la prochaine pièce avant de créer la pièce initiale
        self.next_piece = random.choice(SHAPES)
        self.next_color = random.choice(COLOR_LIST)
        
        # Crée la première pièce
        self.create_piece()
        
        self.fall_speed = 500  # Temps avant que la pièce tombe
        self.last_fall_time = pygame.time.get_ticks()
        self.last_move_time = pygame.time.get_ticks()  # Temps pour gérer la répétition des actions
        self.repeat_rate = 60  # Temps avant qu'une action répétée soit exécutée
        self.move_left_pressed = False
        self.move_right_pressed = False
        self.move_down_pressed = False
        
        # Charger les textures des blocs et les redimensionner pour la section "prochaine pièce"
        self.textures = {
            (255, 0, 0): pygame.image.load("textures/red.png"),
            (0, 255, 0): pygame.image.load("textures/green.png"),
            (0, 0, 255): pygame.image.load("textures/bleu.png"),
            (255, 255, 0): pygame.image.load("textures/yellow.png"),
            (255, 165, 0): pygame.image.load("textures/orange.png"),
            (0, 255, 255): pygame.image.load("textures/cyan.png"),
            (128, 0, 128): pygame.image.load("textures/violet.png")
        }
        
        # Redimensionner les textures pour s'assurer qu'elles correspondent à la taille des blocs
        for key in self.textures:
            self.textures[key] = pygame.transform.scale(self.textures[key], (BLOCK_SIZE, BLOCK_SIZE))
        
        # Redimensionner les textures des prochaines pièces (plus petites pour l'affichage à droite)
        self.next_piece_textures = {
            (255, 0, 0): pygame.transform.scale(self.textures[(255, 0, 0)], (BLOCK_SIZE // 2, BLOCK_SIZE // 2)),
            (0, 255, 0): pygame.transform.scale(self.textures[(0, 255, 0)], (BLOCK_SIZE // 2, BLOCK_SIZE // 2)),
            (0, 0, 255): pygame.transform.scale(self.textures[(0, 0, 255)], (BLOCK_SIZE // 2, BLOCK_SIZE // 2)),
            (255, 255, 0): pygame.transform.scale(self.textures[(255, 255, 0)], (BLOCK_SIZE // 2, BLOCK_SIZE // 2)),
            (255, 165, 0): pygame.transform.scale(self.textures[(255, 165, 0)], (BLOCK_SIZE // 2, BLOCK_SIZE // 2)),
            (0, 255, 255): pygame.transform.scale(self.textures[(0, 255, 255)], (BLOCK_SIZE // 2, BLOCK_SIZE // 2)),
            (128, 0, 128): pygame.transform.scale(self.textures[(128, 0, 128)], (BLOCK_SIZE // 2, BLOCK_SIZE // 2))
        }


    def create_piece(self):
            # La pièce actuelle devient la prochaine pièce
            self.current_piece = self.next_piece
            self.current_color = self.next_color

            # Générer une nouvelle prochaine pièce
            self.next_piece = random.choice(SHAPES)
            self.next_color = random.choice(COLOR_LIST)

            # Réinitialiser la position de la pièce
            self.current_position = [0, 4]

    def rotate_piece(self):
        rotated = [list(row) for row in zip(*self.current_piece[::-1])]
        if self.valid_position(rotated, self.current_position):
            self.current_piece = rotated

    def valid_position(self, piece, pos):
        for y, row in enumerate(piece):
            for x, cell in enumerate(row):
                if cell:
                    new_x = pos[1] + x
                    new_y = pos[0] + y
                    if new_x < 0 or new_x >= 10 or new_y < 0 or new_y >= 20 or self.board[new_y][new_x] is not None:
                        return False
        return True

    def valid_move(self, dx, dy):
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.current_position[1] + x + dx
                    new_y = self.current_position[0] + y + dy
                    if new_x < 0 or new_x >= 10 or new_y >= 20 or self.board[new_y][new_x] is not None:
                        return False
        return True

    def freeze_piece(self):
        # Vérifie si la pièce peut être placée en haut
        if self.current_position[0] == 0:
            self.game_over = True
            return

        # Sinon, on place la pièce dans le plateau et on nettoie les lignes
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.current_position[1] + x
                    new_y = self.current_position[0] + y

                    # Vérification des indices hors limites
                    if new_y >= 20 or new_x < 0 or new_x >= 10:
                        continue  # Ignorer ce bloc si hors limites

                    # Placer la pièce dans le tableau si l'indice est valide
                    self.board[new_y][new_x] = self.current_color

        self.clear_lines()  # Effacer les lignes après avoir placé la pièce
        self.create_piece()


    def clear_lines(self):
        lines_cleared = 0
        i = len(self.board) - 1
        while i >= 0:
            if all(cell is not None for cell in self.board[i]):
                del self.board[i]
                self.board.insert(0, [None] * 10)
                lines_cleared += 1
                continue  # Revérifie la même ligne insérée
            i -= 1
        # Mettre à jour le score
        if lines_cleared > 0:
            self.score += lines_cleared * 100  # Ajoute 100 points par ligne supprimée
            print(f"Score increased by {lines_cleared * 100}, total score: {self.score}")
        else:
            print("No lines cleared.")
            
        

    def move_left(self):
        if self.valid_move(-1, 0):
            self.current_position[1] -= 1

    def move_right(self):
        if self.valid_move(1, 0):
            self.current_position[1] += 1

    def move_down(self):
        if self.valid_move(0, 1):
            self.current_position[0] += 1
        else:
            self.freeze_piece()  # La pièce se fige lorsqu'elle atteint le bas

    def handle_input(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time >= self.repeat_rate:
            if self.move_left_pressed:
                self.move_left()
            if self.move_right_pressed:
                self.move_right()
            if self.move_down_pressed:
                self.move_down()
            self.last_move_time = current_time

            # Vérifie que la position reste valide
            if not self.valid_position(self.current_piece, self.current_position):
                self.game_over = True

    def draw(self, screen):
        # Dessiner la partie gauche (jeu)
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell is not None:
                    screen.blit(self.textures[cell], (x * BLOCK_SIZE, y * BLOCK_SIZE))  # Affiche la texture des blocs fixes
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    screen.blit(self.textures[self.current_color], ((self.current_position[1] + x) * BLOCK_SIZE, (self.current_position[0] + y) * BLOCK_SIZE))
        
        # Dessiner la partie droite (score et Prochaine pièce)
        RIGHT_PANEL_WIDTH = 150  # Réduit la largeur de la section droite
        pygame.draw.rect(screen, RIGHT_PANEL_COLOR, (SCREEN_WIDTH - RIGHT_PANEL_WIDTH, 0, RIGHT_PANEL_WIDTH, SCREEN_HEIGHT))  # Fond de la partie droite
        
        # Police pour afficher les informations
        font = pygame.font.SysFont('Arial', 20)

        # Afficher le score
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH - RIGHT_PANEL_WIDTH + 10, SCREEN_HEIGHT // 2 - 100))

        # Afficher "Prochaine pièce"
        next_piece_text = font.render("Prochaine pièce :", True, WHITE)
        screen.blit(next_piece_text, (SCREEN_WIDTH - RIGHT_PANEL_WIDTH + 10, SCREEN_HEIGHT // 2 - 50))

        # Dessiner la prochaine pièce avec les textures redimensionnées
        if self.next_piece:
            for y, row in enumerate(self.next_piece):
                for x, cell in enumerate(row):
                    if cell:
                        x_pos = SCREEN_WIDTH - RIGHT_PANEL_WIDTH + 50 + x * (BLOCK_SIZE // 2)
                        y_pos = SCREEN_HEIGHT // 2 + y * (BLOCK_SIZE // 2)
                        screen.blit(self.next_piece_textures[self.next_color], (x_pos, y_pos))

        # Afficher "Game Over" si nécessaire
        if self.game_over:
            game_over_text = font.render("Game Over", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH - RIGHT_PANEL_WIDTH + 10, (SCREEN_HEIGHT // 2)+50 ))



    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_fall_time >= self.fall_speed:
            self.move_down()
            self.last_fall_time = current_time

    def reset(self):
        """Réinitialiser le jeu."""
        self.board = [[None] * 10 for _ in range(20)]
        self.game_over = False
        self.score = 0
        self.create_piece()
        self.last_fall_time = pygame.time.get_ticks()
        self.last_move_time = pygame.time.get_ticks()

        # Réinitialiser les inputs persistants
        self.move_left_pressed = False
        self.move_right_pressed = False
        self.move_down_pressed = False



# Fonction principale
def main():
    pygame.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    tetris = Tetris()


    # Lancer la musique de fonds
    continuer = True
    while continuer:
        if tetris.game_over:
            # Si la partie est terminée, attendre que l'utilisateur appuie sur R pour recommencer
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_DELETE:
                    continuer = False
                    pygame.quit()
                    relancer_main()
                    sys.exit()
                elif event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == KEYDOWN and event.key == K_r:
                    tetris.reset()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return  # Quitter le jeu
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        tetris.move_left_pressed = True
                    elif event.key == pygame.K_RIGHT:
                        tetris.move_right_pressed = True
                    elif event.key == pygame.K_DOWN:
                        tetris.move_down_pressed = True
                    elif event.key == pygame.K_UP:
                        tetris.rotate_piece()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        tetris.move_left_pressed = False
                    elif event.key == pygame.K_RIGHT:
                        tetris.move_right_pressed = False
                    elif event.key == pygame.K_DOWN:
                        tetris.move_down_pressed = False

            # Gestion des déplacements automatiques
            tetris.update()

            # Gérer les entrées utilisateur avec répétition contrôlée
            tetris.handle_input()

            # Rendu de l'écran
            screen.fill(BLACK)
            tetris.draw(screen)
            pygame.display.flip()

            # Limiter la vitesse du jeu
            clock.tick(60)

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
