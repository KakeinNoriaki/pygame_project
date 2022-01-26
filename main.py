import pygame
import sys
import os
import random


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, bullets)
        self.image = pygame.transform.scale(load_image("assets/items/arrow.png"), (64, 64))
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.speed = 20
        self.rect.bottom = y
        self.rect.centerx = x

    def update(self):
        self.rect.x += self.speed
        if self.rect.right > WIDTH:
            self.kill()


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_x, speed_y):
        super().__init__(all_sprites, bullets)
        self.image = pygame.transform.scale(load_image("assets/items/ball.png"), (64, 64))
        self.rect = self.image.get_rect()
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.max_hit_count = 10
        self.rect.bottom = y
        self.rect.centerx = x

    def update(self):
        self.rect = self.rect.move(self.speed_x, self.speed_y)
        collides = pygame.sprite.spritecollide(self, all_sprites, False)
        for coll in collides:
            if coll.__class__ is Tile:
                if coll.image == tile_images['wall'] or \
                        coll.image == tile_images['door_out'] or coll.image == tile_images['door_in']:
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
        self.arrows = 0

    def print_hp(self):
        for i in range(self.hp):
            rect = pygame.Rect(64 * i, 0, 64, 64)
            screen.blit(self.im, rect)

    def update(self):
        if self.hp > 0:
            global level_now_num, counter, boss, seconds, seconds1, minutes
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

                            self.get_out_of_the_wall_or_trap_2(coll.rect.x, coll.rect.y)
                            counter += 1

                    if coll.image == tile_images['door_out']:
                        if self.rect.collidepoint(coll.rect.center):
                            level_now_num += 1
                            load_new_room(f'assets/rooms/map_{level_now_num}.txt')
                            break

                    if coll.image == tile_images['door_in']:
                        if self.rect.collidepoint(coll.rect.center):
                            level_now_num -= 1
                            load_new_room(f'assets/rooms/map_{level_now_num}.txt')
                            break

                    if coll.image == tile_images['plate_off']:
                        if self.rect.collidepoint(coll.rect.center):
                            if level_now_num == 4:
                                self.rect.x = 1120
                                self.rect.y = 690
                            else:
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

                    if coll.image == tile_images['arrow_trap']:
                        if self.rect.collidepoint(coll.rect.center):
                            if self.arrows != 2:
                                arrow = Arrow(0, coll.rect.centery + 32)
                                all_sprites.add(arrow)
                                bullets.add(arrow)
                                self.arrows += 1

                    if coll.image == tile_images['hp_up']:
                        if self.rect.collidepoint(coll.rect.center):
                            self.hp = 3
                            coll.image = tile_images['floor']

                if coll.__class__ is Arrow:
                    if self.rect.collidepoint(coll.rect.center):
                        self.hp -= 1

                if boss.__class__ == AbstractBoss:
                    if coll.__class__ is Projectile:
                        if self.rect.collidepoint(coll.rect.center):
                            self.hp -= 1
                            coll.kill()

        else:
            seconds1 = 0
            seconds = 0
            minutes = 0
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


