import pygame
import random
import sys

WIDTH = 1280
HEIGHT = 736
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.hp = 3
        self.key_frag = 0
        self.move_right_animation = []
        self.move_left_animation = []
        self.move_top_animation = []
        self.move_down_animation = []
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.left < 0:
            self.rect.left = 0


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame_project")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
pygame.key.set_repeat(1, 1)
player = Player()
all_sprites.add(player)
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.rect.y -= 1
        if keys[pygame.K_s]:
            player.rect.y += 1
        if keys[pygame.K_d]:
            player.rect.x += 1
        if keys[pygame.K_a]:
            player.rect.x -= 1
    all_sprites.update()
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
