from os import environ
from random import choice, random, randint
# from InGames.Tetris.main import TetrisGame
from Buttons import *
from plane import *
from farm import *


environ['SDL_VIDEO_CENTERED'] = '1'  # центрирование окна


# Окно главного меню игры (самое первое окно, которое появляется при запуске игры)
def mainMenu():
    menu_group = pygame.sprite.Group()
    Button(menu_group, func=gameLobby, y=HEIGHT // 4, text='Играть')  # играть
    Button(menu_group, func=settingsMenu, y=HEIGHT // 2.5, text='Настройки')  # настройки
    Button(menu_group, func=pygame.quit, y=HEIGHT // 1.8, text='Выход')  # выход

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
    Button(settings_group, func=lambda x: x, y=225, text='Ничего')
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
    Button(lobby_group, func=Happy_Farmer, images=Images.farm_buttons, x=100, size=size)  # локация фермера
    Button(lobby_group, func=BuilderTetris, images=Images.build_buttons, x=WIDTH // 2 - 150, size=size)  # строитель
    Button(lobby_group, func=Young_Avia, images=Images.engineer_buttons, x=WIDTH - 400, size=size)  # инженер
    Button(lobby_group, func=mainMenu, images=[Images.arrow_left, Images.arrow_left], x=0, y=0, size=(50, 50))  # назад

    running = True
    while running:
        screen.blit(lobby_background, (0, 0))
        lobby_group.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            lobby_group.update(event)
        pygame.display.flip()


def HappyFarmer():
    farm_running = Happy_Farmer()
    if not farm_running:
        gameLobby()


# Игра: Строительный Тетрис
def BuilderTetris():
    # tetris_running = TetrisGame()
    # if not tetris_running:
    #     gameLobby()
    pass

def Young_Avia():
    avia_running = YoungAvia()
    if not avia_running:
        gameLobby()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Мир Труда')  # заголовок
    screen = pygame.display.set_mode()  # создание окна
    WIDTH, HEIGHT = screen.get_size()

    # задний фон главного меню
    menu_background = Images.menu_background
    menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))

    # запуск игры (начало игры с главного меню)
    mainMenu()
