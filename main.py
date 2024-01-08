from os import environ
from Buttons import *
from settings import *
from random import random, randint


environ['SDL_VIDEO_CENTERED'] = '1'  # центрирование окна


# Окно главного меню игры (самое первое окно, которое появляется при запуске игры)
def mainMenu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # создание кнопок главного меню
    play = MenuButton(y=70, image_text='Играть')
    settings_button = MenuButton(y=170, image_text='Настройки')
    exit_button = MenuButton(y=270, image_text='Выход')
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
    difficult_settings_button = MenuButton(y=100, image_text='Сложность')
    back_button_button = MenuButton(y=200, image_text='Назад')
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
    WIDTH, HEIGHT = 1000, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # задний фон игровой карты (лобби)
    lobby_background = pygame.image.load(Images.lobby_background)
    lobby_background = pygame.transform.scale(lobby_background, (WIDTH, HEIGHT))

    farm_location = Button(*Images.farm_button, 100, HEIGHT // 2 - 150)  # кнопка для локации фермера
    build_location = Button(*Images.builder_button, 600, HEIGHT // 2 - 150)  # кнопка для локации строителя
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


# Игра: Весёлый фермер
def HappyFarmer():
    global DIFFICULT_K
    SCREEN_WIDTH = 800  # ширина окна
    SCREEN_HEIGHT = 500  # высота окна
    FPS = 60  # количество кадров в секунду
    WHITE = (255, 255, 255)  # цвет
    FONT = pygame.font.Font(None, 36)  # шрифт счётчика

    # Игровые переменные:
    score = 0  # текущий счёт
    lives = 5  # Начальное количество жизней
    egg_speed = 2 * DIFFICULT_K  # скорость падения предметов (зависит от выбранной сложности)
    player_speed = 6  # скорость игрока

    # размеры окна игры
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # загружаем картинки для объектов
    egg_image = pygame.image.load(Images.egg_img)  # яйцо
    farmer_left_img = pygame.image.load(Images.farmer_left_img)  # фермер, который идёт влево
    farmer_right_img = pygame.image.load(Images.farmer_right_img)  # фермер, который идёт вправо
    heart_img = pygame.image.load(Images.heart_img)  # сердца

    # Создаем отдельный поверхностный объект для затемнения экрана (для паузы)
    dim_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    dim_surface.set_alpha(150)  # Устанавливаем прозрачность

    # Размеры объектов (берутся из изображений)
    egg_width, egg_height = egg_image.get_size()  # яйцо
    farmer_width, farmer_height = farmer_left_img.get_size()  # фермер
    heart_width, heart_height = heart_img.get_size()  # сердца

    #
    basket_x = SCREEN_WIDTH // 2 - farmer_width // 2
    basket_y = SCREEN_HEIGHT - farmer_height - 10

    # начальное направление движения фермера
    basket_direction = "left"
    eggs = []  # яйца (ну это понятно)
    paused = False  # поставлена ли игра на паузу

    # отрисовка всех объектов
    def draw_objects():
        screen.fill(WHITE)

        # картинка фермера зависит от направления его движения
        if basket_direction == "left":
            screen.blit(farmer_left_img, (basket_x, basket_y))
        else:
            screen.blit(farmer_right_img, (basket_x, basket_y))

        # отображение яиц
        for q in eggs:
            screen.blit(egg_image, q)

        # отображение оставшегося количества сердец
        for i in range(lives):
            screen.blit(heart_img, (10 + i * (heart_width + 5), 10))

        # отображение счета в углу
        score_text = FONT.render(f"Счёт: {score}", True, (0, 0, 0))
        screen.blit(score_text, (SCREEN_WIDTH - 130, 10))

        # отображение паузы
        if paused:
            # Затемнение экрана
            screen.blit(dim_surface, (0, 0))
            # Отображение текста паузы
            pause_text = FONT.render("Пауза. Нажмите P, чтобы продолжить", True, (0, 0, 0))  # текст паузы
            screen.blit(pause_text, (SCREEN_WIDTH // 2 - 230, SCREEN_HEIGHT // 2 - 20))  # отображение текста

    # Главный цикл игры
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)

        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # обработка нажатия на клавиши:
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Пауза при нажатии P
                    paused = not paused

        # если игра не на паузе - продолжаем обработку событий:
        if not paused:
            keys = pygame.key.get_pressed()

            # обрабатываем движение фермера влево
            if keys[pygame.K_LEFT] and basket_x > 0:
                basket_x -= player_speed
                basket_direction = "left"

            # обрабатываем движение фермера вправо
            elif keys[pygame.K_RIGHT] and basket_x < SCREEN_WIDTH - farmer_width:
                basket_x += player_speed
                basket_direction = "right"

            # Добавление нового яйца с вероятностью 2% (за один игровой кадр)
            if random() < 0.02:
                egg_x = randint(0, SCREEN_WIDTH - egg_width)
                egg_y = 0
                eggs.append((egg_x, egg_y))

            # падение яиц
            for i in range(len(eggs)):
                eggs[i] = (eggs[i][0], eggs[i][1] + egg_speed)

            # Проверка столкновения яиц с корзиной
            for egg in eggs:
                if (egg[0] < basket_x + farmer_width
                        and egg[0] + egg_width - 50 > basket_x
                        and egg[1] < basket_y + farmer_height
                        and egg[1] + egg_height - 50 > basket_y):
                    eggs.remove(egg)
                    score += 1

            # Проверка падения яиц за экран
            for egg in eggs:
                if egg[1] > SCREEN_HEIGHT:
                    eggs.remove(egg)
                    lives -= 1  # Уменьшение количества жизней

            # если количество жизней кончилось - завершаем игру
            if lives <= 0:
                running = False
                gameLobby()

        # отрисовка игровых объектов, игры в целом
        draw_objects()
        pygame.display.flip()

    pygame.quit()


# Игра: Строительный Тетрис
def BuilderTetris():
    Tetris_Game()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Мир Труда')  # заголовок
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # создание окна

    # задний фон главного меню
    menu_background = pygame.image.load(Images.mainmenu_img)
    menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))

    # запуск игры (начало игры с главного меню)
    mainMenu()
