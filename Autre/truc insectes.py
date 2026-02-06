# -*- coding: utf-8 -*-
import pygame
from random import randint, random
import math
import os

pygame.init()
surf = pygame.display.set_mode((800, 600))
L = 800
H = 600

# Classe pour la pluie
class Goutte:
    def __init__(self, x, y, vitesse, longueur):
        self.x = x
        self.y = y
        self.vitesse = vitesse
        self.longueur = longueur

    def dessine(self):
        # Dessine une ligne verticale pour représenter la goutte
        pygame.draw.line(surf, (39, 187, 245), (self.x, self.y), (self.x, self.y + self.longueur), 2)

    def tombe(self):
        # Déplace la goutte vers le bas
        self.y += self.vitesse
        # Si la goutte sort de l'écran, réinitialise sa position en haut
        if self.y > H:
            self.y = randint(-20, 0)
            self.x = randint(0, L)

class Insecte:
    def __init__(self, x, y, images, vitesse=1):
        self.x = x
        self.y = y
        self.images = images
        self.vitesse = vitesse
        self.rect = self.images[0].get_rect(center=(x, y))
        self.compteur_animation = 0

    def dessine(self):
        surf.blit(self.images[self.compteur_animation // 10 % len(self.images)], self.rect)

    def calcule_futures_parametres(self):
        self.x += self.vitesse
        self.rect.center = (int(self.x), int(self.y))
        if self.x > L + self.rect.width // 2:
            self.x = -self.rect.width // 2
        self.compteur_animation += 1

class InsecteVolant:
    def __init__(self, x, y, images_marche, images_vol, vitesse=1):
        self.x = x
        self.y = y
        self.images_marche = images_marche  
        self.images_vol = images_vol        
        self.vitesse = vitesse
        self.flying = False
        self.rect = self.images_marche[0].get_rect(center=(x, y))
        self.compteur_animation = 0
        self.compteur_vol = 0
        self.vol_duree = 120  
        self.compteur_attente = 0
        self.attente_duree = 280
        self.y_sol = H - 200  # Niveau du sol pour les insectes

    def dessine(self):
        if self.flying:
            surf.blit(self.images_vol[self.compteur_animation // 10 % len(self.images_vol)], self.rect)
        else:
            surf.blit(self.images_marche[self.compteur_animation // 10 % len(self.images_marche)], self.rect)

    def calcule_futures_parametres(self):
        self.x += self.vitesse
        self.rect.center = (int(self.x), int(self.y))
        if self.x > L + self.rect.width // 2:
            self.x = -self.rect.width // 2
        # Gestion du décollage automatique
        if not self.flying:
            self.compteur_attente += 1
            if self.compteur_attente >= self.attente_duree:
                self.flying = True
                self.compteur_attente = 0
        # Animation de vol
        if self.flying:
            self.y -= 2  # Monte
            self.compteur_vol += 1
            if self.compteur_vol >= self.vol_duree:
                self.flying = False
                self.compteur_vol = 0
        else:
            # Redescend jusqu'au niveau du sol (H - 200)
            if self.y < self.y_sol:
                self.y += 1
        self.compteur_animation += 1

class Papillon:
    def __init__(self, x, y, images_vol, vitesse=1):
        self.x = x
        self.y = y
        self.images_vol = images_vol  
        self.vitesse = vitesse
        self.rect = self.images_vol[0].get_rect(center=(x, y))
        self.compteur_animation = 0
        self.angle = 0
        self.amplitude = 10
        self.frequence = 0.1

    def dessine(self):
        surf.blit(self.images_vol[self.compteur_animation // 10 % len(self.images_vol)], self.rect)

    def calcule_futures_parametres(self):
        self.x += self.vitesse
        self.rect.center = (int(self.x), int(self.y))
        if self.x > L + self.rect.width // 2:
            self.x = -self.rect.width // 2
        self.angle += self.frequence
        self.y = H // 2 + math.sin(self.angle) * self.amplitude  # Mouvement sinusoïdal
        self.compteur_animation += 1

# Classe pour la mouche
class Mouche:
    def __init__(self):
        self.x = randint(0, L)
        self.y = randint(0, H // 2)
        self.images = [mouche_1, mouche_2]
        self.rect = self.images[0].get_rect(center=(self.x, self.y))
        self.compteur_animation = 0
        self.cible_x = randint(0, L)
        self.cible_y = randint(0, H // 2)
        self.vitesse = 0.05

    def dessine(self):
        surf.blit(self.images[self.compteur_animation // 10 % len(self.images)], self.rect)

    def calcule_futures_parametres(self):
        if random() < 0.01:
            self.cible_x = randint(0, L)
            self.cible_y = randint(0, H // 2)
        dx = self.cible_x - self.x
        dy = self.cible_y - self.y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist > 0:
            self.x += dx * self.vitesse
            self.y += dy * self.vitesse
        if self.x > L + self.rect.width // 2:
            self.x = -self.rect.width // 2
        elif self.x < -self.rect.width // 2:
            self.x = L + self.rect.width // 2
        self.rect.center = (int(self.x), int(self.y))
        self.compteur_animation += 1

# Chargement des images
coccinelle_1 = pygame.transform.scale(pygame.image.load(os.path.join("images", "coccinelle_1_sol.png")), (95, 95))
coccinelle_2 = pygame.transform.scale(pygame.image.load(os.path.join("images", "coccinelle_2.3_sol.png")), (95, 95))
coccinelle_1_vol = pygame.transform.scale(pygame.image.load(os.path.join("images", "coccinelle_1_vol.png")), (95, 95))
coccinelle_2_vol = pygame.transform.scale(pygame.image.load(os.path.join("images", "coccinelle_2_vol.png")), (95, 95))
noiraude_1 = pygame.transform.scale(pygame.image.load(os.path.join("images", "noiraude_1.png")), (95, 95))
noiraude_2 = pygame.transform.scale(pygame.image.load(os.path.join("images", "noiraude_2.png")), (95, 95))
chenille_1 = pygame.transform.scale(pygame.image.load(os.path.join("images", "chenille_1.png")), (95, 95))
chenille_2 = pygame.transform.scale(pygame.image.load(os.path.join("images", "chenille_2.png")), (95, 95))
escargot_1 = pygame.transform.scale(pygame.image.load(os.path.join("images", "escargot_1.png")), (95, 95))
escargot_2 = pygame.transform.scale(pygame.image.load(os.path.join("images", "escargot_2.png")), (95, 95))
fourmi_1 = pygame.transform.scale(pygame.image.load(os.path.join("images", "fourmi_1.png")), (95, 95))
fourmi_2 = pygame.transform.scale(pygame.image.load(os.path.join("images", "fourmi_2.png")), (95, 95))
libellule_marche_1 = pygame.transform.scale(pygame.image.load(os.path.join("images", "libellule_1_sol.png")), (95, 95))
libellule_marche_2 = pygame.transform.scale(pygame.image.load(os.path.join("images", "libellule_2_sol.png")), (95, 95))
libellule_vol_1 = pygame.transform.scale(pygame.image.load(os.path.join("images", "libellule_1_vol.png")), (95, 95))
libellule_vol_2 = pygame.transform.scale(pygame.image.load(os.path.join("images", "libellule_2_vol.png")), (95, 95))
mouche_1 = pygame.transform.scale(pygame.image.load(os.path.join("images", "mouche_1.png")), (95, 95))
mouche_2 = pygame.transform.scale(pygame.image.load(os.path.join("images", "mouche_2.png")), (95, 95))
papillon_vol_1 = pygame.transform.scale(pygame.image.load(os.path.join("images", "papillon_1.png")), (95, 95))
papillon_vol_2 = pygame.transform.scale(pygame.image.load(os.path.join("images", "papillon_2.png")), (95, 95))
bourdon_1 = pygame.transform.scale(pygame.image.load(os.path.join("images", "bourdon_1.png")), (95, 95))
bourdon_2 = pygame.transform.scale(pygame.image.load(os.path.join("images", "bourdon_2.png")), (95, 95))
sauterelle_1 = pygame.transform.scale(pygame.image.load(os.path.join("images", "sauterelle_1.png")), (95, 95))
sauterelle_2 = pygame.transform.scale(pygame.image.load(os.path.join("images", "sauterelle_2.png")), (95, 95))
fond = pygame.image.load(os.path.join("images", "fond2.png"))
fond = fond.convert()

# Initialisation des objets
liste_objets = [
    InsecteVolant(0, H - 210, [coccinelle_1, coccinelle_2], [coccinelle_1_vol, coccinelle_2_vol], 1),  # Coccinelle
    Insecte(-125, H - 200, [noiraude_1, noiraude_2], 1),  # Noiraude
    Insecte(-250, H - 200, [chenille_1, chenille_2], 1),  # Chenille
    Insecte(-375, H - 200, [escargot_1, escargot_2], 1),  # Escargot
    InsecteVolant(-500, H - 200, [libellule_marche_1, libellule_marche_2], [libellule_vol_1, libellule_vol_2], 1),  # Libellule
    Insecte(-575, H - 210, [bourdon_1, bourdon_2], 1),  # Bourdon
    Insecte(-650, H - 200, [sauterelle_1, sauterelle_2], 1),  # Sauterelle
    Insecte(-800, H - 200, [fourmi_1, fourmi_2], 1),  # Fourmi
    Papillon(-150, H // 2, [papillon_vol_1, papillon_vol_2]),  # Papillon (vol permanent)
]

mouche = Mouche()
liste_objets.append(mouche)

# Initialisation des gouttes de pluie
gouttes = []
for _ in range(100):
    x = randint(0, L)
    y = randint(-H, 0)
    vitesse = randint(5, 15)
    longueur = randint(5, 15)
    gouttes.append(Goutte(x, y, vitesse, longueur))

# Boucle principale
run = True
clock = pygame.time.Clock()
compteur_pluie = 0
pluie_active = False


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    surf.blit(fond, (0, 0))

    # Incrémente le compteur de pluie
    compteur_pluie += 1
    # Active la pluie après 300 frames
    if compteur_pluie >= 300 and not pluie_active:
        pluie_active = True

    # Si la pluie est active, incrémente le compteur de durée
    if pluie_active:
        compteur_pluie += 1
        if compteur_pluie >= 1000 and pluie_active:
            pluie_active = False
            compteur_pluie = 0

    # Dessine et déplace les gouttes si la pluie est active
    if pluie_active:
        for goutte in gouttes:
            goutte.dessine()
            goutte.tombe()

    # Dessine et déplace les autres objets
    for obj in liste_objets:
        obj.dessine()
        obj.calcule_futures_parametres()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()


