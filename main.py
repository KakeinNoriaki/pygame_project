import pygame
import sys
import os
import time


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
                        self.get_out_of_the_wall_or_trap(coll.rect.x, coll.rect.y, 0)
                if coll.image == tile_images['pit'] or coll.image == tile_images['spike']:
                    if self.rect.collidepoint(coll.rect.center):
                        self.hp -= 1
                        print(self.hp)
                        self.get_out_of_the_wall_or_trap(coll.rect.x, coll.rect.y, 45)
                        time.sleep(0.5)
                if coll.image == tile_images['door']:
                    if self.rect.collidepoint(coll.rect.center):
                        load_new_lvl()

    def get_out_of_the_wall_or_trap(self, coll_rect_x, coll_rect_y, mod):
        if self.rect.x + 15 < coll_rect_x:
            self.rect.x -= 15 + mod
        if self.rect.x - 15 > coll_rect_x:
            self.rect.x += 15 + mod
        if self.rect.y + 15 < coll_rect_y:
            self.rect.y -= 15 + mod
        if self.rect.y - 15 > coll_rect_y:
            self.rect.y += 15 + mod


class AbstractBoss:
    pass
    #  тут крч сами как нибудь


def load_image(name):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    global level_map
    filename = filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('floor', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('floor', x, y)
                new_player = Player(x, y)
            elif level[y][x] == 'O':
                Tile('pit', x, y)
            elif level[y][x] == '1':
                Tile('spike', x, y)
            elif level[y][x] == 'E':
                Tile('door', x, y)
    return new_player, x, y


def load_new_lvl():
    global player, level_x, level_y, level_map, all_sprites
    all_sprites = pygame.sprite.Group()
    player.kill()
    level_map = load_level('map_2.txt')
    player, level_x, level_y = generate_level(level_map)
    all_sprites.add(player)
    print(all_sprites)


WIDTH = 1280
HEIGHT = 768
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

tile_images = {
    'wall': load_image("assets\_rooms\_room_tiles_1\wall_tile.png"),
    'floor': load_image("assets\_rooms\_room_tiles_1\_floor_tile.png"),
    'spike': load_image("assets\_rooms\_room_tiles_1\spike_tile.png"),
    'pit': load_image("assets\_rooms\_room_tiles_1\pit_tile.png"),
    'door': load_image("assets\_rooms\_room_tiles_1\_floor_tile.png"),
}

pygame.display.set_caption("Pygame_project")
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tile_width = tile_height = 64
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bgk = pygame.Surface((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.key.set_repeat(1, 1)
player_image = load_image('assets\player\down\player_move_down_1.png')

level_map = load_level('map_1.txt')
player, level_x, level_y = generate_level(level_map)
all_sprites.add(player)


def main():
    print(all_sprites)
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
        screen.fill((180, 35, 122))
        player_group.update()
        all_sprites.update()
        all_sprites.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    sys.exit(main())
