import pygame
import sys
import os


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, bullets)
        self.image = pygame.transform.scale(load_image("assets/items/arrow.png"), (WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 20

    def update(self):
        self.rect.x += self.speedy
        if self.rect.right > WIDTH:
            self.kill()


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
        self.im = pygame.transform.scale(load_image("assets/items/heart.png"), [64, 64])
        self.count = 0

    def print_hp(self):
        for i in range(self.hp):
            rect = pygame.Rect(64 * i, 0, 64, 64)
            screen.blit(self.im, rect)

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

                    if coll.image == tile_images['plate_off']:
                        if self.rect.collidepoint(coll.rect.center):
                            coll.image = tile_images['plate_on']
                            usl = True

                            for i in tiles_group:
                                if i.image == tile_images['plate_off']:
                                    usl = False
                                    break

                            if usl:
                                tiles_group.sprites()[119].image = tile_images['door_out']
                                tiles_group.sprites()[139].image = tile_images['door_out']
                                tiles_group.update()
                                tiles_group.draw(screen)

                    if coll.image == tile_images['fake_floor']:
                        if self.rect.collidepoint(coll.rect.center):
                            coll.image = tile_images['spike']
                            self.get_out_of_the_wall_or_trap_2(coll.rect.x, coll.rect.y)

        else:
            game_over()

    def get_out_of_the_wall_or_trap(self, coll_rect_x, coll_rect_y):
        if self.rect.x + 1 < coll_rect_x:
            self.rect.x -= 10
        if self.rect.x - 1 > coll_rect_x:
            self.rect.x += 10
        if self.rect.y + 1 < coll_rect_y:
            self.rect.y -= 10
        if self.rect.y - 1 > coll_rect_y:
            self.rect.y += 10

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
    b = 0
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

            elif room[y][x] == 'P':
                Tile('plate_off', x, y)

            elif room[y][x] == 'F':
                Tile('fake_floor', x, y)

            elif room[y][x] == 'A':
                Tile('arrow_trap', x, y)

            elif room[y][x] == "!":
                Tile('floor', x, y)
                b = AbstractBoss()

    return new_player, x, y, b


def load_new_room(room):
    global player, level_x, level_y, level_map, all_sprites, tiles_group
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player.kill()
    level_map = load_level(room)
    player, level_x, level_y, boss = generate_level(level_map)
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

                if 14 * 30 <= event.pos[0] <= WIDTH / 2 + 120 and 300 <= event.pos[1] <= 420:
                    pygame.mixer.music.load('assets/tracks/main_theme')
                    pygame.mixer.music.set_volume(0.01)
                    pygame.mixer.music.play()
                    main()

                if 14 * 30 <= event.pos[0] <= WIDTH / 2 + 120 and 420 <= event.pos[1] <= 540:
                    terminate()

                if 14 * 30 <= event.pos[0] <= WIDTH / 2 + 120 and 540 <= event.pos[1] <= 660:
                    authors_screen()

        pygame.display.flip()
        clock.tick(FPS)


def authors_screen():
    intro_text = ["Максим 'Kakein Noriaki' Князев",
                  "Артём 'Easy711' Мохов",
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
FPS = 120
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
    'door_in': load_image("assets/rooms/room_tiles_1/floor_tile_2.png"),
    'plate_on': load_image("assets/rooms/room_tiles_1/plate_on.png"),
    'plate_off': load_image("assets/rooms/room_tiles_1/plate_off.png"),
    'fake_floor': load_image("assets/rooms/room_tiles_1/fake_floor.png"),
    'arrow_trap': load_image("assets/rooms/room_tiles_1/arrow_trap.png")
}

pygame.init()
pygame.display.set_caption("Pygame_project")
tile_width = tile_height = 64
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bgk = pygame.Surface((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.key.set_repeat(1, 1)
player_image = load_image('assets/player/down/player_move_down_1.png')
boss_image = load_image('assets/player/down/player_move_down_1.png')
pygame.mixer.init()

walkright = [pygame.image.load("assets/player/right/player_move_right_1.png"),
             pygame.image.load("assets/player/right/player_move_right_2.png"),
             pygame.image.load("assets/player/right/player_move_right_3.png")]

walkleft = [pygame.image.load("assets/player/left/player_move_left_1.png"),
            pygame.image.load("assets/player/left/player_move_left_2.png"),
            pygame.image.load("assets/player/left/player_move_left_3.png")]

walkforward = [pygame.image.load("assets/player/up/player_move_up_1.png"),
               pygame.image.load("assets/player/up/player_move_up_2.png"),
               pygame.image.load("assets/player/up/player_move_up_3.png")]

walkdown = [pygame.image.load("assets/player/down/player_move_down_1.png"),
            pygame.image.load("assets/player/down/player_move_down_2 .png"),
            pygame.image.load("assets/player/down/player_move_down_3.png")]

attackright = [pygame.image.load("assets/player/attack_right/player_attack_right_1.png"),
               pygame.image.load("assets/player/attack_right/player_attack_right_2.png"),
               pygame.image.load("assets/player/attack_right/player_attack_right_3.png"),
               pygame.image.load("assets/player/attack_right/player_attack_right_4.png")]

attackleft = [pygame.image.load("assets/player/attack_left/player_attack_left_1.png"),
              pygame.image.load("assets/player/attack_left/player_attack_left_2.png"),
              pygame.image.load("assets/player/attack_left/player_attack_left_3.png"),
              pygame.image.load("assets/player/attack_left/player_attack_left_4.png")]

attackdown = [pygame.image.load("assets/player/attack_down/player_attack_down_1.png"),
              pygame.image.load("assets/player/attack_down/player_attack_down_2.png"),
              pygame.image.load("assets/player/attack_down/player_attack_down_3.png"),
              pygame.image.load("assets/player/attack_down/player_attack_down_4.png")]

attackup = [pygame.image.load("assets/player/attack_up/player_attack_up_1.png"),
            pygame.image.load("assets/player/attack_up/player_attack_up_2.png"),
            pygame.image.load("assets/player/attack_up/player_attack_up_3.png"),
            pygame.image.load("assets/player/attack_up/player_attack_up_4.png")]


playerStand = [pygame.image.load("assets/player/down/player_move_down_1.png")]

bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
level_now_num = 0
level_map = 0
player = 0
boss = 0
level_x = 0
level_y = 0
counter = 0
animCount = 0
animCount1 = 0
a = True
left = False
right = False
forward = False
down = False
left_attack = False
right_attack = False
forward_attack = False
down_attack = False
attack = False


def main():
    global all_sprites, tiles_group, player_group, level_now_num, level_map, player, counter,\
        animCount, left, right, forward, down, bullets, a, animCount1,left_attack, right_attack, forward_attack, down_attack, attack

    bullets = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    level_now_num = 1
    level_map = load_level('map_1.txt')
    player, _, __, boss = generate_level(level_map)
    all_sprites.add(player)
    running = True
    player.hp = 3
    pause = False
    while running:

        clock.tick(FPS)
        for event in pygame.event.get():
            if not pause:
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

                if keys[pygame.K_ESCAPE]:
                    pause = True

                if not (keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]):
                    left = False
                    right = False
                    forward = False
                    down = False

                if keys[pygame.K_a] and event.type == pygame.MOUSEBUTTONDOWN:
                    left_attack = True
                    right_attack = False
                    forward_attack = False
                    down_attack = False

                if keys[pygame.K_s] and event.type == pygame.MOUSEBUTTONDOWN:
                    left_attack = False
                    right_attack = False
                    forward_attack = False
                    down_attack = True

                if keys[pygame.K_w] and event.type == pygame.MOUSEBUTTONDOWN:
                    left_attack = False
                    right_attack = False
                    forward_attack = True
                    down_attack = False

                if keys[pygame.K_d] and event.type == pygame.MOUSEBUTTONDOWN:
                    left_attack = False
                    right_attack = True
                    forward_attack = False
                    down_attack = False

                if not (keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]) and event.type == pygame.MOUSEBUTTONDOWN:
                    left_attack = False
                    right_attack = False
                    forward_attack = False
                    down_attack = False
                    left = False
                    right = False
                    forward = False
                    down = False
                    attack = True

            else:
                intro_text = ["                                   Пауза",
                              "Для продолжения нажните любую кнопку мыши"]

                pygame.mixer.music.load('assets/tracks/main_menu_music')
                pygame.mixer.music.set_volume(0.01)
                pygame.mixer.music.play()
                fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
                screen.blit(fon, (0, 0))
                font = pygame.font.SysFont('comicsansms', 50)
                text_coord = 300

                for line in intro_text:
                    string_rendered = font.render(line, 1, pygame.Color('yellow'))
                    intro_rect = string_rendered.get_rect()
                    text_coord += 30
                    intro_rect.top = text_coord
                    intro_rect.x = WIDTH / 2 - 600
                    text_coord += intro_rect.height
                    screen.blit(string_rendered, intro_rect)
                    run = True

                while run:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            terminate()

                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            pause = False
                            run = False

                    pygame.display.flip()
                    clock.tick(FPS)
                    pygame.display.flip()
                    clock.tick(FPS)

        if not pause:
            screen.fill((180, 35, 122))
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

            if left_attack:
                a = True
                while a:
                    print(animCount1)
                    screen.blit(attackleft[animCount1 // 15], (player.rect.x, player.rect.y))
                    animCount1 += 1
                    if animCount1 + 1 >= 60:
                        animCount1 = 0
                        a = False
                        left_attack = False

            if right_attack:
                a = True
                while a:
                    print(animCount1)
                    screen.blit(attackright[animCount1 // 15], (player.rect.x, player.rect.y))
                    animCount1 += 1
                    if animCount1 + 1 >= 60:
                        animCount1 = 0
                        a = False
                        right_attack = False

            if forward_attack:
                a = True
                while a:
                    print(animCount1)
                    screen.blit(attackup[animCount1 // 15], (player.rect.x, player.rect.y))
                    animCount1 += 1
                    if animCount1 + 1 >= 60:
                        animCount1 = 0
                        a = False
                        forward_attack = False

            if down_attack:
                a = True
                while a:
                    print(animCount1)
                    screen.blit(attackdown[animCount1 // 15], (player.rect.x, player.rect.y))
                    animCount1 += 1
                    if animCount1 + 1 >= 60:
                        animCount1 = 0
                        a = False
                        down_attack =  False

            if attack:
                a = True
                while a:
                    print(animCount1)
                    screen.blit(attackdown[animCount1 // 15], (player.rect.x, player.rect.y))
                    animCount1 += 1
                    if animCount1 + 1 >= 60:
                        animCount1 = 0
                        a = False
                        attack = False

            player.print_hp()

        pygame.display.flip()


if __name__ == '__main__':
    start_screen()
    sys.exit(main())
