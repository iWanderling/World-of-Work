import pygame

from tetris import *  # игра для строителя
from plane import *  # игра для инженера
from farm import *  # игра для фермера
import os  # для проверки существования БД в настройках игры и центрирования экрана
from buttons import Slider

# Центрирование окна, создание флага для первого проигрывания музыки в главном меню
os.environ['SDL_VIDEO_CENTERED'] = '1'
play = True


# Создание базы данных с хранением рекордов в каждой игре (если она существует - то не создаём), а также имя игрока:
def create_database():
    # создаём файл с именем игрока
    if not os.access('../settings/username.txt', os.F_OK):
        with open('../settings/username.txt', 'w') as f:
            f.write('')

    # создаём БД
    if not os.access('../settings/records.sqlite', os.F_OK):
        connect = sqlite3.connect('../settings/records.sqlite')
        cursor = connect.cursor()
        cursor.execute("CREATE TABLE data(id INTEGER PRIMARY KEY AUTOINCREMENT, game TEXT, record INT, played INT)")

        # Добавление данных в БД
        for game in ('farmer', 'builder', 'engineer', 'final'):
            cursor.execute(f"""INSERT INTO data(game, record, played)
                              VALUES("{game}", 0, 0)""")
            connect.commit()

# Окно ввода имени (самое первое окно, которое появляется при запуске игры)
def setPlayerName():
    width, height = 300, 32  # размеры окна ввода
    input_box = pygame.Rect((WIDTH - width) // 2, HEIGHT // 2, width, height)
    color_inactive = pygame.Color('lightskyblue3')
    color = color_inactive
    active = True
    text = ''
    font_input = pygame.font.Font(None, 32)

    # Инструкция для ввода текста:
    font_instruction = pygame.font.Font(None, 24)
    instruction_text = font_instruction.render("Введи своё имя в поле ниже и нажми ENTER", True, (255, 255, 255))
    instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                    setPlayerName.name_entered = text
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
        screen.fill((30, 30, 30))

        # Отображение текста инструкции
        screen.blit(instruction_text, instruction_rect)
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.draw.rect(screen, color, input_box)
        text_surface = font_input.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (input_box.x + 10, input_box.y + 5))
        pygame.display.flip()

    text = text.capitalize()
    with open('../settings/username.txt', 'w') as f:
        f.write(text)

    # Отображение приветственного сообщения после нажатия клавиши ENTER
    welcome_font = pygame.font.Font(None, 36)
    welcome_text = welcome_font.render(f"Добро пожаловать, {text}!", True, (255, 255, 255))
    welcome_rect = welcome_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(welcome_text, welcome_rect)
    pygame.display.flip()
    pygame.time.delay(1000)
    mainMenu()


