import pygame
import random
import sys
import os


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y - 64)
        self.pos = [pos_x, pos_y]
        # здесь будем хранить изменения по x и если оно равно 64 или -64 обнулям и меняем pos_x на 1 или -1
        # аналогично с y
        # это всё нужно что бы правильно считать столкновения со стенами
        self.move_x = 0
        self.move_y = 0

    def update(self):
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.left < 0:
            self.rect.left = 0

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0],
                                               tile_height * self.pos[1] - 64)


class AbstractBoss:
    pass
    #  тут крч сами как нибудь


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    filename = filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


WIDTH = 1280
HEIGHT = 768
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}

pygame.display.set_caption("Pygame_project")
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tile_width = tile_height = 64
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.key.set_repeat(1, 1)

level_map = load_level('map.txt')
player_image = load_image('assets\player\down\player_move_down_1.png')
player, level_x, level_y = generate_level(load_level('map.txt'))
all_sprites.add(player)


def main():
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                x, y = player.pos
                if keys[pygame.K_w]:
                    if y > 0 and level_map[y - 1][x] != '#':
                        player.move(x, y - 1)
                if keys[pygame.K_s]:
                    if y < level_y - 1 and level_map[y + 1][x] != '#':
                        player.move(x, y + 1)
                if keys[pygame.K_d]:
                    if x < level_x - 1 and level_map[y][x + 1] != '#':
                        player.move(x + 1, y)
                if keys[pygame.K_a]:
                    if x > 0 and level_map[y][x - 1] != '#':
                        player.move(x - 1, y)
        screen.fill(pygame.Color('black'))
        player_group.update()
        all_sprites.update()
        all_sprites.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    sys.exit(main())
