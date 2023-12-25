import os
import pygame
from base_functions import terminate, draw_buttons_group, event_quit


WIDTH, HEIGHT = 600, 400
RUNNING = 1
os.environ['SDL_VIDEO_CENTERED'] = '1'


# Класс, создающий объект кнопки в главном меню игры
class MenuButton:
    def __init__(self, x, y, image_text, width=150, height=70):
        self.image_text = image_text
        self.is_hovered = False
        self.is_pressed = False

        self.image = pygame.image.load('files/img/button.png')
        self.image = pygame.transform.scale(self.image, (width, height))  # масштабирование картинки под размер кнопки

        self.hover_image = pygame.image.load('files/img/button_hover.png')
        self.hover_image = pygame.transform.scale(self.hover_image, (width, height))

        self.sound = pygame.mixer.Sound('files/sounds/sound.mp3')
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        if self.is_hovered:
            current_image = self.hover_image
        else:
            current_image = self.image
        screen.blit(current_image, self.rect.topleft)

        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.image_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    # Проверка: наведена ли мышь на кнопку
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    # Обработчик событий нажатия на кнопку, если кнопка нажата, воспроизведется звук
    def soundplay(self):
        if self.is_hovered:
            self.sound.play()


# Окно главного меню
def main_menu():
    play = MenuButton(WIDTH // 2 - 75, 70, 'Играть')
    settings = MenuButton(WIDTH // 2 - 75, 170, 'Настройки')
    exit_ = MenuButton(WIDTH // 2 - 75, 270, 'Выход')
    menu_buttons = [play, settings, exit_]

    screen.blit(image_background, (0, 0))

    while RUNNING:
        draw_buttons_group(menu_buttons, screen)

        for event in pygame.event.get():
            event_quit(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    # Проигрывание звука при нажатии кнопки
                    for btn in menu_buttons:
                        btn.soundplay()

                    if play.is_hovered:
                        game_window()

                    if exit_.is_hovered:
                        terminate()

                    if settings.is_hovered:
                        settings_menu()

        pygame.display.flip()


# Окно с настройками
def settings_menu():
    sound_settings = MenuButton(WIDTH // 2 - 75, 70, 'Звук')
    difficult_settings = MenuButton(WIDTH // 2 - 75, 170, 'Сложность')
    back_button = MenuButton(WIDTH // 2 - 75, 270, 'Назад')
    settings_buttons = [sound_settings, difficult_settings, back_button]

    screen.blit(image_background, (0, 0))

    while RUNNING:
        draw_buttons_group(settings_buttons, screen)

        for event in pygame.event.get():
            event_quit(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    # Проигрывание звука при нажатии кнопки
                    for btn in settings_buttons:
                        btn.soundplay()

                    if sound_settings.is_hovered:
                        sound_menu()

                    if difficult_settings.is_hovered:
                        difficult_menu()

                    if back_button.is_hovered:
                        main_menu()

        pygame.display.flip()


# Окно с выбором сложности
def difficult_menu():

    with open('settings.txt') as f:
        diff = str(f.readlines()[0])

    font = pygame.font.Font(None, 54)
    text_surface = font.render(f'Текущий уровень: {diff}', False, 'white')
    text_rect = text_surface.get_rect(center=(WIDTH // 2, 40))

    easy_difficult = MenuButton(WIDTH // 2 - 75, 70, 'Легкий')
    medium_difficult = MenuButton(WIDTH // 2 - 75, 170, 'Средний')
    hard_difficult = MenuButton(WIDTH // 2 - 75, 270, 'Высокий')
    difficult_buttons = [easy_difficult, medium_difficult, hard_difficult]

    screen.blit(image_background, (0, 0))

    while RUNNING:
        draw_buttons_group(difficult_buttons, screen)
        screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            event_quit(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    # Проигрывание звука при нажатии кнопки
                    for btn in difficult_buttons:
                        if btn.is_hovered:
                            with open('settings.txt', 'w') as f:
                                f.write(btn.image_text)
                            btn.soundplay()
                            settings_menu()
                            break

        pygame.display.flip()


def sound_menu():
    font = pygame.font.Font(None, 36)
    text_surface = font.render('Регулируйте звук стрелочками (влево и вправо)', False, 'white')
    text_rect = text_surface.get_rect(center=(WIDTH // 2, 50))
    screen.blit(image_background, (0, 0))

    back_button = MenuButton(WIDTH // 2 - 75, 270, 'Назад')

    while RUNNING:
        draw_buttons_group([back_button], screen)
        screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            event_quit(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and back_button.is_hovered:
                    settings_menu()

        pygame.display.flip()


def game_window():
    WIDTH, HEIGHT = 1000, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    image_background = pygame.image.load('files/img/brickstone_background.jpg')
    image_background = pygame.transform.scale(image_background, (WIDTH, HEIGHT))
    screen.blit(image_background, (0, 0))


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Мир Труда')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    image_background = pygame.image.load('files/img/brickstone_background.jpg')
    image_background = pygame.transform.scale(image_background, (WIDTH, HEIGHT))
    screen.blit(image_background, (0, 0))

    main_menu()
