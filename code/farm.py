import pygame

from data import *
from buttons import Button
from random import random, choice, randint


WIDTH, HEIGHT = pygame.display.set_mode().get_size()  # размеры окна
egg_speed = 3  # скорость падения предметов (зависит от выбранной сложности)
player_speed = 8  # скорость игрока
FPS = 60  # количество кадров в секунду
size = (350, 350)  # размеры персонажа (фермера)


# Падающие предметы
class Items(pygame.sprite.Sprite):
    # Изображения предметов
    img_list = (change_size(Images.egg, (150, 100)), change_size(Images.apple, (100, 80)),
                change_size(Images.cabbage, (150, 130)))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = choice(self.img_list)  # Случайный выбор изображений
        self.mask = pygame.mask.from_surface(self.image)  # маска объекта-изображения

        # Квадрат изображения
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, WIDTH - self.rect.width)
        self.rect.y = 0

        # Загрузка звука падения предмета в тележку фермера
        self.sound = pygame.mixer.Sound('../data/sounds/catch.mp3')
        self.sound.set_volume(sound_parameter)

    def update(self):
        global lives, score, farmer
        self.rect = self.rect.move(0, egg_speed)  # передвижение предмета (падение)

        # обработка столкновения по маске
        if pygame.sprite.collide_mask(self, farmer):
            score += 1
            self.kill()
            self.sound.play()

        # обработка падения предмета (если игрок не смог поймать предмет)
        if self.rect.y > HEIGHT:
            lives -= 1
            self.kill()


# фермер
class Farmer(pygame.sprite.Sprite):

    # Загрузка изображений (фермер с пустой тележкой)
    empty_left = [change_size(img, size) for img in Images.left]
    empty_right = [change_size(img, size) for img in Images.right]

    # Спрайты персонажа с наполовину полной тележкой
    half_left = [change_size(img, size) for img in Images.half_left]
    half_right = [change_size(img, size) for img in Images.half_right]

    # Спрайты персонажа с наполненной тележкой
    full_left = [change_size(img, size) for img in Images.full_left]
    full_right = [change_size(img, size) for img in Images.full_right]

    def __init__(self, *group):
        super().__init__(*group)
        self.direction = -1  # направление движения фермера (-1 - влево) (1 - вправо) (0 - нет движения)
        self.anim = 0  # переменная для анимирования фермера

        # Группы спрайтов (с фермером, который движется влево и вправо соответственно)
        self.left_sprites = self.empty_left[:]
        self.right_sprites = self.empty_right[:]

        # Изображение фермера, маска
        self.image = self.left_sprites[self.anim]
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT - 350

        # Загрузка звука ходьбы фермера (по траве)
        self.sound = pygame.mixer.Sound('../data/sounds/going.mp3')
        self.sound.set_volume(sound_parameter)
        self.sound_playing = True  # флаг для проигрывания звука (только если фермер идёт)

    def update(self, stay=False):
        collide_border = self.collide_window_border()  # столкнулся ли фермер с границей игрового окна

        # Проигрывем звук, если фермер идёт и все условия для этого соблюдаются:
        if self.sound_playing and not collide_border and not stay:
            self.sound_playing = False
            self.sound.play()

        # Обновляем группы спрайтов в соответствии со счётом
        self.choose_sprite()

        # если персонаж не столкнулся с границей окна - анимируем его
        if not collide_border and not stay:
            self.anim += 0.1
            if self.anim > 2:
                self.anim = 0

        # если персонаж остановился - приглушаем звук ходьбы
        if stay or collide_border:
            self.sound.stop()
            self.sound_playing = True

        # обновление персонажа, если он идёт вправо
        if self.direction == 1:
            self.image = self.right_sprites[int(self.anim)]

        # обновление персонажа, если он идёт влево
        elif self.direction == -1:
            self.image = self.left_sprites[int(self.anim)]

        # обновление маски изображения
        self.mask = pygame.mask.from_surface(self.image)

        if not collide_border and not stay:
            self.rect = self.rect.move(player_speed * self.direction, 0)

    # Обновление группы спрайтов
    def choose_sprite(self):
        global score
        if 5 <= score <= 15:
            self.left_sprites = self.half_left[:]
            self.right_sprites = self.half_right[:]

        elif score > 15:
            self.left_sprites = self.full_left
            self.right_sprites = self.full_right

    # проверка столкновения персонажа с границами окна игры
    def collide_window_border(self):
        return not (-19 <= self.rect.x + player_speed * self.direction <= WIDTH - 335)


