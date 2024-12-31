from typing import Any
import pygame
from pygame.locals import *
import pygame.locals
from pygame.sprite import Group
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 664
screen_height = 736

#Definir fondo de la pantalla
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('FLAPPY BIRD')

#definir fuente
font = pygame.font.SysFont('Bauhaus 93', 60)


#definir colores
withe = (255, 255, 255)


#definir variables del juego
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500 #milisegundos
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False


#cargar imagenes
bg = pygame.image.load('bg.png')
ground_img = pygame.image.load('ground.png')
button_img = pygame.image.load('restart.png')

def dificultad(score):
    global scroll_speed, pipe_frequency
    scroll_speed = 4 + (score // 4) * 1
    pipe_frequency = max(1500 - (score //4) * 80, 500)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def reset_game():
    global scroll_speed
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height/2)
    score = 0
    scroll_speed = 4
    return score

def mostrar_mensaje(score):

    y_pos = screen_height - 100
    x_pos = 50

    if score >= 25:
            draw_text(("Omg"), font, withe, x_pos + 20, y_pos)
    #elif score >= 7 and score < 10:
    #    draw_text(("No que muy acá"), font, withe, x_pos + 80, y_pos)
    #elif score >= 0 and score < 7:
    #    draw_text(("Nah mijo, ni pa la muela"), font, withe, x_pos + 60, y_pos)

class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.clicked = False
        self.rotation_angle = 0

    def update(self):
        #handle the animation

        #gravity
        if flying == True:
            self.vel += 0.6
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 568:
                self.rect.y += int(self.vel)

        if game_over == False:

        #jump

            if pygame.key.get_pressed()[pygame.K_SPACE] == 1 and self.clicked == False :
                self.clicked = True
                self.vel = -8
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.clicked = False
        


            self.counter += 1
            flap_cooldown = 7


            #animacion bird
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            #rotate
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
            self.rotation_angle = 0 
        else:
            #self.image = pygame.transform.rotate(self.images[self.index], -90)
            self.rotation_angle += 5  # Ajusta este valor para controlar la velocidad de rotación
            self.image = pygame.transform.rotate(self.images[self.index], self.rotation_angle)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('pipe.png')
        self.rect = self.image.get_rect()
        #posicion 1 es para el top, posicion -1 para el bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap/2) ]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap/2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def draw(self):
        action = False

        #mostrar la posicion del mouse
        pos = pygame.mouse.get_pos()

        #verificar si el mouse está sobre el boton
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        #dibujar boton
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height/2))
bird_group.add(flappy)

#crear instancia del boton de restart
button = Button(screen_width // 2 -50, screen_height // 2 -100, button_img)

run = True
#Bucle principal
while run:

    clock.tick(fps)

    dificultad(score)

    #draw background
    screen.blit(bg, (0,0))
   

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    #dibujar el piso
    screen.blit(ground_img,(ground_scroll,568))

    #revisar el puntaje
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    print(score)
    draw_text(str(score), font, withe, int(screen_width /2 ), 20)

    #revisar la colision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0 :
        game_over = True


    #ver si el pajaro se verguió
    if flappy.rect.bottom >= 568:
        game_over = True
        flying = False

    #draw and scroll the ground
    if game_over == False and flying == True:

        #hacer nuevos tubos
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height/2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height/2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now


        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0
        pipe_group.update()

    #revisar si se murio y resetear
    if game_over == True:
        mostrar_mensaje(score)
        if button.draw() == True:
            game_over = False
            score = reset_game()
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not flying and not game_over:
                flying = True  # Activar vuelo cuando se presione barra espaciadora

        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
        

    pygame.display.update()

pygame.quit()

