import pygame
import PhysObjects

pygame.init()

screen_width, screen_height= 1200,1200
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Controls")
clock = pygame.time.Clock()


player1_IfElse = PhysObjects.Object2D(30,screen_height/2,25,(0,255,0),"IfElse")
player1_PD = PhysObjects.Object2D(screen_width-30,screen_height/2,25,(255,0,0),"PD")
target = (screen_width/2,screen_height/2)


running = True
while running:
    clock.tick(60)
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: #left mouse button
                mouse_x,mouse_y = pygame.mouse.get_pos()
                target = (mouse_x,mouse_y)

    PhysObjects.Object2D.update(target)
    PhysObjects.Object2D.draw(screen)
    # Target line draws (poor code lol)#################################
    pygame.draw.line(screen,(0,170,0),target,(target[0],target[1]+20),3)
    pygame.draw.line(screen,(0,170,0),target,(target[0],target[1]-20),3)
    pygame.draw.line(screen,(0,170,0),target,(target[0]+20,target[1]),3)
    pygame.draw.line(screen,(0,170,0),target,(target[0]-20,target[1]),3)
    ####################################################################

    pygame.display.flip()

pygame.quit()
