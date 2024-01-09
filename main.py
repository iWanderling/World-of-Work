from os import environ
from random import choice
from Buttons import *
from settings import *
from random import random, randint
from InGames.Tetris.main import TetrisGame
from farm import *


environ['SDL_VIDEO_CENTERED'] = '1'  # центрирование окна


# Окно главного меню игры (самое первое окно, которое появляется при запуске игры)
def mainMenu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # создание кнопок главного меню
    play = MenuButton(y=150, image_text='Играть')
    settings_button = MenuButton(y=250, image_text='Настройки')
    exit_button = MenuButton(y=350, image_text='Выход')
    menu_buttons = (play, settings_button, exit_button)  # список кнопок

    # игровой цикл
    running = True
    while running:
        screen.blit(menu_background, (0, 0))
        draw_buttons_group(menu_buttons, screen)  # Отрисовка группы кнопок

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    # Обработка проигрывания звука при нажатии кнопки
                    for btn in menu_buttons:
                        btn.soundplay()

                    # обработка нажатия на кнопку запуска игры
                    if play.is_hovered:
                        gameLobby()

                    # обработка нажатия на кнопку выхода из игры
                    if exit_button.is_hovered:
                        pygame.quit()

                    # обработка нажатия на кнопку настроек
                    if settings_button.is_hovered:
                        settings()

        pygame.display.flip()


# Окно с игровыми настройками
def settings():
    # создание кнопок
    difficult_settings_button = MenuButton(y=225, image_text='Сложность')
    back_button_button = MenuButton(y=325, image_text='Назад')
    settings_buttons = (difficult_settings_button, back_button_button)  # список кнопок для их обработки и отображения

    # Игровой цикл
    running = True
    while running:
        screen.blit(menu_background, (0, 0))  # задний фон окна
        draw_buttons_group(settings_buttons, screen)

        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # обработка нажатия левой кнопки мыши
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    # Проигрывание звука при нажатии кнопки
                    for btn in settings_buttons:
                        btn.soundplay()

                    # обработка нажатия на кнопку изменения сложности
                    if difficult_settings_button.is_hovered:
                        difficult()

                    # обработка нажатия на кнопку <назад> (в главное меню)
                    if back_button_button.is_hovered:
                        mainMenu()

        pygame.display.flip()


# Окно с выбором сложности в игре
def difficult():
    global DIFFICULT_K

    # кнопки выбора сложности
    easy_difficult = MenuButton(y=70, image_text='Легкий')
    medium_difficult = MenuButton(y=170, image_text='Средний')
    hard_difficult = MenuButton(y=270, image_text='Высокий')
    difficult_buttons = (easy_difficult, medium_difficult, hard_difficult)  # список кнопок

    # Определяем текущую сложность
    with open('files/game_settings/settings.txt') as f:
        difficult_level = str(f.readlines()[0])
        DIFFICULT_K = {'Легкий': 1, 'Средний': 2, 'Высокий': 3}[difficult_level]
        text_surface, text_rect = create_font(size=54, text=f'Текущий уровень: {difficult_level}',
                                              x=WIDTH // 2, y=40)  # Font created

    # игровой цикл
    running = True
    while running:
        screen.blit(menu_background, (0, 0))  # отрисовка фона
        screen.blit(text_surface, text_rect)  # отрисовка шрифта
        draw_buttons_group(difficult_buttons, screen)

        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # изменение сложности игры в зависимости от того, какая кнопка нажата
                    for btn in difficult_buttons:
                        if btn.is_hovered:
                            with open('files/game_settings/settings.txt', 'w') as f:
                                f.write(btn.image_text)
                            btn.soundplay()
                            settings()
                            break

        pygame.display.flip()


# Игровое окно
def gameLobby():
    WIDTH, HEIGHT = 1200, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # задний фон игровой карты (лобби)
    lobby_background = pygame.image.load(Images.lobby_background)
    lobby_background = pygame.transform.scale(lobby_background, (WIDTH, HEIGHT))

    farm_location = Button(*Images.farm_button, 100, HEIGHT // 2 - 150)  # кнопка для локации фермера
    build_location = Button(*Images.builder_button, WIDTH - 400, HEIGHT // 2 - 150)  # кнопка для локации строителя
    arrow_button = Button(*Images.arrow_back_button, 0, 0, 50, 50)  # кнопка "назад"
    lobby_buttons = (farm_location, build_location, arrow_button)  # кнопки лобби

    # игровой цикл
    running = True
    while running:
        screen.blit(lobby_background, (0, 0))
        draw_buttons_group(lobby_buttons, screen)

        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if farm_location.is_hovered:  # нажатие на игру "Весёлый Фермер"
                        HappyFarmer()
                    elif build_location.is_hovered:  # нажатие на игру "Строительный Тетрис"
                        BuilderTetris()
                    if arrow_button.is_hovered:  # нажатие на кнопку "назад"
                        mainMenu()
        pygame.display.flip()


def HappyFarmer():
    farm_running = Happy_Farmer()
    if not farm_running:
        gameLobby()


# Игра: Строительный Тетрис
def BuilderTetris():
    tetris_running = TetrisGame()
    if not tetris_running:
        gameLobby()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Мир Труда')  # заголовок
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # создание окна

    # задний фон главного меню
    menu_background = pygame.image.load(Images.mainmenu_img)
    menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))

    # запуск игры (начало игры с главного меню)
    mainMenu()
