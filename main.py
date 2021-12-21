import pygame
import random
import sys

WIDTH = 1280
HEIGHT = 768
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
        self.image = pygame.Surface((1 * 64, 2 * 64))
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


class Room():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        #  тут по тайлам распишем как устороена комната 0 - пол или стена если скраю, 1 - дверь, 2 ловушка, 3 предмет
        #  пока хз как это передавать, позже придумаю
        self.tiles = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen): # ТУТ ВМЕСТО РЕКТОВ НУЖНО ВСТАВИТЬ РЕНДЕР ТАЙЛОВ
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, (255, 255, 255), (i * self.cell_size + self.left, j * self.cell_size +
                                                           self.top, self.cell_size, self.cell_size), 1)


class AbstractBoss:
    pass
    #  тут крч сами как нибудь


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pygame_project")
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    pygame.key.set_repeat(1, 1)
    player = Player()
    room = Room(20, 12)
    room.set_view(0, 0, 64)
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

        screen.fill(BLACK)
        room.render(screen)
        all_sprites.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    sys.exit(main())