import pygame
from random import shuffle
from time import time
from data import Images


FPS = 180
score = 0
time_ = time()

WIDTH, HEIGHT = pygame.display.set_mode().get_size()


# генерация деталей
def generate_details():
    # детали самолёта
    x_s = 50  # рисуем детали в ряд
    indexes = list(range(6))  # случайные индексы (0, ..., 5)
    shuffle(indexes)  # перемешиваем список
    dgroup = pygame.sprite.Group()  # группа спрайтов (деталей)
    for i in indexes:  # выбор детали и отрисовка
        Detail(i, x_s, dgroup)
        x_s += WIDTH // 6

    return dgroup


# Класс для работы с деталями самолёта
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
            if not pygame.sprite.collide_mask(self, stand) or self.queue != order[-1] + 1:
                self.rect.x, self.rect.y = self.initial_coordinates
            else:
                order.append(self.queue)
                self.kill()


# Стенд
class Stand(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = Images.stand
        self.image = pygame.transform.scale(self.image, (600, 500))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - self.rect.width // 2
        self.rect.y = HEIGHT - 250


# Класс самолёта (собирается по частям)
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
        self.image = self.progress[0]
        self.image = pygame.transform.scale(self.image, (700, 300))
        self.fly = False  # самолёт улетает с площадки, только если он построен
        self.play_sound_flag = True  # флаг, нужен для проигрывания звука полёта
        self.rect = self.image.get_rect()
        self.sound = pygame.mixer.Sound('../data/sounds/fly.mp3')
        self.rect.x = WIDTH // 2 - self.rect.width // 1.7
        self.rect.y = HEIGHT - 350

    # обновление самолёта
    def update(self, index):
        global score
        if index < 6:
            self.image = pygame.transform.scale(self.progress[index], (700, 300))
        else:
            self.fly = True

        if self.fly:
            if self.play_sound_flag:
                score += 1
                self.sound.play()
                self.play_sound_flag = False
            self.rect = self.rect.move(4, -1)

        if self.rect.x > WIDTH:
            self.sound.stop()
            self.kill()


def YoungAvia():
    global stand, order
    pygame.init()
    screen = pygame.display.set_mode()
    WIDTH, HEIGHT = screen.get_size()

    # Шрифт
    font_scale = 32  # размер шрифта
    FONT = pygame.font.Font(f'..\data\{"fonts"}\{"appetite.ttf"}', font_scale)  # шрифт
    score_text = FONT.render(f'Построено cамолётов: {score}', True, 'white')  # шрифт для отображения счёта

    # фон игры
    back = pygame.transform.scale(Images.engineer_background, (WIDTH, HEIGHT))

    # детали самолёта
    details_group = generate_details()

    # стенд
    stand_group = pygame.sprite.Group()
    stand = Stand(stand_group)

    # самолёт
    plane_group = pygame.sprite.Group()
    plane = Plane(plane_group)

    order = [0]

    clock = pygame.time.Clock()
    running = True
    while running:
        screen.blit(back, (0, 0))  # отрисовка фона
        stand_group.draw(screen)  # отрисовка стенда
        details_group.draw(screen)  # отрисовка деталей
        plane_group.draw(screen)  # отрисовка самолёта

        # длина порядка деталей (нужна для сравнения и изменения изображения самолёта)
        order_len = len(order)

        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                break

            details_group.update(event)  # обновление деталей

        if len(order) >= order_len:
            plane.update(order[-1])

        if not len(plane.groups()):
            # детали самолёта
            details_group = generate_details()

            # стенд
            stand_group = pygame.sprite.Group()
            stand = Stand(stand_group)

            # самолёт
            plane_group = pygame.sprite.Group()
            plane = Plane(plane_group)

            order = [0]

        timer = 15 - int(time() - time_)

        timer_text = FONT.render(f'Осталось секунд: {timer}', True, 'white')
        score_text = FONT.render(f'Построено cамолётов: {score}', True, 'white')
        screen.blit(timer_text, (50, HEIGHT - 100))  # отображение таймера
        screen.blit(score_text, (WIDTH - score_text.get_width() - 50, HEIGHT - 100))  # отображение счёта

        if timer < 1:
            plane.sound.stop()
            timer_text = FONT.render(f'Время вышло!', True, 'white')
            screen.blit(timer_text, (100, 100))
            running = False
            break

        clock.tick(FPS)
        pygame.display.flip()

    # Создаем отдельный поверхностный объект для затемнения экрана
    dim_surface = pygame.Surface((WIDTH, HEIGHT))
    dim_surface.set_alpha(150)  # Устанавливаем прозрачность
    game_over = True
    while game_over:
        screen.blit(back, (0, 0))
        screen.blit(dim_surface, (0, 0))

        game_over_text = FONT.render(f'Время вышло!', True, 'white')
        screen.blit(game_over_text, (WIDTH // 2 - font_scale * 4, HEIGHT // 4))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 1.9, HEIGHT // 3))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
                pygame.quit()

        clock.tick(FPS)
        pygame.display.flip()
        return False
