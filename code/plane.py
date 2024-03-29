from data import *
from time import time
from buttons import Button
from random import shuffle


# Количество кадров в секунду, ширина и высота монитора игрока:
FPS = 180
WIDTH, HEIGHT = pygame.display.set_mode().get_size()


# Генерация деталей самолёта на игровом поле (в игровом окне):
def generate_details():
    x_s = 50  # рисуем детали в ряд
    indexes = list(range(6))  # случайные индексы (0, ..., 5)
    shuffle(indexes)  # перемешиваем список
    dgroup = pygame.sprite.Group()  # группа спрайтов (деталей)
    for i in indexes:  # выбор детали и отрисовка
        Detail(i, x_s, dgroup)
        x_s += WIDTH // 6
    return dgroup


# Класс для работы с деталями самолёта:
class Detail(pygame.sprite.Sprite):
    # картинки деталей самолёта
    details_images = (Images.fuselage,  # фюзеляж
                      Images.cabine,  # кабина
                      Images.rudder,  # хвост
                      Images.wing,  # крылья
                      Images.engine,  # двигатель
                      Images.chassis)  # шасси

    def __init__(self, index, x, *group, y=100):
        super().__init__(*group)
        self.moving = False  # можно ли передвигать деталь
        self.mouse_previous_pos = pygame.mouse.get_pos()  # предыдущая позиция мыши
        self.initial_coordinates = (x, y)  # начальные координаты детали
        self.queue = index + 1  # порядок детали
        self.image = pygame.transform.scale(self.details_images[index], (150, 150))
        self.mask = pygame.mask.from_surface(self.image)  # маска

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Загрузка звуков сварки и неправильного выбора детали:
        self.sound = pygame.mixer.Sound('../data/sounds/svarka.mp3')
        self.sound.set_volume(sound_parameter)
        self.incorrect_sound = pygame.mixer.Sound('../data/sounds/plane_incorrect.mp3')
        self.incorrect_sound.set_volume(sound_parameter)

    def update(self, event):
        mouse_pos = pygame.mouse.get_pos()

        # обработка клика левой кнопкой мыши по маске детали (разрешаем передвижение если все условия соблюдены):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mask_pos = mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y
                if self.rect.collidepoint(*mouse_pos) and self.mask.get_at(mask_pos):
                    self.moving = True

        # обработка передвижения мыши: передвигаем деталь, если это разрешено:
        if event.type == pygame.MOUSEMOTION:
            if self.moving:
                x, y = mouse_pos[0] - self.mouse_previous_pos[0], mouse_pos[1] - self.mouse_previous_pos[1]
                self.rect.x += x
                self.rect.y += y
            self.mouse_previous_pos = mouse_pos

        # Если предмет достиг стенда и порядок добавления - верный, то удаляем его, обновляем спрайт самолёта,
        # иначе - возвращаем деталь на место
        if event.type == pygame.MOUSEBUTTONUP:
            self.moving = False
            if pygame.sprite.collide_mask(self, stand) and self.queue != order[-1] + 1:
                self.incorrect_sound.play()

            if not pygame.sprite.collide_mask(self, stand) or self.queue != order[-1] + 1:
                self.rect.x, self.rect.y = self.initial_coordinates
            else:
                order.append(self.queue)
                if 1 < self.queue < 6:
                    self.sound.play()
                self.kill()


