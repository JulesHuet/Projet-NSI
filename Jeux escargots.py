import pygame
import sys
from random import randint

pygame.init()
L = 1280
H = 720
screen = pygame.display.set_mode((L, H))
clock = pygame.time.Clock()

class Goutte:
    def __init__(self, x, y, vitesse, longueur):
        self.x = x
        self.y = y
        self.vitesse = vitesse
        self.longueur = longueur

    def dessine(self):
        pygame.draw.line(screen, (135, 206, 235), (self.x, self.y), (self.x, self.y + self.longueur), 2)

    def tombe(self):
        self.y += self.vitesse
        if self.y > H:
            self.y = randint(-20, 0)
            self.x = randint(0, L)

class Confetti:
    def __init__(self):
        self.x = randint(0, L)
        self.y = randint(-H, 0)
        self.v = randint(2, 5)
        self.taille = randint(3, 6)
        self.couleur = (randint(50, 255), randint(50, 255), randint(50, 255))
    
    def bouger(self):
        self.y += self.v
        if self.y > H:
            self.y = -10
            self.x = randint(0, L)
            self.couleur = (randint(50, 255), randint(50, 255), randint(50, 255))
    
    def afficher(self):
        pygame.draw.circle(screen, self.couleur, (self.x, int(self.y)), self.taille)

class escargot:
    def __init__(self, img, y=680):
        self.x = 0
        self.y = y
        self.vitesse = 10
        self.img = img
        self.position_podium = None

    def bouger(self):
        self.vitesse += 0.1
        self.x += self.vitesse

    def afficher(self):
        screen.blit(self.img, (self.x, self.y))
        