class AbstractBoss(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(boss_group, all_sprites)
        self.image = pygame.transform.scale(boss_image, (128, 128))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.hp = 30
        self.speed = 1
        self.on_attack = False
        self.on_attack_counter = 0
        self.attack_cool_down = 0
        self.chill = False

    def move(self, player_x, player_y):
        if self.rect.x > player_x and self.rect.y > player_y:
            for i in range(10):
                self.rect.x -= self.speed
                self.rect.y -= self.speed

        if self.rect.x < player_x and self.rect.y < player_y:
            for i in range(10):
                self.rect.x += self.speed
                self.rect.y += self.speed

        if self.rect.x > player_x and self.rect.y < player_y:
            for i in range(10):
                self.rect.x -= self.speed
                self.rect.y += self.speed

        if self.rect.x < player_x and self.rect.y > player_y:
            for i in range(10):
                self.rect.x += self.speed
                self.rect.y -= self.speed

        if self.rect.x > player_x and self.rect.y == player_y:
            for i in range(10):
                self.rect.x -= self.speed

        if self.rect.x < player_x and self.rect.y == player_y:
            for i in range(10):
                self.rect.x += self.speed

        if self.rect.x == player_x and self.rect.y > player_y:
            for i in range(10):
                self.rect.y -= self.speed

        if self.rect.x == player_x and self.rect.y < player_y:
            for i in range(10):
                self.rect.y += self.speed

    def attack_1(self, player_rect):
        attack_rect = pygame.Rect([self.rect.centerx - 96, self.rect.centery - 96, 192, 192])
        if attack_rect.colliderect(player_rect):
            return True
        return False

    def attack_2(self):
        projectile1 = Projectile(self.rect.centerx, self.rect.centery, -10, 0)
        projectile2 = Projectile(self.rect.centerx, self.rect.centery, 10, 0)
        projectile3 = Projectile(self.rect.centerx, self.rect.centery, 0, -10)
        projectile4 = Projectile(self.rect.centerx, self.rect.centery, 0, 10)

        bullets.add(projectile1)
        bullets.add(projectile2)
        bullets.add(projectile3)
        bullets.add(projectile4)

        all_sprites.add(projectile1)
        all_sprites.add(projectile2)
        all_sprites.add(projectile3)
        all_sprites.add(projectile4)

    def get_out_of_the_wall_or_trap(self, coll_rect_x, coll_rect_y):
        if self.rect.x + 1 < coll_rect_x:
            self.rect.x -= 10

        if self.rect.x - 1 > coll_rect_x:
            self.rect.x += 10

        if self.rect.y + 1 < coll_rect_y:
            self.rect.y -= 10

        if self.rect.y - 1 > coll_rect_y:
            self.rect.y += 10

    def update(self):
        collides = pygame.sprite.spritecollide(self, all_sprites, False)
        for coll in collides:
            if coll.__class__ is Tile:
                if coll.image == tile_images['wall'] or coll.image == tile_images['door_in'] \
                        or coll.image == tile_images['door_out']:
                    if self.rect.collidepoint(coll.rect.center):
                        self.get_out_of_the_wall_or_trap(coll.rect.x, coll.rect.y)


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
    new_player = None
    b = None
    y, x = 0, 0
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
                b = AbstractBoss(x, y)

            elif room[y][x] == "H":
                Tile('hp_up', x, y)

    return new_player, x, y, b


def load_new_room(room):
    global player, level_x, level_y, level_map, all_sprites, tiles_group, boss
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
                  "      Авторы",
                  "      Справка"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    f = pygame.font.SysFont('comicsansms', 60)
    text_coord = 300

    for line in intro_text:
        string_rendered = f.render(line, True, pygame.Color('yellow'))
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

                if 14 * 30 <= event.pos[0] <= WIDTH / 2 + 120 and 300 <= event.pos[1] <= 420:
                    pygame.mixer.music.load('assets/tracks/main_theme')
                    pygame.mixer.music.set_volume(0.01)
                    pygame.mixer.music.play()
                    main()

                if 14 * 30 <= event.pos[0] <= WIDTH / 2 + 120 and 420 <= event.pos[1] <= 540:
                    terminate()

                if 14 * 30 <= event.pos[0] <= WIDTH / 2 + 120 and 540 <= event.pos[1] <= 660:
                    authors_screen()

                if 14 * 30 <= event.pos[0] <= WIDTH / 2 + 120 and 660 <= event.pos[1] <= 780:
                    FAQ()

        pygame.display.flip()
        clock.tick(FPS)


def authors_screen():
    intro_text = [
                  "Максим 'Kakein Noriaki' Князев",
                  "Артём 'Easy711' Мохов",
                  "Владислав Соловцов"
                 ]

    fon = pygame.transform.scale(load_image('fon_2.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    f = pygame.font.SysFont('comicsansms', 60)
    text_coord = 50

    for line in intro_text:
        string_rendered = f.render(line, True, pygame.Color('yellow'))
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
    f = pygame.font.SysFont('comicsansms', 80)
    text_coord = 300

    for line in intro_text:
        string_rendered = f.render(line, True, pygame.Color('yellow'))
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


def FAQ():
    intro_text = [
        "W, A, S, D - управление",
        "LBM - удар",
        "Для прохождения игры",
        "необходимо пройти 6 комнат и 1 босса", "",
        "Удачи и приятной игры"
    ]

    fon = pygame.transform.scale(load_image('fon_2.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    f = pygame.font.SysFont('comicsansms', 60)
    text_coord = 50

    for line in intro_text:
        string_rendered = f.render(line, True, pygame.Color('yellow'))
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


def wim_screen():
    global minutes, seconds
    intro_text = ["Игра окончена",
                  f"Ваш результат: {minutes}:{seconds}"]

    pygame.mixer.music.load('assets/tracks/main_menu_music')
    pygame.mixer.music.set_volume(0.01)
    pygame.mixer.music.play()

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    f = pygame.font.SysFont('comicsansms', 80)
    text_coord = 300

    for line in intro_text:
        string_rendered = f.render(line, True, pygame.Color('yellow'))
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
    'arrow_trap': load_image("assets/rooms/room_tiles_1/arrow_trap.png"),
    'hp_up': load_image("assets/rooms/room_tiles_1/hp_up.png")
}

pygame.init()
pygame.display.set_caption("Pygame_project")
tile_width = tile_height = 64
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bgk = pygame.Surface((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.key.set_repeat(1, 1)
player_image = load_image('assets/player/down/player_move_down_1.png')
boss_image = load_image("assets/boss/miniboss7.png")
pygame.mixer.init()

walk_right = [
              pygame.image.load("assets/player/right/player_move_right_1.png"),
              pygame.image.load("assets/player/right/player_move_right_2.png"),
              pygame.image.load("assets/player/right/player_move_right_3.png")
             ]

walk_left = [
             pygame.image.load("assets/player/left/player_move_left_1.png"),
             pygame.image.load("assets/player/left/player_move_left_2.png"),
             pygame.image.load("assets/player/left/player_move_left_3.png")
            ]

walk_forward = [
                pygame.image.load("assets/player/up/player_move_up_1.png"),
                pygame.image.load("assets/player/up/player_move_up_2.png"),
                pygame.image.load("assets/player/up/player_move_up_3.png")
               ]

walk_down = [
             pygame.image.load("assets/player/down/player_move_down_1.png"),
             pygame.image.load("assets/player/down/player_move_down_2 .png"),
             pygame.image.load("assets/player/down/player_move_down_3.png")
            ]

attack_right = [
                pygame.image.load("assets/player/attack_right/player_attack_right_1.png"),
                pygame.image.load("assets/player/attack_right/player_attack_right_2.png"),
                pygame.image.load("assets/player/attack_right/player_attack_right_3.png"),
                pygame.image.load("assets/player/attack_right/player_attack_right_4.png")
               ]

attack_left = [
               pygame.image.load("assets/player/attack_left/player_attack_left_1.png"),
               pygame.image.load("assets/player/attack_left/player_attack_left_2.png"),
               pygame.image.load("assets/player/attack_left/player_attack_left_3.png"),
               pygame.image.load("assets/player/attack_left/player_attack_left_4.png")
              ]

attack_down = [
               pygame.image.load("assets/player/attack_down/player_attack_down_1.png"),
               pygame.image.load("assets/player/attack_down/player_attack_down_2.png"),
               pygame.image.load("assets/player/attack_down/player_attack_down_3.png"),
               pygame.image.load("assets/player/attack_down/player_attack_down_4.png")
              ]

attack_up = [
             pygame.image.load("assets/player/attack_up/player_attack_up_1.png"),
             pygame.image.load("assets/player/attack_up/player_attack_up_2.png"),
             pygame.image.load("assets/player/attack_up/player_attack_up_3.png"),
             pygame.image.load("assets/player/attack_up/player_attack_up_4.png")
            ]

playerStand = [pygame.image.load("assets/player/down/player_move_down_1.png")]

boss_attack = [
               pygame.transform.scale(pygame.image.load("assets/boss/miniboss7.png"), [128, 128]),
               pygame.transform.scale(pygame.image.load("assets/boss/miniboss8.png"), [128, 128]),
               pygame.transform.scale(pygame.image.load("assets/boss/miniboss9.png"), [128, 128]),
               pygame.transform.scale(pygame.image.load("assets/boss/miniboss10.png"), [128, 128]),
               pygame.transform.scale(pygame.image.load("assets/boss/miniboss11.png"), [128, 128]),
               pygame.transform.scale(pygame.image.load("assets/boss/miniboss12.png"), [128, 128]),
               pygame.transform.scale(pygame.image.load("assets/boss/miniboss13.png"), [128, 128]),
               pygame.transform.scale(pygame.image.load("assets/boss/miniboss14.png"), [128, 128])
              ]

boss_stand = [pygame.image.load("assets/boss/miniboss7.png")]

#  тут мы объявляем целую кучу переменыых что их потом использовать голабпльно
#  код после такой фигни становиться не очень читаемым, но поправлять нам это было некогда
#  Всё что сзязанно с группами спрайтов
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
#  всё что связано с уровнями
level_now_num = 0
level_map = 0
level_x = 0
level_y = 0
#  это затычки для игрока и босса
player = 0
boss = None
#  всё для анимаций
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
pause1 = False
attack_on = False
boss_in_attack = False
boss_attack_on = False
animCount2 = 0
#  всё для таймера
minutes = 0
time_score = 0
seconds = 0
seconds1 = 0
#  это для шрифта таймера
font = pygame.font.Font(None, 68)
black = (0, 0, 0)


def main():
    #  тут мы немного накосячили со структурой программы и образовался такой вот костыль
    #  поправить мы его не можем, т.к. слишком ко многому эта куча привязана и нам лень
    global all_sprites, tiles_group, player_group,\
        level_now_num, level_map, player, counter,\
        animCount, left, right, forward, down,\
        bullets, a, animCount1, left_attack,\
        right_attack, forward_attack, down_attack,\
        attack, boss_group, boss, minutes, seconds,\
        time_score, font, black, pause1, seconds1,\
        boss, attack_on, boss_attack, boss_stand, \
        boss_in_attack, animCount2, boss_attack_on
    #  очищаем группы спрайтов
    bullets = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    boss_group = pygame.sprite.Group()
    #  это нужно для начала игры
    level_now_num = 1
    level_map = load_level('assets/rooms/map_1.txt')
    player, _, __, boss = generate_level(level_map)

    all_sprites.add(player)
    running = True
    player.hp = 3
    pause = False
    #  основой цикл
    #  !!!ВЫСОКАЯ ВЕРОЯТНОСТЬ ВСТРЕТИТЬ НЕ ОЧЕНЬ АККУРАТНЫЙ КОД!!!
    while running:

        clock.tick(FPS)
        for event in pygame.event.get():
            if not pause:
                if event.type == pygame.QUIT:
                    running = False
                #  тут мы обрабатываем нажатия
                #  следующая строчка позволяет считывать много нажатий сразу, но имеет много минусов
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
                # тут мы проверяем куда игрок атакуем что бы позже нарисовать правильную анимацию
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

                if not (keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a]
                        or keys[pygame.K_d]) and event.type == pygame.MOUSEBUTTONDOWN:
                    left_attack = False
                    right_attack = False
                    forward_attack = False
                    down_attack = False
                    left = False
                    right = False
                    forward = False
                    down = False
                    attack = True
            # это на случай паузы
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
                    string_rendered = font.render(line, True, pygame.Color('yellow'))
                    intro_rect = string_rendered.get_rect()
                    text_coord += 30
                    intro_rect.top = text_coord
                    intro_rect.x = WIDTH / 2 - 600
                    text_coord += intro_rect.height
                    screen.blit(string_rendered, intro_rect)

                run = True
                while run:
                    for e in pygame.event.get():
                        if e.type == pygame.QUIT:
                            terminate()

                        elif e.type == pygame.MOUSEBUTTONDOWN:
                            pause = False
                            run = False

                    pygame.display.flip()
                    clock.tick(FPS)
                    pygame.display.flip()
                    clock.tick(FPS)

        if not pause:
            #  если босс существует то можно с ним делать штуки
            if boss.__class__ == AbstractBoss:

                if boss.attack_1(player.rect):
                    if not boss.chill:
                        player.hp -= 1
                        #  небольшой стан босса что бы его можно было победить
                        boss.chill = True
                        boss.on_attack = True
                        boss_in_attack = True
                #  тут может иногда слишком много прокать
                elif random.randint(0, 100) == 5:
                    boss.attack_2()
                    boss.chill = True
                    boss.on_attack = True
                #  если первые пара вариков не произошли
                else:
                    if not boss.on_attack:
                        boss.move(player.rect.x, player.rect.y)

                boss.on_attack_counter += 1
                boss.attack_cool_down += 1
                #  на случай если игрок смог победить босса
                if boss.hp <= 0:
                    boss.kill()
                    minutes = 0
                    seconds = 0
                    seconds1 = 0
                    win_screen()
                # откатываем все станы
                if boss.on_attack_counter >= 120:
                    boss.on_attack = False
                    boss.on_attack_counter = 0
                if boss.attack_cool_down >= 720:
                    boss.chill = False
                    boss.attack_cool_down = 0
            # отрисовка всего
            screen.fill((180, 35, 122))
            all_sprites.update()
            all_sprites.draw(screen)

            if animCount + 1 >= 60:
                animCount = 0
            # отрисовка игрока и его анимаций
            if not attack_on:
                if left:
                    screen.blit(walk_left[animCount // 20], (player.rect.x, player.rect.y))
                    animCount += 1

                if right:
                    screen.blit(walk_right[animCount // 20], (player.rect.x, player.rect.y))
                    animCount += 1

                if forward:
                    screen.blit(walk_forward[animCount // 20], (player.rect.x, player.rect.y))
                    animCount += 1

                if down:
                    screen.blit(walk_down[animCount // 20], (player.rect.x, player.rect.y))
                    animCount += 1

                if not (forward or left or right or down):
                    screen.blit(playerStand[0], (player.rect.x, player.rect.y))
            # отрисовка анимаций атак игрока
            if left_attack:
                screen.blit(attack_left[animCount1 // 15], (player.rect.x, player.rect.y))
                animCount1 += 1
                if animCount1 + 1 >= 60:
                    animCount1 = 0
                    left_attack = False
                    attack_on = False
                    if boss.__class__ == AbstractBoss:
                        attack_rect = pygame.Rect([player.rect.centerx - 96, player.rect.centery - 96, 192, 192])
                        if attack_rect.colliderect(boss.rect):
                            boss.hp -= 1
                            print(boss.hp)

            if right_attack:
                screen.blit(attack_right[animCount1 // 15], (player.rect.x, player.rect.y))
                animCount1 += 1
                if animCount1 + 1 >= 60:
                    animCount1 = 0
                    right_attack = False
                    attack_on = False
                    if boss.__class__ == AbstractBoss:
                        attack_rect = pygame.Rect([player.rect.centerx - 96, player.rect.centery - 96, 192, 192])
                        if attack_rect.colliderect(boss.rect):
                            boss.hp -= 1
                            print(boss.hp)

            if forward_attack:
                screen.blit(attack_up[animCount1 // 15], (player.rect.x, player.rect.y))
                animCount1 += 1
                if animCount1 + 1 >= 60:
                    animCount1 = 0
                    forward_attack = False
                    attack_on = False
                    if boss.__class__ == AbstractBoss:
                        attack_rect = pygame.Rect([player.rect.centerx - 96, player.rect.centery - 96, 192, 192])
                        if attack_rect.colliderect(boss.rect):
                            boss.hp -= 1
                            print(boss.hp)

            if down_attack:
                screen.blit(attack_down[animCount1 // 15], (player.rect.x, player.rect.y))
                animCount1 += 1
                if animCount1 + 1 >= 60:
                    animCount1 = 0
                    down_attack = False
                    attack_on = False
                    if boss.__class__ == AbstractBoss:
                        attack_rect = pygame.Rect([player.rect.centerx - 96, player.rect.centery - 96, 192, 192])
                        if attack_rect.colliderect(boss.rect):
                            boss.hp -= 1
                            print(boss.hp)

            if attack:
                screen.blit(attack_down[animCount1 // 15], (player.rect.x, player.rect.y))
                animCount1 += 1
                if animCount1 + 1 >= 60:
                    animCount1 = 0
                    attack = False
                    attack_on = False
                    if boss.__class__ == AbstractBoss:
                        attack_rect = pygame.Rect([player.rect.centerx - 96, player.rect.centery - 96, 192, 192])
                        if attack_rect.colliderect(boss.rect):
                            boss.hp -= 1
                            print(boss.hp)
            # отрисовка анимаций атак босса
            if boss.__class__ == AbstractBoss:
                if boss_in_attack:
                    boss_attack_on = True
                    screen.blit(boss_attack[animCount2 // 8], (boss.rect.x, boss.rect.y))
                    animCount2 += 1
                    print(animCount2)
                    if animCount2 + 1 >= 60:
                        animCount2 = 0
                        boss_in_attack = False

                if not boss_in_attack:
                    if not boss_attack_on:
                        screen.blit(boss_stand[0], (boss.rect.x, boss.rect.y))
            # рисуем хп игрока
            player.print_hp()
            # рисуем таймер
            text = font.render(f"Время: {str(minutes)}:{str(seconds)}", True, black)
            player.print_hp()
            seconds1 += 1
            seconds = seconds1 // 60
            if seconds == 60:
                minutes += 1
                seconds1 = 0
            screen.blit(text, [1000, 10])
            #  Рисуем снаряды
            bullets.update()
            for bullet in bullets:
                screen.blit(bullet.image, bullet.rect)
            boss_group.update()
        boss_group.draw(screen)

        pygame.display.flip()


if __name__ == '__main__':
    start_screen()
    sys.exit(main())