# Класс для отображения стенда (статичный):
class Stand(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = Images.stand
        self.image = pygame.transform.scale(self.image, (600, 500))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - self.rect.width // 2
        self.rect.y = HEIGHT - 250


# Класс самолёта (собирается по частям):
class Plane(pygame.sprite.Sprite):
    progress = (Images.airplane0,
                Images.airplane1,  # 1 - только фюзеляж
                Images.airplane2,  # 2 - фюзеляж и кабина пилота
                Images.airplane3,  # 3 - фюзеляж, кабина, хвост
                Images.airplane4,  # 4 - фюзеляж, кабина, хвост, крылья
                Images.airplane5,  # 5 - всё, кроме шасси
                Images.airplane6)  # 6 - самолёт собран

    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(self.progress[0], (700, 300))  # загрузка и трансформирование изображения
        self.fly = False  # самолёт улетает с площадки, только если он построен
        self.play_sound_flag = True  # флаг, нужен для проигрывания звука полёта
        self.rect = self.image.get_rect()
        self.sound = pygame.mixer.Sound('../data/sounds/fly.mp3')  # звук вылета самолёта
        self.sound.set_volume(sound_parameter)
        self.rect.x = WIDTH // 2 - self.rect.width // 1.7
        self.rect.y = HEIGHT - 350

    # обновление самолёта
    def update(self, index):
        global score
        if index < 6:  # если индекс меньше 6, то обновляем изображение самолёта
            self.image = pygame.transform.scale(self.progress[index], (700, 300))
        else:
            self.fly = True  # иначе - самолёт собран, и он может улетать
            self.image = pygame.transform.scale(self.progress[-1], (700, 300))

        # Проверяем, собран ли самолёт
        if self.fly:
            if self.play_sound_flag:  # флаг для проигрывания звука вылета
                score += 1
                self.sound.play()
                self.play_sound_flag = False
            self.rect = self.rect.move(4, -1)

        if self.rect.x > WIDTH:
            self.sound.stop()
            self.kill()


# Игровая функция:
def YoungAvia(function):
    global stand, order, score, sound_parameter

    sound_parameter = get_volume()  # параметр громкости

    # Инициализация игры
    pygame.init()
    pygame.display.set_caption('Юный Авиаинженер')
    screen = pygame.display.set_mode()
    WIDTH, HEIGHT = screen.get_size()
    game_background = pygame.transform.scale(Images.engineer_background, (WIDTH, HEIGHT))  # Фон игры

    # Подключение к БД
    connect = sqlite3.connect('../settings/records.sqlite')
    cursor = connect.cursor()
    data = cursor.execute('SELECT * from data WHERE game="engineer"').fetchone()
    is_played = data[3]

    # Счёт игры и флаг для паузы:
    score = 0
    paused = False
    paused_flag = False  # флаг для остановки обратного отсчёта таймера (чтобы таймер не обновлялся на паузе)
    wanna_quit = False  # если игрок нажимает на Esc, то спрашиваем, желает ли он завершить игру (флаг)

    # Шрифт
    font_scale = 26  # размер шрифта
    game_font = pygame.font.Font('../data/fonts/appetite.ttf', font_scale)  # шрифт

    # Работа со звуком
    pygame.mixer.stop()  # останавливаем музыку
    sound = pygame.mixer.Sound('../data/sounds/plane_music.mp3')
    sound.set_volume(sound_parameter)
    sound.play()

    # Если игрок впервые играет в данную игру - проводим краткий инструктаж (если так можно выразиться):
    if not is_played:
        get_instruction(screen, game_background, game_font, '../settings/plane_i.txt', 'engineer')

    # Детали самолёта
    details_group = generate_details()
    order = [0]

    # Стенд
    stand_group = pygame.sprite.Group()
    stand = Stand(stand_group)

    # Самолёт
    plane_group = pygame.sprite.Group()
    plane = Plane(plane_group)

    # Работа с временем
    start_time = time()
    timer_index = 30  # 30 секунд + 5 за каждый собранный самолёт
    timer = timer_index - int(time() - start_time)  # таймер (оставшееся время до конца игры)
    add_bonus_time = True  # флаг для добавления бонусного времени
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.blit(game_background, (0, 0))  # отрисовка фона
        stand_group.draw(screen)  # отрисовка стенда
        details_group.draw(screen)  # отрисовка деталей
        plane_group.draw(screen)  # отрисовка самолёта

        # длина порядка деталей (нужна для сравнения и изменения изображения самолёта)
        order_len = len(order)

        # Если игра на паузе - создаём паузу, меняем флаг паузы, останавливаем звук полёта самолёта (если он улетает)
        if paused:
            pause(screen, game_font)
            paused_flag = True
            plane.sound.stop()
        elif wanna_quit:
            pause(screen, game_font, text='Вы хотите выйти? Нажмите ENTER, чтобы завершить игру')
            paused_flag = True
            plane.sound.stop()
        else:
            # Если игрок продолжил играть после паузы, а пауза была включена в момент, когда самолёт улетал - заново
            # проигрываем звук полёта:
            if paused_flag and plane.fly:
                plane.sound.play()
            paused_flag = False

        if paused_flag:
            timer_index = timer  # сохраняем оставшееся время в индекс таймера
        else:
            timer = timer_index - int(time() - start_time)  # если нет паузы - обновляем таймер

        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and not wanna_quit:
                    paused = not paused
                    if not paused:
                        start_time = time()
                elif event.key == pygame.K_ESCAPE:
                    wanna_quit = not wanna_quit
                    paused = False
                    if not wanna_quit:
                        start_time = time()
                elif event.key == pygame.K_RETURN and wanna_quit:
                    running = False

            if not paused and not wanna_quit:
                details_group.update(event)  # обновление деталей

        if not paused and not wanna_quit:
            if len(order) >= order_len:
                plane.update(order[-1])

        # добавляем бонусное время, если самолёт собран
        if plane.fly and add_bonus_time:
            timer_index += 5  # секунд
            add_bonus_time = False

        if not len(plane.groups()):
            add_bonus_time = True

            # детали самолёта
            details_group = generate_details()

            # стенд
            stand_group = pygame.sprite.Group()
            stand = Stand(stand_group)

            # самолёт
            plane_group = pygame.sprite.Group()
            plane = Plane(plane_group)

            order = [0]

        # Отрисовка таймера, счётчика построенных самолётов:
        timer_text = game_font.render(f'Осталось секунд: {timer}', True, 'white')
        score_text = game_font.render(f'Построено cамолётов: {score}', True, 'white')
        screen.blit(timer_text, (50, HEIGHT - 100))  # отображение таймера
        screen.blit(score_text, (WIDTH - score_text.get_width() - 50, HEIGHT - 100))  # отображение счёта

        if timer < 1:
            plane.sound.stop()
            timer_text = game_font.render(f'Время вышло!', True, 'white')
            screen.blit(timer_text, (100, 100))
            break

        clock.tick(FPS)
        pygame.display.flip()

    # Функция завершения игры:
    game_over(screen, game_font, 'engineer', score, YoungAvia, function, Images.plane_over_buttons, game_background,
              'Время вышло!', 'Построено самолётов', Button)