class Leaderboard():
    def __init__(self):
        self.font = pygame.font.SysFont(None, 36)
        self.resultats = []
        
    def ajouter(self, couleur, temps):
        for r in self.resultats:
            if r[0] == couleur:
                return
        self.resultats.append((couleur, temps))
    
    def afficher(self):
        posY = H//2 + (-70)
        for pos, (couleur, temps) in enumerate(self.resultats):
            sec = temps / 60
            texte = self.font.render(f"{pos+1}. {couleur} - {sec:.2f}s", True, (255, 255, 255))
            screen.blit(texte, (L//2 - 250, posY))
            posY += 40
        
class Fond:
    def afficher(self):
        screen.blit(bg, (0, 0))
 
        
class affiche_victoire():
    def __init__(self, couleur):
        self.couleur = couleur
        self.font = pygame.font.SysFont(None, 72)
        self.texte = self.font.render(f"Victoire de {self.couleur} !", True, (255, 255, 255))
        
    def afficher(self):
        screen.blit(self.texte, (L//2 - self.texte.get_width()//2, 210))

class Podium():
    def __init__(self, img):
        self.img = img
        self.positions = {0: (700, 260), 1: (630, 300), 2: (760, 300)}
    
    def afficher(self, leaderboard, listeescargots):
        screen.blit(self.img, (600, 230))
        for i in range(min(3, len(leaderboard.resultats))):
            couleur, temps = leaderboard.resultats[i]
            escargots = ['Bleu', 'Vert', 'Jaune', 'Violet'].index(couleur)
            escargot = listeescargots[escargots]
            pos = self.positions[i]
            screen.blit(escargot.img, pos)
        
        
bg = pygame.transform.scale(pygame.image.load("bg.png"), (1280, 720))
podium = pygame.transform.scale(pygame.image.load("podium.png"), (300, 300))
bleu = pygame.transform.scale(pygame.image.load("snail_1.1.png"), (110, 110))
vert = pygame.transform.scale(pygame.image.load("snail_2.1.png"), (110, 110))
jaune = pygame.transform.scale(pygame.image.load("snail_3.1.png"), (120, 120))
violet = pygame.transform.scale(pygame.image.load("snail_4.1.png"), (110, 110)) 

# Initialisation des gouttes de pluie
gouttes = []
for _ in range(100):
    x = randint(0, L)
    y = randint(-H, 0)
    vitesse = randint(15, 30)
    longueur = randint(5, 15)
    gouttes.append(Goutte(x, y, vitesse, longueur))

confettis = [Confetti() for i in range(150)]

# LISTE DE TOUTES LES CLASSES EN ORDRE DE COUCHE
liste_objets = [Fond()]
listeescargots = [
    escargot(img=bleu, y=460),
    escargot(img=vert, y=520),
    escargot(img=jaune, y=570),
    escargot(img=violet, y=620)
]

# Boucle principale
run = True
compteur_pluie = 0
compteur_frame = 0
leaderboard = None
pluie_active = False
confettis_actifs = False
prev_keys = pygame.key.get_pressed()
victoire = None
course_lancee = False
decompte = ['3', '2', '1', 'Go !']
index_decompte = 0
decompte_actif = True
font_decompte = pygame.font.SysFont(None, 100)
afficher_podium = False
podium = Podium(podium)

while run:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            run = False

    clock.tick(60)

    # Affiche le fond
    screen.blit(bg, (0, 0))

    # Gestion du décompte
    if decompte_actif:
        texte_decompte = font_decompte.render(decompte[index_decompte], True, (255, 255, 255))
        screen.blit(texte_decompte, (L//2 - texte_decompte.get_width()//2, H//2 - 50))
        pygame.display.flip()
        pygame.time.wait(1000)  # Attend 1 seconde
        index_decompte += 1
        if index_decompte >= len(decompte):
            decompte_actif = False
            course_lancee = True
            compteur_frame = 0  # Réinitialise le compteur de temps
        continue  # On saute le reste de la boucle pendant le décompte
        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_TAB] and not prev_keys[pygame.K_TAB]:
        for escargot in listeescargots:
            escargot.x = 0
            escargot.vitesse = 400
        victoire = None
        leaderboard = None
        afficher_podium = False
        confettis_actifs = False
        compteur_frame = 0
        course_lancee = False
        decompte_actif = True
        index_decompte = 0
        compteur_pluie = 0
        pluie_active = False

    if not afficher_podium:
        if keys[pygame.K_LCTRL] and not prev_keys[pygame.K_LCTRL]:
            listeescargots[0].bouger()
        if keys[pygame.K_SPACE] and not prev_keys[pygame.K_SPACE]:
            listeescargots[1].bouger()
        if keys[pygame.K_RCTRL] and not prev_keys[pygame.K_RCTRL]:
            listeescargots[2].bouger()
        if keys[pygame.K_RIGHT] and not prev_keys[pygame.K_RIGHT]:
            listeescargots[3].bouger()
    prev_keys = keys

    # Affiche les objets
    for obj in liste_objets:
        obj.afficher()

    if not afficher_podium:
        for escargot in listeescargots:
            escargot.afficher()
    else:
        podium.afficher(leaderboard, listeescargots)

    for i, escargot in enumerate(listeescargots):
        if escargot.x >= L - 30 and victoire is None:
            victoire = affiche_victoire(['bleu', 'vert', 'jaune', 'violet'][i])
            leaderboard = Leaderboard()
            confettis_actifs = True
        if escargot.x >= L - 30 and leaderboard:
            leaderboard.ajouter(['Bleu', 'Vert', 'Jaune', 'Violet'][i], compteur_frame)
            
            if len(leaderboard.resultats) == 4:
                afficher_podium = True
            
    # Dessine et déplace les gouttes si la pluie est active
    if pluie_active:
         for goutte in gouttes:
             goutte.dessine()
             goutte.tombe()

    if confettis_actifs:
        for confetti in confettis:
            confetti.afficher()
            confetti.bouger()

    # Incrémente le compteur de pluie
    compteur_pluie += 1
    if course_lancee:
        compteur_frame += 1

    # Active la pluie 
    if compteur_pluie >= 500 and not pluie_active:
        pluie_active = True

    # Si la pluie est active, incrémente le compteur de durée
    if pluie_active:
        compteur_pluie += 1
        if compteur_pluie >= 1000 and pluie_active:
            pluie_active = False
            compteur_pluie = 0

    if victoire:
        victoire.afficher()

    if leaderboard:
        leaderboard.afficher()

    pygame.display.flip()

pygame.quit()
sys.exit()
 
