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
        if self.hp > 0:
            global level_now_num, counter
            collides = pygame.sprite.spritecollide(self, all_sprites, False)
            for coll in collides:
                if coll.__class__ is Tile:
                    if coll.image == tile_images['wall']:
                        if self.rect.collidepoint(coll.rect.center):
                            self.get_out_of_the_wall_or_trap(coll.rect.x, coll.rect.y)
                    if coll.image == tile_images['pit'] or coll.image == tile_images['spike']:
                        if self.rect.collidepoint(coll.rect.center):
                            if counter > 20:
                                self.hp -= 1
                                counter = 0
                            print(self.hp)
                            self.get_out_of_the_wall_or_trap_2(coll.rect.x, coll.rect.y)
                            counter += 1
                    if coll.image == tile_images['door_out']:
                        if self.rect.collidepoint(coll.rect.center):
                            level_now_num += 1
                            load_new_room(f'map_{level_now_num}.txt')
                            break
                    if coll.image == tile_images['door_in']:
                        if self.rect.collidepoint(coll.rect.center):
                            level_now_num -= 1
                            load_new_room(f'map_{level_now_num}.txt')
                            break
        else:
            game_over()

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


def generate_level(room):
    for y in range(len(room)):
        for x in range(len(room[y])):
            if room[y][x] == '.':
                Tile('floor', x, y)
            elif room[y][x] == '#':
                Tile('wall', x, y)
            elif room[y][x] == '@':
                Tile('floor', x, y)
                new_player = Player(x, y)
            elif room[y][x] == 'O':
                Tile('pit', x, y)
            elif room[y][x] == '1':
                Tile('spike', x, y,)
            elif room[y][x] == 'E':
                Tile('door_out', x, y)
            elif room[y][x] == 'W':
                Tile('door_in', x, y)
    return new_player, x, y


def load_new_room(room):
    global player, level_x, level_y, level_map, all_sprites
    all_sprites = pygame.sprite.Group()
    player.kill()
    level_map = load_level(room)
    player, level_x, level_y = generate_level(level_map)
    all_sprites.add(player)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["  Начать игру",
                  "Выйти из игры",
                  "      Авторы"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('comicsansms', 60)
    text_coord = 300
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord += 30
        intro_rect.top = text_coord
        intro_rect.x = WIDTH / 2 - 230
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
                if 14 * 30 <= event.pos[0] <= WIDTH / 2 and 300 <= event.pos[1] <= 420:
                    pygame.mixer.music.load('assets/tracks/main_theme')
                    pygame.mixer.music.set_volume(0.01)
                    pygame.mixer.music.play()
                    main()
                if 14 * 30 <= event.pos[0] <= WIDTH / 2 and 420 <= event.pos[1] <= 540:
                    terminate()
                if 14 * 30 <= event.pos[0] <= WIDTH / 2 and 540 <= event.pos[1] <= 660:
                    authors_screen()

        pygame.display.flip()
        clock.tick(FPS)


def authors_screen():
    intro_text = ["Князев 'Kakein Noriaki' Максим",
                  "Артём Мохов",
                  "Владислав Соловцов"]

    fon = pygame.transform.scale(load_image('fon_2.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('comicsansms', 60)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord += 30
        intro_rect.top = text_coord
        intro_rect.x = 50
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                start_screen()
        pygame.display.flip()
        clock.tick(FPS)


def game_over():
    intro_text = ["Игра окончена"]
    pygame.mixer.music.load('assets/tracks/main_menu_music')
    pygame.mixer.music.set_volume(0.01)
    pygame.mixer.music.play()
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('comicsansms', 80)
    text_coord = 300
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('yellow'))
        intro_rect = string_rendered.get_rect()
        text_coord += 30
        intro_rect.top = text_coord
        intro_rect.x = WIDTH / 2 - 230
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                start_screen()
        pygame.display.flip()
        clock.tick(FPS)

        pygame.display.flip()
        clock.tick(FPS)


WIDTH = 1280
HEIGHT = 768
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

tile_images = {
    'wall': load_image("assets/rooms/room_tiles_1/wall_tile.png"),
    'floor': load_image("assets/rooms/room_tiles_1/floor_tile.png"),
    'spike': load_image("assets/rooms/room_tiles_1/spike_tile.png"),
    'pit': load_image("assets/rooms/room_tiles_1/pit_tile.png"),
    'door_out': load_image("assets/rooms/room_tiles_1/floor_tile.png"),
    'door_in': load_image("assets/rooms/room_tiles_1/floor_tile_2.png")
}

pygame.init()
pygame.display.set_caption("Pygame_project")
tile_width = tile_height = 64
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bgk = pygame.Surface((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.key.set_repeat(1, 1)
player_image = load_image('assets/player/down/player_move_down_1.png')

pygame.mixer.init()

all_sprites = 0
tiles_group = 0
player_group = 0
level_now_num = 0
level_map = 0
player, level_x, level_y = 0, 0, 0
counter = 0


def main():
    global all_sprites, tiles_group, player_group, level_now_num, level_map, player, counter
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    level_now_num = 1
    level_map = load_level('map_1.txt')
    player, level_x, level_y = generate_level(level_map)
    all_sprites.add(player)
    counter = 0
    running = True
    player.hp = 3
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
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
    start_screen()
    sys.exit(main())
