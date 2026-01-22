import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
keystate = pygame.key.get_pressed()

color='black'
couleurrect='red'
couleurrect2='yellow'

count=0
count2=0

prev_keys = pygame.key.get_pressed()

def point_in_rect(x, y, x1, y1, x2, y2):
    return min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(color)
        
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_RIGHT] and not prev_keys[pygame.K_RIGHT]:
        color='orange'
        count+=1
        print(1, count)

    if keys[pygame.K_LCTRL] and not prev_keys[pygame.K_LCTRL]:
        color='blue'
        count2+=1
        print(2, count2)
    

    prev_keys = keys
    
    mpos=pygame.mouse.get_pos()
    lclick=pygame.mouse.get_pressed(3)[0]
    
    if lclick:
        print(mpos)
        if point_in_rect(mpos[0], mpos[1], 0, 0, 200, 200):
            print('rect1')
            couleurrect='blue'
        if point_in_rect(mpos[0], mpos[1], 400, 0, 600, 200):
            print('rect2')
            couleurrect2='purple'
        
    else:
        couleurrect='red'
        couleurrect2='yellow'
    
    
    pygame.draw.rect(screen, couleurrect, (0,0,200,200))
    pygame.draw.rect(screen, couleurrect2, (400,0,200,200))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()