# Окно главного меню игры
def mainMenu():
    global play, menu_sound
    menu_group = pygame.sprite.Group()  # создаём кнопки, привязываем их к группе
    Button(menu_group, func=gameLobby, y=HEIGHT // 4, text='Играть')  # Играть
    Button(menu_group, func=settingsMenu, y=HEIGHT // 2.5, text='Настройки')  # Настройки
    Button(menu_group, func=exit, y=HEIGHT // 1.8, text='Выход')  # Выйти из игры

    # Воспроизводим музыку главного меню (за это отвечает флаг play)
    if play:
        menu_sound = pygame.mixer.Sound('../data/sounds/menu.mp3')
        menu_sound.set_volume(get_volume())
        menu_sound.play()
        play = False

    # Считываем имя пользователя, отображаем имя в главном меню
    with open('../settings/username.txt') as username_file:
        player_name = username_file.read()
    font_player_name = pygame.font.Font(None, 24)
    player_name_text = font_player_name.render(f"Игрок: {player_name}", True, 'white')
    player_name_rect = player_name_text.get_rect(bottomleft=(10, HEIGHT - 10))
    screen.blit(player_name_text, player_name_rect)

    while True:
        screen.blit(menu_background, (0, 0))
        menu_group.draw(screen)
        screen.blit(player_name_text, player_name_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if player_name_rect.collidepoint(event.pos):
                    setPlayerName()

            menu_group.update(event)
        pygame.display.flip()


# Окно с игровыми настройками
def settingsMenu():
    pygame.display.set_caption('Мир Труда')
    settings_group = pygame.sprite.Group()
    Button(settings_group, func=setPlayerName, y=HEIGHT // 4, text='Изменить имя')
    Button(settings_group, func=changeVolume, y=HEIGHT // 2.5, text='Звук')
    Button(settings_group, func=mainMenu, y=HEIGHT // 1.8, text='Назад')

    while True:
        screen.blit(menu_background, (0, 0))
        settings_group.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            settings_group.update(event)
        pygame.display.flip()


# Функция в настройках - изменение громкости всей игры:
def changeVolume():
    volume_group = pygame.sprite.Group()  # группа кнопки и ползунка
    back_b = Button(volume_group, func=settingsMenu, y=HEIGHT // 1.6, text='Назад')  # кнопка "назад"
    slider = Slider(volume_group, x=WIDTH // 2 - 110 + (get_volume() * 100) * 1.7, y=HEIGHT // 2.1, screen=screen)

    font_scale = 26
    volume_font = pygame.font.Font('../data/fonts/appetite.ttf', font_scale)  # шрифт
    volume_text = volume_font.render('Двигайте ползунок влево и вправо, чтобы изменить громкость звука', True, 'white')
    w, h = volume_text.get_width(), volume_text.get_height()  # размеры volume_text

    # разница левой и правой координаты x [линии ползунка] (необходима для корректного вычисления параметра звука)
    bar_width_difference = (WIDTH // 2 + 60) - (WIDTH // 2 - 110)

    while True:
        screen.blit(menu_background, (0, 0))  # отображение фона
        screen.blit(volume_text, (WIDTH // 2 - w // 2, HEIGHT // 5))  # отображение текста-подсказки

        # рисуем полосу, по которой перемещается ползунок
        pygame.draw.rect(screen, 'gray', (WIDTH // 2 - 100, HEIGHT // 2, 200, 10))

        # отображаем параметр звука:
        sound_parameter = int((slider.rect.x - (WIDTH // 2 - 110)) // (bar_width_difference / 100))

        # сохраняем значение громкости звука:
        with open('../settings/volume.txt', 'w') as f:
            f.write(str(sound_parameter))  # записываем громкость в файл
            menu_sound.set_volume(sound_parameter / 100)  # сразу же меняем значение громкости музыки главного меню
            back_b.sound.set_volume(sound_parameter / 100)  # и громкость клика по кнопке "назад" (продумано, хе-хе)

        # отображаем уровень громкости (текст):
        volume_k_text = volume_font.render(f'Громкость: {sound_parameter}', True, 'white')
        vkt_w = volume_k_text.get_width()
        screen.blit(volume_k_text, (WIDTH // 2 - vkt_w // 2, HEIGHT // 3))

        # отображение кнопки и ползунка
        volume_group.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            volume_group.update(event)

        pygame.display.flip()


# Игровое окно (лобби с локациями разных профессий):
def gameLobby(soundplay=False):

    connect = sqlite3.connect('../settings/records.sqlite')
    cursor = connect.cursor()

    # Проигрываем музыку главного меню, если игрок вышел из любой игры-локации:
    if soundplay:
        menu_sound.play()

    # задний фон игровой карты (лобби)
    lobby_background = pygame.transform.scale(Images.lobby_background, (WIDTH, HEIGHT))

    # если игрок поиграл во все игры и набрал хотя-бы несколько очков в каждой из них - то поздравляем его
    if cursor.execute('SELECT played FROM data WHERE game="final"').fetchall()[0][0] == 0:
        data = cursor.execute('SELECT record FROM data').fetchall()[:-1]
        for d in data:
            if d[0] == 0:
                break
        else:
            font_scale = 24  # размер игрового шрифта
            _font = pygame.font.Font('../data/fonts/appetite.ttf', font_scale)  # шрифт

            get_instruction(screen, lobby_background, _font, '../settings/congrats.txt', 'final')

    size = (350, 350)  # размеры кнопок локаций
    lobby_group = pygame.sprite.Group()

    # локация фермера
    Button(lobby_group, func=HappyFarmer, par=gameLobby, images=Images.farm_buttons, x=100, size=size)
    # локация строителя
    Button(lobby_group, func=TetrisGame, par=gameLobby, images=Images.build_buttons, x=WIDTH // 2 - 150, size=size)
    # локация инженера
    Button(lobby_group, func=YoungAvia, par=gameLobby, images=Images.engineer_buttons, x=WIDTH - 400, size=size)
    # кнопка "назад"
    Button(lobby_group, func=mainMenu, images=Images.arrow_left, x=0, y=0, size=(50, 50))

    while True:
        screen.blit(lobby_background, (0, 0))
        lobby_group.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            lobby_group.update(event)
        pygame.display.flip()


if __name__ == '__main__':
    create_database()  # создаём базу данных

    pygame.init()  # инициализация игры
    pygame.display.set_caption('Мир Труда')  # заголовок
    screen = pygame.display.set_mode()  # создание окна
    WIDTH, HEIGHT = screen.get_size()  # размеры монитора пользователя

    # задний фон главного меню
    menu_background = Images.menu_background
    menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))

    # Если значение звука ещё не указано - ставим 50%
    if not os.access('../settings/volume.txt', os.F_OK):
        with open('../settings/volume.txt', 'w') as volume_file:
            volume_file.write('50')

    # Сохраняем имя пользователя, если его ещё нет:
    with open('../settings/username.txt') as username:
        username = username.read()
        if not username:
            setPlayerName()
        else:
            # запуск игры (начало игры с главного меню)
            mainMenu()
