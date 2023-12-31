FPS = 240  # количество кадров
TILE = 35  # размер плитки
SCORE = ROWS = 0  # очки, собранные ряды
WIDTH, HEIGHT = 10, 20  # TILE
GAME_WINDOW_SIZE = WIDTH * TILE, HEIGHT * TILE  # игровое окно
WINDOW_SIZE = GAME_WINDOW_SIZE[0] + 200, GAME_WINDOW_SIZE[1]


# координаты падающей фигуры, скорость падения
FALL_CURRENT_POSITION, FALL_SPEED = 0, 100

# игровое поле (нужно для отрисовки игрового процесса)
GAME_FIELD = [[0 for x in range(WIDTH)] for y in range(HEIGHT)]


# Координаты фигур (для отрисовки)
FIGURES_POSITION = [[(-1, 0), (-1, 1), (0, 0), (0, -1)],  # ⚡
                    [(0, -1), (0, -2), (0, 0), (0, 1)],  # |
                    [(0, -1), (-1, -1), (-1, 0), (0, 0)],  # █
                    [(0, 0), (0, -1), (0, 1), (-1, -1)],  # ⅃
                    [(0, 0), (0, -1), (0, 1), (-1, 0)],  # -|
                    [(0, 0), (0, -1), (0, 1), (1, -1)],  # L
                    [(0, 0), (-1, 0), (0, 1), (-1, -1)]]  # .-
