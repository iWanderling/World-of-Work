"""
      Данный файл содержит в себе функции, которые используются во всех играх, а также класс со всеми изображениями для
    удобной работы с ними. Помимо этого, этот файл импортирует библиотеки pygame и sqlite, так что импортировать их
    в других файлах не придётся. Проще говоря, этот файл значительно уменьшает количество строк кода, что может быть
    полезно для людей, которые только знакомятся с нашим кодом. Да и, на самом деле, такой подход более рационален)
"""


# Импорт библиотек
from os import path  # для загрузки файлов
import sqlite3  # БД
import pygame  # <- из-за этого красавца мы все здесь сегодня собрались (o_o)


# Размеры монитора игрока (ширина и высота)
WIDTH, HEIGHT = pygame.display.set_mode().get_size()


# Создаем отдельный поверхностный объект для затемнения экрана
dim_surface = pygame.Surface((WIDTH, HEIGHT))
dim_surface.set_alpha(150)  # Устанавливаем прозрачность


# Отображение инструкции в каждой игре (запрос: экран, фон игры, шрифт игры, путь к инструкции, название игры):
def get_instruction(screen, background, font, i_path, game_title):
    # Открываем БД и текстом инструкции:
    connect = sqlite3.connect('../settings/records.sqlite')
    cursor = connect.cursor()
    with open(i_path, encoding='utf-8') as f:
        instruction = [s.strip() for s in f.readlines()]  # чтение инструкции

    if game_title == 'final':
        with open('../settings/username.txt') as f:
            try:
                instruction[0] = instruction[0].replace('наш юный друг', f.readlines()[0])
            except IndexError:
                pass

    # Цикл для отображения инструкции:
    irun = True
    while irun:
        font_y = 100  # поскольку в pygame текст нельзя переносить, будем построчно отображать текст на экране
        screen.blit(background, (0, 0))  # рисуем фон
        screen.blit(dim_surface, (0, 0))  # затемняем экран

        # Отрисовка инструкции (построчно):
        for i in range(len(instruction)):
            instruction_string = font.render(instruction[i], True, 'white')
            w_i, h_i = instruction_string.get_size()
            screen.blit(instruction_string, (WIDTH // 2 - w_i // 2, font_y))
            font_y += 50

        # Обрабатываем нажатие на любую кнопку, чтобы начать игру
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if game_title == 'final':
                    irun = False
                    break
                elif event.key == pygame.K_s:
                    irun = False
                    break
            elif event.type == pygame.QUIT:
                exit()
        pygame.display.flip()

    # Обновляем БД: инструкция больше не покажется:
    cursor.execute(f'UPDATE data SET played=1 WHERE game="{game_title}"')
    connect.commit()


# Функция для завершения игры | Параметры: экран, шрифт игры, название игры (farmer, builder, engineer), набранный счёт,
# функция игры, функция игрового лобби (function), изображения кнопок, фон игры, текста: КОНЕЦ ИГРЫ, СЧЁТ; класс кнопок,
# необязательные параметры: [цвет, звук]:
def game_over(screen, game_font, game_title, game_score, game_function, function, button_images, background,
              game_over_text, score_text, Button, color='white', sound=None):

    # Останавливаем все звуки и проигрываем переданный звук:
    pygame.mixer.stop()
    if sound is not None:
        sound.play()

    connect = sqlite3.connect('../settings/records.sqlite')
    cursor = connect.cursor()
    record = cursor.execute(f'SELECT record FROM data WHERE game="{game_title}"').fetchone()[0]

    # Создаём кнопки:
    button_images = button_images
    buttons = pygame.sprite.Group()
    Button(buttons, func=game_function, par=function, images=button_images, y=HEIGHT // 3 + 50, text='Играть снова')
    Button(buttons, func=function, par=True, images=button_images, y=HEIGHT // 2 + 50, text='Меню')

    # создаём шрифты, отображаем и/или обновляем рекорд
    game_over_text = game_font.render(game_over_text, True, color)
    score_text = game_font.render(f'{score_text}: {game_score}', True, color)
    if game_score > record:
        cursor.execute(f'UPDATE data SET record={game_score} WHERE game="{game_title}"')
        connect.commit()
        record_text = game_font.render(f'Новый рекорд: {game_score}!', True, color)
    else:
        record_text = game_font.render(f'Лучший рекорд: {record}', True, color)

    while True:
        # Отрисовка кнопок, фона, затемнения
        screen.blit(background, (0, 0))
        screen.blit(dim_surface, (0, 0))
        buttons.draw(screen)

        # Отрисовка текста
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 5))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 4))
        screen.blit(record_text, (WIDTH // 2 - record_text.get_width() // 2, HEIGHT // 3.3))

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            buttons.update(event)

        pygame.display.flip()


# Функция для изменения размеров pygame-изображения:
def change_size(image, size):
    return pygame.transform.scale(image, size)


# Функция для загрузки и конвентирования изображения в pygame-формат:
def loader(folder, name):
    address = path.join(f'../data/images/{folder}', name)
    return pygame.image.load(address)


# Игровая пауза (Также используется, как экран с вопросом игроку о его желании завершить игру):
def pause(screen, game_font, text="Пауза. Нажмите P, чтобы продолжить"):
    screen.blit(dim_surface, (0, 0))  # Затемнение экрана
    pause_text = game_font.render(text, True, 'white')
    screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 20))  # отображение текста


