import pygame
import random
import sys
import os


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, is_wall):
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
        self.cords = [pos_x * 64, pos_y * 64]
        self.old_cords = 0, 0
        self.hp = 3
        self.speed = 1

    def update(self):
        collides = pygame.sprite.spritecollide(self, all_sprites, False)
        for coll in collides:
            if coll.__class__ is Tile:
                if coll.image == tile_images['wall']:
                    if self.rect.collidepoint(coll.rect.center):
                        if self.rect.x + 15 < coll.rect.x:
                            self.rect.x -= 15
                        if self.rect.x - 15 > coll.rect.x:
                            self.rect.x += 15
                        if self.rect.y + 15 < coll.rect.y:
                            self.rect.y -= 15
                        if self.rect.y - 15 > coll.rect.y:
                            self.rect.y += 15


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
                Tile('empty', x, y, False)
            elif level[y][x] == '#':
                Tile('wall', x, y, True)
            elif level[y][x] == '@':
                Tile('empty', x, y, False)
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
            if keys[pygame.K_w]:
                player.old_cords = player.rect.x, player.rect.y
                player.rect.y -= player.speed
            if keys[pygame.K_s]:
                player.old_cords = player.rect.x, player.rect.y
                player.rect.y += player.speed
            if keys[pygame.K_d]:
                player.old_cords = player.rect.x, player.rect.y
                player.rect.x += player.speed
            if keys[pygame.K_a]:
                player.old_cords = player.rect.x, player.rect.y
                player.rect.x -= player.speed
        screen.fill(pygame.Color('black'))
        player_group.update()
        all_sprites.update()
        all_sprites.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    sys.exit(main())
