import pygame
pygame.init()
from random import randint

screen_width = 500
screen_height = 300
screen = pygame.display
screen.set_mode((screen_width, screen_height))
screen.set_caption("my pyGAME")

all_sprite = []

class Player(pygame.sprite.Sprite):
    def __init__(self, width=30, height=14, speed=5, color="blue", max_health=3):
        super().__init__()
        self.x = screen_width / 2
        self.y = 200
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.max_health = max_health
        self.current_health = self.max_health
        self.should_move_right = False
        self.should_move_left = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        all_sprite.add(self)
    
    def update(self):
        self.should_move_right = False
        self.should_move_left = False
        for event in pygame.key.get_pressed():
            if event == pygame.K_RIGHT:
                self.should_move_right = True
            if event == pygame.K_LEFT:
                self.should_move_left = True
        if pygame.mouse.get_pressed()[0]:
            if pygame.mouse.get_pos()[0] > self.x:
                self.should_move_right = True
            elif pygame.mouse.get_pos()[0] < self.x:
                self.should_move_left = True
        self.move(self.speed, int(self.should_move_right)-int(self.should_move_left))
    
    def move(self, speed, dir):
        self.rect.x += speed * dir
        if self.x > screen_width:
            self.x = screen_height
        elif self.x < 0:
            self.x = 0
    
    def remove_health(self, count=1):
        self.current_health -= count
        if self.current_health <= 0:
            self.die()
    
    def die(self):
        self.kill()

    def draw(self):
        pygame.draw.rect(screen.get_surface(), self.color, self.rect)

class Meteor(pygame.sprite.Sprite):
    def __init__(self, x, y=0, width=20, height=25, speed=3, color="red"):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.active = True
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        all_sprite.add(self)
    
    def update(self, player):
        self.move(self.speed)
        if self.y >= screen_height:
            self.expload()
        
        if self.colliderect(player.rect):
            if self.active:
                player.remove_health()
            self.active = False
            self.expload()

    
    def move(self, speed):
        self.rect.y += speed
    
    def expload(self):
        self.kill()

    def draw(self):
        pygame.draw.rect(screen.get_surface(), self.color, self.rect)

player = Player()
meteors = []

running = True
while running:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            running = False
    
    if randint(1, 100) == 1:
        meteors.add(Meteor)
    screen.get_surface().fill((0, 0, 0))
    player.update()
    meteors.update(player)
    all_sprite.draw()
    screen.flip()
    pygame.time.Clock().tick(60)

pygame.quit()