from os import environ
from button import *
from tetris import *
from plane import *
from farm import *

environ['SDL_VIDEO_CENTERED'] = '1'  # центрирование окна
play = True
pygame.mixer.init()


class Slider(pygame.sprite.Sprite):
    def __init__(self, group, x, y, width, height):
        super().__init__(group)
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.color = pygame.Color('lightskyblue3')
        self.marker_rect = pygame.Rect(0, 760, 10, height)  # Размер маркера
        self.active = False
        self.value = 0.5  # Изначальное положение слайдера (0.5 - посередине)

    def get_value(self):
        return self.value

    def set_active(self, active):
        self.active = active

    def handle_event(self, event):
        if self.active:
            if event.type == pygame.MOUSEMOTION:
                mouse_x, _ = event.pos
                mouse_x = max(self.rect.left, min(mouse_x, self.rect.right))
                self.value = (mouse_x - self.rect.left) / self.rect.width
                self.marker_rect.left = mouse_x - self.marker_rect.width // 2

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.active = False

    def update(self, *args):
        pass  # Нет необходимости в этом методе

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        pygame.draw.rect(screen, (255, 0, 0), self.marker_rect)



# Окно ввода имени (самое первое окно, которое появляется при запуске игры)
def setPlayerName():
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
    volume_slider = Slider(menu_group, x=WIDTH - 150, y=HEIGHT - 50, width=100, height=20)

    if play:
        sound = pygame.mixer.Sound('../data/sounds/menu.mp3')
        sound.play()
        play = False

    with open('../settings/username.txt') as username_file:
        player_name = username_file.read()

    font_player_name = pygame.font.Font(None, 24)
    player_name_text = font_player_name.render(f"Игрок: {player_name}", True, (255, 255, 255))
    player_name_rect = player_name_text.get_rect(bottomleft=(10, HEIGHT - 10))
    screen.blit(player_name_text, player_name_rect)

    running = True
    while running:
        screen.blit(menu_background, (0, 0))
        menu_group.draw(screen)

        # Обновление и отрисовка слайдера
        volume_slider.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if volume_slider.rect.collidepoint(event.pos):
                    volume_slider.set_active(True)
                else:
                    volume_slider.set_active(False)

            elif event.type == pygame.MOUSEMOTION:
                volume_slider.handle_event(event)
                # Изменение громкости в зависимости от положения ползунка
                pygame.mixer.music.set_volume(volume_slider.get_value())
                #print(volume_slider.get_value())

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
