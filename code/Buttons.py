import pygame
from os import path
from data import Images


WIDTH, HEIGHT = pygame.display.set_mode().get_size()


# Класс для создания кнопок. От него идут классы для создания кнопок меню и локаций (func - функция, привязана к кнопке)
class Button(pygame.sprite.Sprite):
    def __init__(self, *group, func, images=Images.menu_buttons, x=WIDTH // 2 - 75, text=None, y=HEIGHT // 2 - 150,
                 size=(150, 75)):

        super().__init__(*group)
        self.pressed = False
        self.stock_image = pygame.transform.scale(images[0], size)
        self.hover_image = pygame.transform.scale(images[1], size)
        self.function = func
        # Загрузка основного изображения
        self.image = self.stock_image
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Создаём текст на кнопке, если он задан
        if text is not None:
            font = pygame.font.Font(path.join(f'..\data\{"fonts"}', 'appetite.ttf'), 26)  # создаём шрифт
            self.text_surface = font.render(text, True, 'white')
            self.text_rect = self.text_surface.get_rect()
            width, height = self.rect.size
            W, H = self.text_surface.get_size()
            self.stock_image.blit(self.text_surface, (width // 2 - W // 2, height // 2 - H // 2))  # отображаем текст
            self.hover_image.blit(self.text_surface, (width // 2 - W // 2, height // 2 - H // 2))  # отображаем текст

        # Загрузка звукового эффекта при нажатии кнопки
        self.sound = pygame.mixer.Sound(path.join('..\data\sounds', 'sound.mp3'))

    def update(self, event):
        # обработка наведения и нажатия на кнопку
        mouse_pos = pygame.mouse.get_pos()
        mask_pos = mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y
        if self.rect.collidepoint(*mouse_pos) and self.mask.get_at(mask_pos):
            self.image = self.hover_image
            if event.type == pygame.MOUSEBUTTONDOWN:  # если кнопка нажата - проигрываем звук
                if event.button == 1:
                    self.sound.play()
                    self.pressed = True
                    self.handler()  # запускаем функцию, которая привязана к кнопке
            else:
                self.pressed = False
        else:
            self.image = self.stock_image
            self.pressed = False

    def handler(self):
        self.function()
