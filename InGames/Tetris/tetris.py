from functions import *
from copy import deepcopy


# начальное расположение новой фигуры
figures = [[pygame.Rect(x + WIDTH // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in FIGURES_POSITION]

# квадратик (1/4 часть) одной фигуры
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)

# текущая фигура
current_figure = deepcopy(choice(figures))
next_figure = deepcopy(choice(figures))

# проверка на выход фигуры за границы (левой, правой, а также столкновения с полом)
def check_borders(index: int) -> bool:
    if current_figure[index].x < 0 or current_figure[i].x > WIDTH - 1:
        return False
    elif current_figure[index].y > HEIGHT - 1 or GAME_FIELD[current_figure[i].y][current_figure[i].x]:
        return False
    return True


# игровой цикл
def Tetris_Game():
    pygame.init()
    pygame.display.set_caption('Тетрис - Юный Строитель')
    screen = pygame.display.set_mode(WINDOW_SIZE)  # окно
    clock = pygame.time.Clock()  # FPS
    # background of game field
    game_window_background = pygame.transform.scale(pygame.image.load('bricks/tetris-background-game-window.jpg'),
                                                    GAME_WINDOW_SIZE)
    window_background = pygame.transform.scale(pygame.image.load('bricks/tetris-background-window.png'), WINDOW_SIZE)

    sound = pygame.mixer.Sound('sounds/collect-row.mp3')  # звук, который проигрывается при создании целого ряда
    brick = create_new_brick()  # создание кирпичика
    next_brick = create_new_brick()

    SCORE_FONT = pygame.font.Font('sunday.ttf', 50)
    SCORE_FONT = SCORE_FONT.render(str(SCORE), True, pygame.Color('red'))

    while True:
        screen.blit(window_background, (0, 0))
        screen.blit(game_window_background, (0, 0))

        X_DIRECTION = 0  # перемещение по оси X
        ROTATION = False  # переменная для переворачивания фигуры
        old_figure = deepcopy(current_figure)  # копия текущей фигуры (читайте далее)

        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # выход
                exit()
            if event.type == pygame.KEYDOWN:  # обработка перемещения фигуры влево и вправо
                if event.key == pygame.K_RIGHT:
                    X_DIRECTION += 1  # перемещение по x ->>
                elif event.key == pygame.K_LEFT:
                    X_DIRECTION -= 1  # перемещение по x <<-
                elif event.key == pygame.K_SPACE:  # переворачивание текущей фигуры
                    ROTATION = True

                elif event.key == pygame.K_ESCAPE:  # ещё один выход (на Esc)
                    exit()

        # переворачивание текущей фигуры (по часовой стрелке, на клавишу SPACE)
        if ROTATION:
            FIGURE_CENTER = current_figure[0]
            for i in range(4):
                x = current_figure[i].y - FIGURE_CENTER.y
                y = current_figure[i].x - FIGURE_CENTER.x
                current_figure[i].x = FIGURE_CENTER.x - x
                current_figure[i].y = FIGURE_CENTER.y + y

        # отрисовка текущей фигуры
        for i in range(4):
            figure_rect.x = current_figure[i].x * TILE
            figure_rect.y = current_figure[i].y * TILE
            screen.blit(brick, figure_rect)

        # движение текущей фигуры по горизонтальной оси (все квадратики фигуры смещаются на +-1 квадратик)
        # фигура не может забежать за границу, поэтому сохраняем копию текущей фигуры, и если граница будет пересечена,
        # то возвратим копию, иначе разрешаем передвижение
        for i in range(4):
            current_figure[i].x += X_DIRECTION
            if not check_borders(i):
                current_figure = deepcopy(old_figure)
                break

        # движение фигуры вниз (обработка падения)
        FALL_CURRENT_POSITION += FALL_SPEED

        # Обработка столкновения фигуры с "полом" экрана. Если фигура упала, то она сохраняется на игровом поле в том
        # виде, в котором она приземлилась, включая цвет. Также создаём следующую фигуру
        if FALL_CURRENT_POSITION > 2000:
            FALL_CURRENT_POSITION = 0
            for i in range(4):
                current_figure[i].y += 1
                if not check_borders(i):
                    for i in range(4):
                        # запоминаем позицию и цвет упавшей фигуры, сохраняем её на поле
                        GAME_FIELD[old_figure[i].y][old_figure[i].x] = brick
                    # создаём новую фигуру
                    current_figure = next_figure
                    brick = next_brick

                    # создаём следующую фигуру
                    next_figure = deepcopy(choice(figures))
                    next_brick = create_new_brick()
                    break

        # поиск заполненных рядов в игровом поле
        row = HEIGHT - 1
        for r in range(HEIGHT - 1, -1, -1):
            count = 0
            for i in range(WIDTH):
                if GAME_FIELD[r][i]:
                    count += 1
                GAME_FIELD[row][i] = GAME_FIELD[r][i]
            if count < WIDTH:
                row -= 1
            # проигрываем звук если создан полный ряд
            else:
                sound.play()
                ROWS += 1
                SCORE = ROWS * 100

        # отрисовка игрового поля
        for y, row in enumerate(GAME_FIELD):
            for x, col in enumerate(row):
                if col:  # отрисовка упавших фигур
                    figure_rect.x, figure_rect.y = x * TILE, y * TILE
                    screen.blit(col, figure_rect)

        # отрисовка текущей фигуры
        for i in range(4):
            figure_rect.x = next_figure[i].x * TILE + 265
            figure_rect.y = next_figure[i].y * TILE + 250
            screen.blit(next_brick, figure_rect)

        SCORE_FONT = pygame.font.Font('sunday.ttf', 25).render(f'Счёт: {SCORE}', True, pygame.Color('aqua'))
        NEXT_FIGURE_FONT = pygame.font.Font('sunday.ttf', 15).render(f'Следующая фигура', True, pygame.Color('aqua'))

        screen.blit(SCORE_FONT, (365, 10))
        screen.blit(NEXT_FIGURE_FONT, (375, 185))
        pygame.display.flip()
        clock.tick(FPS)


Tetris_Game()