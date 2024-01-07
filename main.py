import random
from Buttons import *
from settings import *
from pygame import mouse


# Отрисовка кнопок и обработка наведения мыши на них
def draw_buttons_group(group, screen):
    for b in group:
        b.draw(screen)
        b.check_hover(mouse.get_pos())


# Окно главного меню игры (самое первое окно, которое появляется при запуске игры)
def main_menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.blit(image_background, (0, 0))

    play = MenuButton(WIDTH // 2 - 75, 70, 'Играть')
    settings = MenuButton(WIDTH // 2 - 75, 170, 'Настройки')
    exit_button = MenuButton(WIDTH // 2 - 75, 270, 'Выход')
    menu_buttons = (play, settings, exit_button)
    screen.blit(image_background, (0, 0))
    running = True
    while running:
        draw_buttons_group(menu_buttons, screen)  # Отрисовка группы

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
                        game_window()

                    # обработка нажатия на кнопку выхода из игры
                    if exit_button.is_hovered:
                        pygame.quit()

                    # обработка нажатия на кнопку настроек
                    if settings.is_hovered:
                        settings_menu()

        pygame.display.flip()


# Окно с игровыми настройками
def settings_menu():
    sound_settings_button = MenuButton(WIDTH // 2 - 75, 70, 'Звук')
    difficult_settings_button = MenuButton(WIDTH // 2 - 75, 170, 'Сложность')
    back_button_button = MenuButton(WIDTH // 2 - 75, 270, 'Назад')
    settings_buttons = (sound_settings_button, difficult_settings_button, back_button_button)
    screen.blit(image_background, (0, 0))
    running = True
    while running:
        draw_buttons_group(settings_buttons, screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    # Проигрывание звука при нажатии кнопки
                    for btn in settings_buttons:
                        btn.soundplay()

                    # обработка нажатия на кнопку регулировки звука
                    if sound_settings_button.is_hovered:
                        sound_menu()

                    # обработка нажатия на кнопку изменения сложности
                    if difficult_settings_button.is_hovered:
                        difficult_menu()

                    # обработка нажатия на кнопку <назад> (в главное меню)
                    if back_button_button.is_hovered:
                        main_menu()

        pygame.display.flip()


# Окно с выбором сложности в игре
def difficult_menu():
    global DIFFICULT_K
    easy_difficult = MenuButton(WIDTH // 2 - 75, 70, 'Легкий')
    medium_difficult = MenuButton(WIDTH // 2 - 75, 170, 'Средний')
    hard_difficult = MenuButton(WIDTH // 2 - 75, 270, 'Высокий')
    difficult_buttons = (easy_difficult, medium_difficult, hard_difficult)
    screen.blit(image_background, (0, 0))
    # Определяем текущую сложность
    with open('settings.txt') as f:
        difficult_level = str(f.readlines()[0])
        DIFFICULT_K = {'Легкий': 1, 'Средний': 2, 'Высокий': 3}[difficult_level]
        text_surface, text_rect = create_font(size=54, text=f'Текущий уровень: {difficult_level}',
                                              x=WIDTH // 2, y=40)  # Font created

    running = True
    while running:
        draw_buttons_group(difficult_buttons, screen)
        screen.blit(text_surface, text_rect)  # отрисовка шрифта

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    # изменение сложности игры в зависимости от того, какая кнопка нажата
                    for btn in difficult_buttons:
                        if btn.is_hovered:
                            with open('settings.txt', 'w') as f:
                                f.write(btn.image_text)
                            btn.soundplay()
                            settings_menu()
                            break

        pygame.display.flip()


# Окно с регулировкой звука
def sound_menu():
    back_button = MenuButton(WIDTH // 2 - 75, 270, 'Назад')  # Кнопка <назад>

    # создание шрифта
    text_surface, text_rect = create_font(size=36, text='Регулируйте звук стрелочками (влево и вправо)',
                                          color='white', x=WIDTH // 2, y=50)
    screen.blit(image_background, (0, 0))
    running = True
    while running:
        draw_buttons_group([back_button], screen)
        screen.blit(text_surface, text_rect)  # создание шрифта

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # если кнопка <назад> нажата, то возвращаемся в настройки
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and back_button.is_hovered:
                    settings_menu()

        pygame.display.flip()


# Игровое окно
def game_window():
    WIDTH, HEIGHT = 1000, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    game_background = pygame.transform.scale(pygame.image.load('files/img/interface/game_background_secret_version.png'),
                                             (WIDTH, HEIGHT))

    farm_location = Button('files/img/farm_game/farm.png', 'files/img/farm_game/farm_hover.png',
                           100, HEIGHT // 2 - 150, 300, 300)
    build_location = Button('files/img/builder_game/build.png', 'files/img/builder_game/build_hover.png',
                            600, HEIGHT // 2 - 150, 300, 300)
    arrow_button = Button('files/img/interface/arrow_left.png', 'files/img/interface/arrow_left.png', 0, 0, 50, 50)
    location_group = (farm_location, build_location, arrow_button)
    screen.blit(game_background, (0, 0))
    running = True
    while running:
        draw_buttons_group(location_group, screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if farm_location.is_hovered:
                        farm_game()
                    elif build_location.is_hovered:
                        builder_game()
                    if arrow_button.is_hovered:
                        main_menu()

        pygame.display.flip()


def farm_game():
    global DIFFICULT_K
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 500
    FPS = 60
    WHITE = (255, 255, 255)
    FONT = pygame.font.Font(None, 36)

    # Игровые переменные
    score = 0
    penalty = 0
    lives = 5  # Начальное количество жизней
    egg_speed = 2 * DIFFICULT_K
    player_speed = 6

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    egg_image = pygame.image.load("files/img/farm_game/egg.png")
    basket_left_image = pygame.image.load("files/img/farm_game/farmer_left.png")
    basket_right_image = pygame.image.load("files/img/farm_game/farmer_right.png")
    heart_image = pygame.image.load("files/img/farm_game/heart.png")

    # Создаем отдельный поверхностный объект для затемнения экрана
    dim_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    dim_surface.set_alpha(150)  # Устанавливаем прозрачность

    egg_width, egg_height = egg_image.get_size()
    basket_width, basket_height = basket_left_image.get_size()
    heart_width, heart_height = heart_image.get_size()

    basket_x = SCREEN_WIDTH // 2 - basket_width // 2
    basket_y = SCREEN_HEIGHT - basket_height - 10

    basket_direction = "left"
    eggs = []
    paused = False

    def draw_objects():
        screen.fill(WHITE)

        if basket_direction == "left":
            screen.blit(basket_left_image, (basket_x, basket_y))
        else:
            screen.blit(basket_right_image, (basket_x, basket_y))

        for q in eggs:
            screen.blit(egg_image, q)

        for i in range(lives):
            screen.blit(heart_image, (10 + i * (heart_width + 5), 10))

        # Отображение счета в углу
        score_text = FONT.render(f"Счёт: {score}", True, (0, 0, 0))
        screen.blit(score_text, (SCREEN_WIDTH - 130, 10))

        # Отображение паузы
        if paused:
            # Затемнение экрана
            screen.blit(dim_surface, (0, 0))
            # Отображение текста паузы
            pause_text = FONT.render("Пауза. Нажмите P, чтобы продолжить", True, (0, 0, 0))
            screen.blit(pause_text, (SCREEN_WIDTH // 2 - 230, SCREEN_HEIGHT // 2 - 20))

    # Главный цикл игры
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Пауза при нажатии P
                    paused = not paused

        if not paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and basket_x > 0:
                basket_x -= player_speed
                basket_direction = "left"  # Изменение направления корзины
            if keys[pygame.K_RIGHT] and basket_x < SCREEN_WIDTH - basket_width:
                basket_x += player_speed
                basket_direction = "right"  # Изменение направления корзины

            # Добавление нового яйца с вероятностью
            if random.random() < 0.02:
                egg_x = random.randint(0, SCREEN_WIDTH - egg_width)
                egg_y = 0
                eggs.append((egg_x, egg_y))

            # Движение яиц вниз
            for i in range(len(eggs)):
                eggs[i] = (eggs[i][0], eggs[i][1] + egg_speed)

            # Проверка столкновения яиц с корзиной
            for egg in eggs:
                if (
                        egg[0] < basket_x + basket_width
                        and egg[0] + egg_width - 50 > basket_x
                        and egg[1] < basket_y + basket_height
                        and egg[1] + egg_height - 50 > basket_y
                ):
                    eggs.remove(egg)
                    score += 1

            # Проверка падения яиц за экран
            for egg in eggs:
                if egg[1] > SCREEN_HEIGHT:
                    eggs.remove(egg)
                    penalty += 1
                    lives -= 1  # Уменьшение количества жизней

            if lives <= 0:
                running = False
                game_window()

        draw_objects()
        pygame.display.flip()

    pygame.quit()


def builder_game():
    pass


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Мир Труда')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    image_background = pygame.image.load('files/img/interface/brickstone_background.jpg')
    image_background = pygame.transform.scale(image_background, (WIDTH, HEIGHT))
    screen.blit(image_background, (0, 0))

    main_menu()
