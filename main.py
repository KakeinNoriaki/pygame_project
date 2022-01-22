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
        global room, counter
        collides = pygame.sprite.spritecollide(self, all_sprites, False)
        for coll in collides:
            if coll.__class__ is Tile:
                if coll.image == tile_images['wall']:
                    if self.rect.collidepoint(coll.rect.center):
                        self.get_out_of_the_wall_or_trap(coll.rect.x, coll.rect.y)
                if coll.image == tile_images['pit'] or coll.image == tile_images['spike']:
                    if self.rect.collidepoint(coll.rect.center):
                        if counter > 250:
                            print(counter)
                            self.hp -= 1
                            counter = 0
                        print(self.hp)
                        self.get_out_of_the_wall_or_trap_2(coll.rect.x, coll.rect.y)
                        #time.sleep(0.5)
                if coll.image != tile_images['pit'] or coll.image != tile_images['spike']:
                    counter += 1

                if coll.image == tile_images['door']:
                    if self.rect.collidepoint(coll.rect.center):
                        if room == 1:
                            load_new_lvl()
                        #if room == 2:
                            #load_new_lvl2()

    def get_out_of_the_wall_or_trap(self, coll_rect_x, coll_rect_y):
        if self.rect.x + 1 < coll_rect_x:
            self.rect.x -= 7
        if self.rect.x - 1 > coll_rect_x:
            self.rect.x += 7
        if self.rect.y + 1 < coll_rect_y:
            self.rect.y -= 7
        if self.rect.y - 1 > coll_rect_y:
            self.rect.y += 7


    def get_out_of_the_wall_or_trap_2(self, coll_rect_x, coll_rect_y):
        if self.rect.x + 1 < coll_rect_x:
            self.rect.x -= 15
        if self.rect.x - 1 > coll_rect_x:
            self.rect.x += 15
        if self.rect.y + 1 < coll_rect_y:
            self.rect.y -= 15
        if self.rect.y - 1 > coll_rect_y:
            self.rect.y += 15


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
    global player, level_x, level_y, level_map, all_sprites, room
    if room == 2:
        all_sprites = pygame.sprite.Group()
        player.kill()
        level_map = load_level('map_2.txt')
        player, level_x, level_y = generate_level(level_map)
        all_sprites.add(player)
        room += 1
        print(all_sprites)
    elif room == 1:
        all_sprites = pygame.sprite.Group()
        player.kill()
        level_map = load_level('map_2.txt')
        player, level_x, level_y = generate_level(level_map)
        all_sprites.add(player)
        room += 1
        print(all_sprites)
        print(room)












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


walkright = [pygame.image.load("assets\player\Right\player_move_right_1.png"), pygame.image.load("assets\player\Right\player_move_right_2.png"), pygame.image.load("assets\player\Right\player_move_right_3.png")]
walkleft = [pygame.image.load("assets\player\left\player_move_left_1.png"), pygame.image.load("assets\player\left\player_move_left_2.png"), pygame.image.load("assets\player\left\player_move_left_3.png")]
walkforward = [pygame.image.load("assets\player\Forward\player_move_up_1.png"), pygame.image.load("assets\player\Forward\player_move_up_2.png"), pygame.image.load("assets\player\Forward\player_move_up_3.png")]
walkdown = [pygame.image.load("assets\player\down\player_move_down_1.png"), pygame.image.load("assets\player\down\player_move_down_2.png"), pygame.image.load("assets\player\down\player_move_down_3.png")]
playerStand = [pygame.image.load("assets\player\down\player_move_down_1.png")]


level_map = load_level('map_1.txt')
player, level_x, level_y = generate_level(level_map)
all_sprites.add(player)
room = 1
counter = 0
с1 = 20
animCount = 0

left = False
right = False
forward = False
down = False

def main():
    global animCount, left, right, forward, down, playerStand
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
                left = False
                right = False
                forward = True
                down = False


            if keys[pygame.K_s]:
                player.old_cords = player.rect.x, player.rect.y
                player.rect.y += player.speed
                left = False
                right = False
                forward = False
                down = True

            if keys[pygame.K_d]:
                player.old_cords = player.rect.x, player.rect.y
                player.rect.x += player.speed
                left = False
                right = True
                forward = False
                down = False

            if keys[pygame.K_a]:
                player.old_cords = player.rect.x, player.rect.y
                player.rect.x -= player.speed
                left = True
                right = False
                forward = False
                down = False

            if not(keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]):
                left = False
                right = False
                forward = False
                down = False


        screen.fill((180, 35, 122))
        player_group.update()
        all_sprites.update()
        all_sprites.draw(screen)

        if animCount + 1 >= 60:
            animCount = 0

        if left:
            screen.blit(walkleft[animCount // 20], (player.rect.x, player.rect.y))
            animCount += 1

        if right:
            screen.blit(walkright[animCount // 20], (player.rect.x, player.rect.y))
            animCount += 1

        if forward:
            screen.blit(walkforward[animCount // 20], (player.rect.x, player.rect.y))
            animCount += 1

        if down:
            screen.blit(walkdown[animCount // 20], (player.rect.x, player.rect.y))
            animCount += 1
        if not (forward or left or right or down):
            screen.blit(playerStand[0], (player.rect.x, player.rect.y))


        pygame.display.flip()




if __name__ == '__main__':
    sys.exit(main())