# Игра: Весёлый фермер
def HappyFarmer(function):
    # Глобальные переменные, которые используются в классах спрайтов
    global score, lives, farmer, game_font, sound_parameter

    sound_parameter = get_volume()  # параметр громкости

    # подключение к БД
    connect = sqlite3.connect('../settings/records.sqlite')
    cursor = connect.cursor()
    data = cursor.execute('SELECT * from data WHERE game="farmer"').fetchone()
    # Берём из БД текущий рекорд и проверяем, играет ли игрок в эту игру впервый раз (для вступления)
    is_played = data[3]

    # Инициализация игры
    pygame.init()
    pygame.display.set_caption('Весёлая ферма')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    farm_background = pygame.transform.scale(Images.farm_background, (WIDTH, HEIGHT))  # фон игры

    # Звук игры
    pygame.mixer.stop()  # приглушаем все звуки
    farm_sound = pygame.mixer.Sound('../data/sounds/farm_sound.mp3')  # звуки фермы (природы) - фоновый звук
    farm_sound.set_volume(sound_parameter)  # громкость звука - 50%
    farm_sound.play()  # проигрываем звук

    font_scale = 32  # размер игрового шрифта
    game_font = pygame.font.Font('../data/fonts/appetite.ttf', font_scale)  # шрифт

    # Если игрок впервые играет в данную игру - проводим краткий инструктаж (если так можно выразиться):
    if not is_played:
        get_instruction(screen, farm_background, game_font, '../settings/farm_i.txt', 'farmer')

    """ Инициализация спрайтов, изображений, музыки """
    # Игровые изображения (трава, сердца)
    grass = pygame.transform.scale(Images.grass, (WIDTH, 100))
    heart_img = Images.heart  # сердца
    heart_width = heart_img.get_width()  # ширина сердечка

    score = 0  # счёт
    lives = 5  # прав на ошибку (жизней)

    paused = False  # поставлена ли игра на паузу
    wanna_quit = False  # если игрок нажимает на Esc, то спрашиваем, желает ли он завершить игру (флаг)
    all_items = pygame.sprite.Group()  # все падающие предметы

    farmer_group = pygame.sprite.Group()  # фермер
    farmer = Farmer(farmer_group)  # экземпляр класса фермера

    # Главный цикл игры
    clock = pygame.time.Clock()
    running = True
    while running:
        # отрисовка всех изображений на экране
        screen.blit(farm_background, (0, 0))  # отрисовка фона
        screen.blit(grass, (0, HEIGHT - 100))  # отрисовка травы (это не то, о чём вы подумали)
        all_items.draw(screen)  # отрисовка падающих предметов
        farmer_group.draw(screen)  # отрисовка фермера

        # отображение оставшегося количества сердец
        for i in range(lives):
            screen.blit(heart_img, (10 + i * (heart_width + 5), 10))

        # Проверка: поставлена ли игра на паузу или желает ли игрок выйти:
        if paused:
            farmer.sound.stop()  # приглушаем звук ходьбы фермера
            pause(screen, game_font)  # пауза
        elif wanna_quit:
            farmer.sound.stop()
            pause(screen, game_font, text='Вы хотите выйти? Нажмите ENTER, чтобы завершить игру')
        else:
            all_items.update()  # обновляем падающие предметы, если игра не поставлена на паузу

        # отображение счета в углу
        screen.blit(game_font.render(f"Счёт: {score}", True, (0, 0, 0)), (WIDTH - 150, 10))

        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()  # закрытие всей игры

            # Работаем с паузой и остановкой игры на Esc + Enter (последовательно):
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and not wanna_quit:
                    paused = not paused
                elif event.key == pygame.K_ESCAPE:  # Попытка завершения игры блокирует паузу
                    wanna_quit = not wanna_quit
                    paused = False
                elif event.key == pygame.K_RETURN and wanna_quit:
                    running = False

        # если игра не на паузе - продолжаем обработку событий:
        if not paused and not wanna_quit:
            stay = False  # флаг для проверки: стоит ли фермер на месте или движется (объяснение в классе фермера)
            keys = pygame.key.get_pressed()
            # обрабатываем движение фермера влево
            if keys[pygame.K_LEFT]:
                farmer.direction = -1
            # обрабатываем движение фермера вправо
            elif keys[pygame.K_RIGHT]:
                farmer.direction = 1
            # если фермер вообще не движется
            else:
                stay = True
            farmer_group.update(stay)

            # Добавление нового яйца с вероятностью 2% (за один игровой кадр)
            if random() < 0.02:
                Items(all_items)

            # если количество жизней кончилось - завершаем игру
            if not lives:
                break

        clock.tick(FPS)
        pygame.display.flip()

    # Функция окончания игры:
    game_over(screen, game_font, 'farmer', score, HappyFarmer, function, Images.farm_over_buttons, farm_background,
              'Время вышло!', 'Собрано продуктов', Button)
