# import pygame

# # pygame setup
# pygame.init()
# screen = pygame.display.set_mode((1280, 720))
# clock = pygame.time.Clock()
# running = True

# prev_keys = pygame.key.get_pressed()


# class escargot:
#     def __init__(self,couleur='red',y=0):
#         self.x=0
#         self.y=y
#         self.vitesse=10
#         self.couleur=couleur
        
#     def ajoutevitesse(self):
#         self.vitesse+=1
    
#     def avance(self):
#         self.x+=self.vitesse
    
#     def draw(self):
#        pygame.draw.rect(screen, self.couleur, (self.x,self.y,30,30))



# listeescargots=[]

# listeescargots.append(escargot())
# listeescargots.append(escargot(couleur='green', y=80))
# listeescargots.append(escargot(couleur='purple', y = 150))
# listeescargots.append(escargot(couleur='pink', y = 230 ))


# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     screen.fill("black")


#     for i in listeescargots:
#         i.draw()
    
#     keys = pygame.key.get_pressed()
    
#     if keys[pygame.K_RIGHT] and not prev_keys[pygame.K_RIGHT]:
#         listeescargots[0].avance()
    
#     if keys[pygame.K_LCTRL] and not prev_keys[pygame.K_LCTRL]:
#         listeescargots[1].avance()
   
#     if keys[pygame.K_SPACE] and not prev_keys[pygame.K_SPACE]:
#         listeescargots[2].avance()
    
#     if keys[pygame.K_RCTRL] and not prev_keys[pygame.K_RCTRL]:
#         listeescargots[3].avance()
        
#     prev_keys = keys
        
        

#     pygame.display.flip()
#     clock.tick(60)

# pygame.quit()

# pygame.quit()


import pygame
import sys
from random import randint

pygame.init()
L = 1280
H = 720
screen = pygame.display.set_mode((L, H))
clock = pygame.time.Clock()

# Chargement des images
bg = pygame.transform.scale(pygame.image.load("bg.png"), (1280, 720))
bleu = pygame.transform.scale(pygame.image.load("snail_1.1.png"), (110, 110))
vert = pygame.transform.scale(pygame.image.load("snail_2.1.png"), (110, 110))
jaune = pygame.transform.scale(pygame.image.load("snail_3.1.png"), (120, 120))
violet = pygame.transform.scale(pygame.image.load("snail_4.1.png"), (110, 110))

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Noms par défaut des escargots
noms_escargots = ["Bleu", "Vert", "Jaune", "Violet"]
touches_escargots = ["LCTRL", "SPACE", "RCTRL", "->"]

# Classe pour le menu
class Menu:
    def __init__(self):
        self.font_titre = pygame.font.SysFont(None, 72)
        self.font_texte = pygame.font.SysFont(None, 36)
        self.font_bouton = pygame.font.SysFont(None, 48)
        self.input_active = [False, False, False, False]
        self.input_index = 0
        self.noms = noms_escargots.copy()

    def dessiner(self):
        screen.blit(bg, (0, 0))
        titre = self.font_titre.render("Course d'escargots", True, WHITE)
        screen.blit(titre, (L//2 - titre.get_width()//2, 50))

        for i in range(4):
            couleur = BLUE if i == 0 else (0, 255, 0) if i == 1 else (255, 255, 0) if i == 2 else (128, 0, 128)
            nom = self.font_texte.render(f"{self.noms[i]} :", True, couleur)
            touche = self.font_texte.render(touches_escargots[i], True, WHITE)
            screen.blit(nom, (L//2 - 200, 150 + i*70))
            screen.blit(touche, (L//2 + 50, 150 + i*70))

            if self.input_active[i]:
                pygame.draw.rect(screen, WHITE, (L//2 - 200, 150 + i*70, 100, 40), 2)

        # Bouton Play
        pygame.draw.rect(screen, GRAY, (L//2 - 100, 500, 200, 60))
        play = self.font_bouton.render("Play", True, BLACK)
        screen.blit(play, (L//2 - play.get_width()//2, 510))

    def gerer_clics(self, pos):
        
        # Vérifie si on clique sur le bouton Play
        if L//2 - 100 <= pos[0] <= L//2 + 100 and 500 <= pos[1] <= 560:
            return "play"
        
        # Vérifie si on clique sur un champ de nom
        for i in range(4):
            if L//2 - 200 <= pos[0] <= L//2 + 100 and 150 + i*70 <= pos[1] <= 190 + i*70:
                self.input_active = [False]*4
                self.input_active[i] = True
                self.input_index = i
                return "menu"
        return "menu"

    def gerer_saisie(self, event):
        if event.type == pygame.KEYDOWN and any(self.input_active):
            i = self.input_index
            if event.key == pygame.K_RETURN:
                self.input_active[i] = False
            elif event.key == pygame.K_BACKSPACE:
                self.noms[i] = self.noms[i][:-1]
            else:
                self.noms[i] += event.unicode