# Класс для хранения всех изображений, задействованных в игре:
class Images:
    # Изображения интерфейса
    arrow_left = [loader('interface', 'arrow_left.png'), loader('interface', 'arrow_left_hover.png')]  # кнопка "назад"
    menu_background = loader('interface', 'menu.jpg')  # фон меню
    lobby_background = loader('interface', 'lobby.png')  # фон лобби (авторское изображение)
    menu_buttons = loader('interface', 'button.png'), loader('interface', 'button_hover.png')  # кнопки меню
    farm_over_buttons = loader('interface', 'farm.png'), loader('interface', 'farm_hover.png')  # кнопки фермера
    builder_over_buttons = loader('interface', 'builder.png'), loader('interface', 'builder_hover.png')  # кнопки build
    plane_over_buttons = loader('interface', 'plane.png'), loader('interface', 'plane_hover.png')  # кнопки инженера

    # Изображения игры Весёлая Ферма
    apple = loader('farm', 'apple.png')  # яйцо
    egg = loader('farm', 'egg.png')  # яблоко
    cabbage = loader('farm', 'cabbage.png')  # капуста
    grass = loader('farm', 'grass.png')  # трава
    farm_background = loader('farm', 'game_background.jpg')  # задний фон игры
    farm_buttons = loader('farm', 'farm.png'), loader('farm', 'farm_hover.png')  # кнопки игры Веселая ферма
    heart = loader('farm', 'heart.png')  # сердца
    left = [loader('farm', f'left{i}.png') for i in range(1, 4)]  # фермер с пустой тележкой, идёт влево
    right = [loader('farm', f'right{i}.png') for i in range(1, 4)]  # фермер с пустой тележкой, идёт вправо
    half_left = [loader('farm', f'half_left{i}.png') for i in range(1, 4)]  # фермер с 50% тележкой, влево
    half_right = [loader('farm', f'half_right{i}.png') for i in range(1, 4)]  # фермер с 50% тележкой, вправо
    full_left = [loader('farm', f'full_left{i}.png') for i in range(1, 4)]  # фермер с полной тележкой, идёт влево
    full_right = [loader('farm', f'full_right{i}.png') for i in range(1, 4)]  # фермер с полной тележкой, идёт вправо

    # Изображения игры Строительный Тетрис
    build_buttons = loader('builder', 'build.png'), loader('builder', 'build_hover.png')  # кнопки локации строителя
    brick_names = ('yellow_brick', 'blue_brick', 'red_brick', 'green_brick', 'aqua_brick', 'brick', 'gray_brick',
                   'pink_brick')
    bricks = list(loader('builder', f'{color}.png') for color in brick_names)  # разноцветные кирпичики
    tetris_background = loader('builder', 'background.jpg')  # задний фон игрового окна тетриса (не всего окна)
    tetris_fullsize_background = loader('builder', 'background_window.png')  # фон окна тетриса (всего окна)

    # Изображения игры Юный Инженер
    engineer_buttons = loader('engineer', 'engineer.png'), loader('engineer', 'engineer_hover.png')
    engineer_background = loader('engineer', 'back.jpg')
    airplane0 = loader('engineer', 'empty.png')  # Пустое изображение
    airplane1 = loader('engineer', 'plane_no_cabine.png')  # Самолёт с фюзеляжем
    airplane2 = loader('engineer', 'plane_no_rubber.png')  # Добавлена кабина
    airplane3 = loader('engineer', 'plane_no_wings.png')  # добавлен хвост
    airplane4 = loader('engineer', 'plane_no_engine.png')  # добавлены крылья
    airplane5 = loader('engineer', 'airplane.png')  # добавлен двигатель
    airplane6 = loader('engineer', 'full_airplane.png')  # добавлены шасси (самолёт собран)
    fuselage = loader('engineer', 'fuselage.png')  # фюзеляж
    cabine = loader('engineer', 'cabine.png')  # кабина
    rudder = loader('engineer', 'rudder.png')  # хвост
    wing = loader('engineer', 'wing.png')  # крылья
    engine = loader('engineer', 'plane_engine.png')  # двигатель
    chassis = loader('engineer', 'chassis.png')  # шасси
    stand = loader('engineer', 'back.png')  # стенд, на котором собирается самолёт
