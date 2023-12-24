import pygame
from variables import RUNNING, WIDTH, HEIGHT


DIFFICULT = 1

# Завершить работу игры
def terminate():
    RUNNING = False
    pygame.quit()


# Отрисовка кнопок и обработка наведения мыши на них
def draw_buttons_group(gr):
    for b in gr:
        b.draw(screen)
        b.check_hover(pygame.mouse.get_pos())


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
        draw_buttons_group(menu_buttons)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    # Проигрывание звука при нажатии кнопки
                    for btn in menu_buttons:
                        btn.soundplay()

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
        draw_buttons_group(settings_buttons)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

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
    font = pygame.font.Font(None, 54)
    text_surface = font.render('Выберите уровень сложности', False, 'white')
    text_rect = text_surface.get_rect(center=(WIDTH // 2, 40))

    easy_difficult = MenuButton(WIDTH // 2 - 75, 70, 'Легкий')
    medium_difficult = MenuButton(WIDTH // 2 - 75, 170, 'Средний')
    hard_difficult = MenuButton(WIDTH // 2 - 75, 270, 'Высокий')
    difficult_buttons = [easy_difficult, medium_difficult, hard_difficult]

    screen.blit(image_background, (0, 0))

    while RUNNING:
        draw_buttons_group(difficult_buttons)
        screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    # Проигрывание звука при нажатии кнопки
                    for btn in difficult_buttons:
                        if btn.is_hovered:
                            btn.soundplay()
                            DIFFICULT = difficult_buttons.index(btn) + 1
                            main_menu()

        pygame.display.flip()


def sound_menu():
    font = pygame.font.Font(None, 36)
    text_surface = font.render('Регулируйте звук стрелочками (влево и вправо)', True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(WIDTH // 2, 50))
    screen.blit(image_background, (0, 0))

    back_button = MenuButton(WIDTH // 2 - 75, 270, 'Назад')

    while RUNNING:
        draw_buttons_group([back_button])
        screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and back_button.is_hovered:
                    settings_menu()

        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Мир Труда')

    image_background = pygame.image.load('files/img/brickstone_background.jpg')
    image_background = pygame.transform.scale(image_background, (WIDTH, HEIGHT))

    screen.blit(image_background, (0, 0))

    main_menu()
