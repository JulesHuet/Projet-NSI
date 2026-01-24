import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

prev_keys = pygame.key.get_pressed()


class escargot:
    def __init__(self,couleur='red',y=0):
        self.x=0
        self.y=y
        self.vitesse=10
        self.couleur=couleur
        
    def ajoutevitesse(self):
        self.vitesse+=1
    
    def avance(self):
        self.x+=self.vitesse
    
    def draw(self):
       pygame.draw.rect(screen, self.couleur, (self.x,self.y,30,30))



listeescargots=[]

listeescargots.append(escargot())
listeescargots.append(escargot(couleur='green', y=80))
listeescargots.append(escargot(couleur='purple', y = 150))
listeescargots.append(escargot(couleur='pink', y = 230 ))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")


    for i in listeescargots:
        i.draw()
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_RIGHT] and not prev_keys[pygame.K_RIGHT]:
        listeescargots[0].avance()
    
    if keys[pygame.K_LCTRL] and not prev_keys[pygame.K_LCTRL]:
        listeescargots[1].avance()
   
    if keys[pygame.K_SPACE] and not prev_keys[pygame.K_SPACE]:
        listeescargots[2].avance()
    
    if keys[pygame.K_RCTRL] and not prev_keys[pygame.K_RCTRL]:
        listeescargots[3].avance()
        
    prev_keys = keys
        
        

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

pygame.quit()

