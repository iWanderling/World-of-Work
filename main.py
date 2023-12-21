# Это немного (пока что), но это честная работа

import pygame
from variables import RUNNING, WIDTH, HEIGHT


# Класс, создающий объект кнопки в главном меню игры
class MenuButton:
    def __init__(self, x, y, width, height, image_text):
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


def terminate():
    RUNNING = False
    pygame.quit()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Мир Труда')
    screen.fill('white')
    image_background = pygame.image.load('files/img/factory_background.jpg')
    image_background = pygame.transform.scale(image_background, (WIDTH, HEIGHT))

    screen.blit(image_background, (0, 0))

    play = MenuButton(WIDTH // 2 - 75, 70, 150, 70, 'Играть')
    settings = MenuButton(WIDTH // 2 - 75, 170, 150, 70, 'Настройки')
    exit_ = MenuButton(WIDTH // 2 - 75, 270, 150, 70, 'Выход')

    buttons = [play, settings, exit_]
    while RUNNING:
        for b in buttons:
            b.draw(screen)
            b.check_hover(pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in buttons:
                        button.soundplay()
                    if exit_.is_hovered:
                        RUNNING = False
        pygame.display.flip()
