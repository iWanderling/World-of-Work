import pygame
from settings import WIDTH

# Создать шрифт (параметры: размер, текст, x, y (относительно центра), цвет, тип шрифта, сглаживание)
def create_font(size: int, text: str, x: int, y: int, color='white', font_type=None, smoothing=False) -> tuple:
    font = pygame.font.Font(font_type, size)
    text_surface = font.render(text, smoothing, color)

    return text_surface, text_surface.get_rect(center=(x, y))


# Отрисовка кнопок и обработка наведения мыши на них
def draw_buttons_group(group, screen):
    for b in group:
        b.draw(screen)
        b.check_hover(pygame.mouse.get_pos())


# Класс для создания кнопок. От него идут классы для создания кнопок меню и локаций
class Button:
    def __init__(self, img, hover_img, x, y, width=300, height=300):

        # Наведен ли курсор на кнопку
        self.is_hovered = False

        # Загрузка основного изображения
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (width, height))  # масштабирование картинки под размер кнопки
        self.mask = pygame.mask.from_surface(self.image)
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
        self.is_hovered = self.rect.collidepoint(*mouse_pos)

    # Обработчик событий нажатия на кнопку, если кнопка нажата, воспроизведется звук
    def soundplay(self):
        if self.is_hovered:
            self.sound.play()


# Класс для создания кнопок главного меню (Наследуется от Button)
class MenuButton(Button):
    def __init__(self, x=WIDTH // 2 - 75, y=70, image_text='NONE', width=150, height=70):
        super().__init__('files/img/interface/button.png', 'files/img/interface/button_hover.png', x, y, width, height)
        self.image_text = image_text  # Текст на кнопке

        # Создаём текст
        x, y = self.rect.center
        self.text_surface, self.text_rect = create_font(font_type='files/fonts/appetite.ttf',
                                                        size=25, text=self.image_text, x=x, y=y, smoothing=True)

    # Отрисовка кнопки с текстом
    def draw(self, screen):
        if self.is_hovered:
            current_image = self.hover_image
        else:
            current_image = self.image
        screen.blit(current_image, self.rect.topleft)
        screen.blit(self.text_surface, self.text_rect)