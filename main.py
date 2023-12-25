import os
import pygame
import random
from base_functions import draw_buttons_group


# Переменные для ширины и высоты экрана
WIDTH, HEIGHT = 600, 400
os.environ['SDL_VIDEO_CENTERED'] = '1'  # центрирование окна


# Создать шрифт (параметры: размер, текст, x, y (относительно центра), цвет, тип шрифта, сглаживание)
def create_font(size: int, text: str, x: int, y: int, color='white', font_type=None, smoothing=False) -> tuple:
    font = pygame.font.Font(font_type, size)
    text_surface = font.render(text, smoothing, color)

    return text_surface, text_surface.get_rect(center=(x, y))


# Добавить маску (комментарий)

# Класс для создания кнопок. От него идут классы для создания кнопок меню и локаций
class Button:
    def __init__(self, img, hover_img, x, y, width, height):

        # Наведен ли курсор на кнопку
        self.is_hovered = False

        # Загрузка основного изображения
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (width, height))  # масштабирование картинки под размер кнопки

        # Загрузка изображения при наведении
        self.hover_image = pygame.image.load(hover_img)
        self.hover_image = pygame.transform.scale(self.hover_image, (width, height))

        # Загрузка звукового эффекта при нажатии кнопки
        self.sound = pygame.mixer.Sound('files/sounds/sound.mp3')
        self.rect = self.image.get_rect(topleft=(x, y))

    # Отрисовка кнопки (в зависимости от того, наведен ли курсор на кнопку, картинка меняется)
    def draw(self, screen):
        if self.is_hovered:
            current_image = self.hover_image
        else:
            current_image = self.image
        screen.blit(current_image, self.rect.topleft)

    # Проверка: наведена ли мышь на кнопку
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    # Обработчик событий нажатия на кнопку, если кнопка нажата, воспроизведется звук
    def soundplay(self):
        if self.is_hovered:
            self.sound.play()


# Класс для создания кнопок главного меню (Наследуется от Button)
class MenuButton(Button):
    def __init__(self, x, y, image_text, width=150, height=70):
        super().__init__('files/img/button.png', 'files/img/button_hover.png', x, y, width, height)
        self.image_text = image_text  # Текст на кнопке

        # Создаём текст
        x, y = self.rect.center
        self.text_surface, self.text_rect = create_font(size=36, text=self.image_text, x=x, y=y, smoothing=True)

    # Отрисовка кнопки с текстом
    def draw(self, screen):
        if self.is_hovered:
            current_image = self.hover_image
        else:
            current_image = self.image
        screen.blit(current_image, self.rect.topleft)
        screen.blit(self.text_surface, self.text_rect)


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
                        terminate()

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
    easy_difficult = MenuButton(WIDTH // 2 - 75, 70, 'Легкий')
    medium_difficult = MenuButton(WIDTH // 2 - 75, 170, 'Средний')
    hard_difficult = MenuButton(WIDTH // 2 - 75, 270, 'Высокий')
    difficult_buttons = (easy_difficult, medium_difficult, hard_difficult)
    screen.blit(image_background, (0, 0))
    # Определяем текущую сложность
    with open('settings.txt') as f:
        text_surface, text_rect = create_font(size=54, text=f'Текущий уровень: {str(f.readlines()[0])}',
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

    game_background = pygame.transform.scale(pygame.image.load('files/img/game_background_secret_version.png'),
                                             (WIDTH, HEIGHT))

    farm_location = Button('files/img/farm.png', 'files/img/farm_hover.png', 100, HEIGHT // 2 - 150, 300, 300)
    build_location = Button('files/img/build.png', 'files/img/build_hover.png', 600, HEIGHT // 2 - 150, 300, 300)
    arrow_button = Button('files/img/arrow_left.png', 'files/img/arrow_left.png', 0, 0, 50, 50)
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
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 500
    FPS = 60
    WHITE = (255, 255, 255)

    # Игровые переменные
    score = 0
    penalty = 0
    lives = 5  # Начальное количество жизней
    egg_speed = 3

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Поймай яйцо!")

    egg_image = pygame.image.load("files/img/egg.png")
    basket_left_image = pygame.image.load("files/img/farmer_left.png")
    basket_right_image = pygame.image.load("files/img/farmer_right.png")
    heart_image = pygame.image.load("files/img/heart.png")  # Изображение сердечка

    egg_width, egg_height = egg_image.get_size()
    basket_width, basket_height = basket_left_image.get_size()
    heart_width, heart_height = heart_image.get_size()

    basket_x = SCREEN_WIDTH // 2 - basket_width // 2
    basket_y = SCREEN_HEIGHT - basket_height - 10

    basket_direction = "left"

    eggs = []

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

    # Главный цикл игры
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and basket_x > 0:
            basket_x -= 5
            basket_direction = "left"  # Изменение направления корзины
        if keys[pygame.K_RIGHT] and basket_x < SCREEN_WIDTH - basket_width:
            basket_x += 5
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
            pygame.display.set_caption('Мир Труда')
            running = False
            game_window()
        draw_objects()
        pygame.display.flip()


def builder_game():
    text_surface, text_rect = create_font(54, 'ЗДЕСЬ СКОРО ЧТО-ТО ПОЯВИТСЯ', WIDTH, HEIGHT)
    arrow_button = Button('files/img/arrow_left.png', 'files/img/arrow_left.png', 0, 0, 50, 50)
    screen.fill('blue')

    running = True
    while running:
        draw_buttons_group([arrow_button], screen)
        screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if arrow_button.is_hovered:
                        game_window()

        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Мир Труда')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    image_background = pygame.image.load('files/img/brickstone_background.jpg')
    image_background = pygame.transform.scale(image_background, (WIDTH, HEIGHT))
    screen.blit(image_background, (0, 0))

    main_menu()
