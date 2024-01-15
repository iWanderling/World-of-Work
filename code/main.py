from os import environ
from button import *
from tetris import *
from plane import *
from farm import *

import sqlite3

environ['SDL_VIDEO_CENTERED'] = '1'  # центрирование окна
play = True


# Окно ввода имени (самое первое окно, которое появляется при запуске игры)
def setPlayerName():
    if hasattr(setPlayerName, 'name_entered') and setPlayerName.name_entered:
        return setPlayerName.name_entered

    input_box_width = 300
    input_box_height = 32
    input_box = pygame.Rect((WIDTH - input_box_width) // 2, HEIGHT // 2, input_box_width, input_box_height)
    color_inactive = pygame.Color('lightskyblue3')
    color = color_inactive
    active = True
    text = ''
    font_input = pygame.font.Font(None, 32)

    # Инструкция
    font_instruction = pygame.font.Font(None, 24)
    instruction_text = font_instruction.render("Введи своё имя в поле ниже и нажми ENTER", True, (255, 255, 255))
    instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
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
    global play
    menu_group = pygame.sprite.Group()
    Button(menu_group, func=gameLobby, y=HEIGHT // 4, text='Играть')  # играть
    Button(menu_group, func=settingsMenu, y=HEIGHT // 2.5, text='Настройки')  # настройки
    Button(menu_group, func=pygame.quit, y=HEIGHT // 1.8, text='Выход')  # выход
    if play:
        sound = pygame.mixer.Sound('../data/sounds/menu.mp3')
        sound.play()
        play = False
    running = True
    while running:
        screen.blit(menu_background, (0, 0))
        menu_group.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            menu_group.update(event)
        pygame.display.flip()


# Окно с игровыми настройками
def settingsMenu():
    settings_group = pygame.sprite.Group()
    Button(settings_group, func=setPlayerName, y=225, text='Изменить имя')
    Button(settings_group, func=mainMenu, y=325, text='Назад')

    running = True
    while running:
        screen.blit(menu_background, (0, 0))
        settings_group.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            settings_group.update(event)
        pygame.display.flip()


# Игровое окно
def gameLobby():
    # задний фон игровой карты (лобби)
    lobby_background = pygame.transform.scale(Images.lobby_background, (WIDTH, HEIGHT))

    size = (350, 350)
    lobby_group = pygame.sprite.Group()

    # локация фермера
    Button(lobby_group, func=HappyFarmer, par=gameLobby, images=Images.farm_buttons, x=100, size=size)
    # локация строителя
    Button(lobby_group, func=TetrisGame, par=gameLobby, images=Images.build_buttons, x=WIDTH // 2 - 150, size=size)
    # локация инженера
    Button(lobby_group, func=YoungAvia, par=gameLobby, images=Images.engineer_buttons, x=WIDTH - 400, size=size)
    # кнопка "назад"
    Button(lobby_group, func=mainMenu, images=Images.arrow_left, x=0, y=0, size=(50, 50))

    running = True
    while running:
        screen.blit(lobby_background, (0, 0))
        lobby_group.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            lobby_group.update(event)
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Мир Труда')  # заголовок
    screen = pygame.display.set_mode()  # создание окна
    WIDTH, HEIGHT = screen.get_size()

    # задний фон главного меню
    menu_background = Images.menu_background
    menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))

    # сохраняем имя пользователя, если его ещё нет
    with open('../settings/username.txt') as username:
        username = username.read()
        if not username:
            setPlayerName()
        else:
            # запуск игры (начало игры с главного меню)
            mainMenu()
