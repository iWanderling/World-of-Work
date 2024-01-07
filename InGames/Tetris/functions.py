import pygame
from settings import *
from random import choice

# получаем случайный кирпичик (цвет)
def get_random_color() -> str:
    return 'bricks/' + choice(('yellow_brick', 'blue_brick', 'red_brick', 'green_brick', 'aqua_brick', 'brick',
                               'gray_brick', 'pink_brick')) + '.png'


# функция для создания объекта - кирпичика
def create_new_brick() -> pygame.surface.Surface:
    brick = pygame.image.load(get_random_color()).convert_alpha()
    return pygame.transform.scale(brick, (TILE, TILE))