import os
from pygame import quit, mouse, QUIT


# Переменные для ширины и высоты экрана
WIDTH, HEIGHT = 600, 400
os.environ['SDL_VIDEO_CENTERED'] = '1'  # центрирование окна

with open('settings.txt') as f:
    DIFFICULT_K = {'Легкий': 1, 'Средний': 2, 'Высокий': 3}[str(f.readlines()[0])]
