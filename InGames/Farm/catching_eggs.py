import pygame
import random

pygame.init()

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
pygame.display.set_caption("Волк ловит")

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
        running = False
    draw_objects()
    pygame.display.flip()

pygame.quit()