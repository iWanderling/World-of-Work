import pygame
from settings import Images
from random import random, choice, randint

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 500  # размеры окна
FPS = 60  # количество кадров в секунду
FONT = pygame.font.Font('files/fonts/appetite.ttf', 36)  # шрифт счётчика

# Игровые переменные:
egg_speed = 3  # скорость падения предметов (зависит от выбранной сложности)
player_speed = 3  # скорость игрока
lives = 5
score = 0

# Создаем отдельный поверхностный объект для затемнения экрана (для паузы)
dim_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
dim_surface.set_alpha(150)  # Устанавливаем прозрачность


# пауза
def pause(scr: pygame.surface.Surface):
    scr.blit(dim_surface, (0, 0))  # Затемнение экрана
    pause_text = FONT.render("Пауза. Нажмите P, чтобы продолжить", True, (255, 255, 255))
    scr.blit(pause_text, (63, SCREEN_HEIGHT // 2 - 20))  # отображение текста


# падающие предметы
class Items(pygame.sprite.Sprite):
    egg_img = pygame.image.load(Images.egg_img)
    apple_img = pygame.image.load(Images.apple_img)

    img_list = (egg_img, apple_img)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = choice(self.img_list)
        self.image = pygame.transform.scale(self.image, (100, 80))
        self.mask = pygame.mask.from_surface(self.image)  # маска объекта

        self.rect = self.image.get_rect()
        self.rect.x = randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = 0

    def update(self):
        global lives, score, farmer
        self.rect = self.rect.move(0, egg_speed)  # передвижение предмета (падение)

        if pygame.sprite.collide_mask(self, farmer):  # обработка столкновения по маске
            score += 1
            self.kill()

        if self.rect.y > SCREEN_HEIGHT:  # обработка падения предмета (если игрок не смог поймать предмет)
            lives -= 1
            self.kill()


# фермер
class Farmer(pygame.sprite.Sprite):
    farmer_left_img = pygame.image.load(Images.farmer_left_img)  # фермер, который идёт влево
    farmer_left_img = pygame.transform.scale(farmer_left_img, (150, 150))

    farmer_right_img = pygame.image.load(Images.farmer_right_img)  # фермер, который идёт вправо
    farmer_right_img = pygame.transform.scale(farmer_right_img, (150, 150))

    def __init__(self, *group):
        super().__init__(*group)
        self.direction = -1

        self.image = self.farmer_left_img
        self.mask = pygame.mask.from_surface(self.image)  # maska
        self.rect = self.image.get_rect()

        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - 150

    def update(self):
        if self.direction > 0:  # передвижение влево или вправо
            self.image = self.farmer_right_img
        else:
            self.image = self.farmer_left_img

        if -5 <= self.rect.x + player_speed * self.direction <= SCREEN_WIDTH - 145:
            self.rect = self.rect.move(player_speed * self.direction, 0)


# Игра: Весёлый фермер
def Happy_Farmer():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    heart_img = pygame.image.load(Images.heart_img)  # сердца
    heart_width, heart_height = heart_img.get_size()  # размеры сердец

    # фон игры
    farm_background = pygame.image.load(Images.farm_img)
    farm_background = pygame.transform.scale(farm_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Создаем отдельный поверхностный объект для затемнения экрана (для паузы)
    dim_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    dim_surface.set_alpha(150)  # Устанавливаем прозрачность

    paused = False  # поставлена ли игра на паузу
    all_items = pygame.sprite.Group()  # все падающие предметы

    farmer_group = pygame.sprite.Group()  # фермер
    global farmer
    farmer = Farmer(farmer_group)  # экземпляр класса фермера

    # Главный цикл игры
    clock = pygame.time.Clock()
    anim = 0
    running = True
    while running:
        anim += 1
        # отрисовка всех изображений на экране
        screen.blit(farm_background, (0, 0))
        all_items.draw(screen)
        farmer_group.draw(screen)

        # отображение оставшегося количества сердец
        for i in range(lives):
            screen.blit(heart_img, (10 + i * (heart_width + 5), 10))

        # Проверка: поставлена ли игра на паузу
        if paused:
            pause(screen)
        else:
            all_items.update()

        # отображение счета в углу
        screen.blit(FONT.render(f"Счёт: {score}", True, (0, 0, 0)), (SCREEN_WIDTH - 150, 10))

        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused

        # если игра не на паузе - продолжаем обработку событий:
        if not paused:
            keys = pygame.key.get_pressed()
            # обрабатываем движение фермера влево
            if keys[pygame.K_LEFT]:
                farmer.direction = -1
                farmer_group.update()

            # обрабатываем движение фермера вправо
            elif keys[pygame.K_RIGHT]:
                farmer.direction = 1
                farmer_group.update()

            # Добавление нового яйца с вероятностью 2% (за один игровой кадр)
            if random() < 0.02:
                Items(all_items)

            # если количество жизней кончилось - завершаем игру
            if not lives:
                return False

        clock.tick(FPS)
        pygame.display.flip()
