import pygame
import PhysObjects
import numpy as np

grav_on = 1


def draw_object_parameters(cls):
    for index,instance in enumerate(cls._instances):
        text1 = font.render(f"K_p: {instance.k_p:.3f}   K_d: {instance.k_d:.3f}   {instance.description}",True,instance.color)
        # text2 = font.render(f"K_d: {instance.k_d:.3f}",True,instance.color)
        # text3
        screen.blit(text1,(10,10+(font_height*index)))
        # screen.blit(text2,(10+120,10+(font_height*index)))



pygame.init()

font = pygame.font.SysFont('Arial',30)
font_height = font.get_height()


screen_width, screen_height= 1500,1200
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Controls")
clock = pygame.time.Clock()


player1_IfElse = PhysObjects.Object2D(screen_width/2,screen_height/2,20,(0,255,0),"PD",0.1,2.5,0,grav_on,"High Kp, High Kd = High 'g' accel & decel, no overshoot")
player1_PD = PhysObjects.Object2D(screen_width/2,screen_height/2,20,(255,0,0),"PD",0.025,0.35,0,grav_on, "Low Kp, Low Kd = Mid 'g' accel, mid overshoot")
player2_PD = PhysObjects.Object2D(screen_width/2,screen_height/2,20,(0,255,255),"PD",0.025,2.5,0,grav_on, "Low Kp, High Kd = Low 'g' accel & decel, no overshoot")
player3_PD = PhysObjects.Object2D(screen_width/2,screen_height/2,20,(255,200,100),"PD",0.1,0.35,0,grav_on, "High Kp, Low Kd = High 'g' accel & decel, high overshoot")
# player1_PD_amax = PhysObjects.Object2D(screen_width-30,screen_height/2,15,(0,100,255),"PD_amax",0.05,1.10,1.25,grav_on,"Constnat value acc")
target = (screen_width/2,screen_height/2)

time_data = []
dist_data = {}
for i in range(len(PhysObjects.Object2D._instances)):
    dist_data[i] = []
time = 0
plot_start_x = (6/7)*screen_width
plot_start_y = screen_height/2
running = True

while running:
    clock.tick(60)
    screen.fill((0,0,0))

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if event.button == 1: #left mouse button
        #         mouse_x,mouse_y = pygame.mouse.get_pos()
        #         target = (mouse_x,mouse_y)
    mouse_x,mouse_y = pygame.mouse.get_pos()
    target = (mouse_x,mouse_y)
    target_vec = np.array([mouse_x,mouse_y])

    if time_data:
        time_data = [x + 1 for x in time_data]
    
    time_data.append(time)
    for index,obj in enumerate(PhysObjects.Object2D._instances):    
        current_dist = np.linalg.norm(target_vec-obj.pos)
        dist_data[index].append(current_dist)
    
    if len(time_data) > screen_width-plot_start_x:
        time_data.pop(0)
        for key,dist_list in dist_data.items():
            dist_list.pop(0)


    PhysObjects.Object2D.gravity()
    PhysObjects.Object2D.update(target)
    PhysObjects.Object2D.draw(screen)
    # Target line draws (poor code lol)#################################
    pygame.draw.line(screen,(0,170,0),target,(target[0],target[1]+20),3)
    pygame.draw.line(screen,(0,170,0),target,(target[0],target[1]-20),3)
    pygame.draw.line(screen,(0,170,0),target,(target[0]+20,target[1]),3)
    pygame.draw.line(screen,(0,170,0),target,(target[0]-20,target[1]),3)
    ####################################################################

    for key,dist_list in dist_data.items():
        for i in range(1,len(time_data)):
            pygame.draw.line(screen,PhysObjects.Object2D._instances[key].color,
            (screen_width - time_data[i-1] , plot_start_y - dist_list[i-1] ),
            (screen_width - time_data[i] ,   plot_start_y - dist_list[i]   ),
            4)

    pygame.draw.line(screen,(255,255,255),(plot_start_x,screen_height/2),(screen_width,screen_height/2),2)
    pygame.draw.line(screen,(255,255,255),(plot_start_x,screen_height/2),(plot_start_x,100),2)

    draw_object_parameters(PhysObjects.Object2D)
    pygame.display.flip()

pygame.quit()
