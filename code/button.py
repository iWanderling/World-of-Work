import pygame
from os import path  # для загрузки шрифта и звука
from data import Images  # для загрузки изображений


# размеры монитора пользователя
WIDTH, HEIGHT = pygame.display.set_mode().get_size()


# Класс для создания кнопок. От него идут классы для создания кнопок меню и локаций
class Button(pygame.sprite.Sprite):
    # передаём в func - функцию, в качестве параметра передаём функцию gameLobby (если это необходимо)
    def __init__(self, *group, func, par=None,
                 images=Images.menu_buttons, x=WIDTH // 2 - 75, text=None, y=HEIGHT // 2 - 150, size=(150, 75)):

        super().__init__(*group)
        self.parameter = par  # параметр функции (используется в играх)
        self.stock_image = pygame.transform.scale(images[0], size)  # обычное изображение кнопки
        self.hover_image = pygame.transform.scale(images[1], size)  # яркое изображение кнопки (для наведения мыши)
        self.function = func  # функция

        # Загрузка основного изображения
        self.image = self.stock_image
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Создаём текст на кнопке, если он задан
        if text is not None:
            font = pygame.font.Font(f'../data/{"fonts"}/appetite.ttf', 20)  # создаём шрифт
            self.text_surface = font.render(text, True, 'white')  # поверхность текста
            self.text_rect = self.text_surface.get_rect()  # область текста
            width, height = self.rect.size  # размеры области кнопки (для корректного вычисления координат текста)
            W, H = self.text_surface.get_size()  # размеры поверхности текста
            self.stock_image.blit(self.text_surface, (width // 2 - W // 2, height // 2 - H // 2))  # отображаем текст
            self.hover_image.blit(self.text_surface, (width // 2 - W // 2, height // 2 - H // 2))  # отображаем текст

        # Загрузка звукового эффекта при нажатии кнопки
        self.sound = pygame.mixer.Sound('../data/sounds/pressed.mp3')

    def update(self, event):
        # обработка наведения и нажатия на кнопку
        mouse_pos = pygame.mouse.get_pos()
        mask_pos = mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y
        if self.rect.collidepoint(*mouse_pos) and self.mask.get_at(mask_pos):
            self.image = self.hover_image
            if event.type == pygame.MOUSEBUTTONDOWN:  # если кнопка нажата - проигрываем звук
                if event.button == 1:
                    self.sound.play()
                    self.handler()  # запускаем функцию, которая привязана к кнопке
        else:
            self.image = self.stock_image

    # запускаем переданную функцию (если она существует)
    def handler(self):
        if self.parameter is not None:
            self.function(self.parameter)  # для обработки функции с параметром (используется в функциях всех 3 игр)
        else:
            self.function()  # простая обработка функции
