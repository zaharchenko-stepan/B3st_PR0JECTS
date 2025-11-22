import pygame
import math

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 1000, 700
FPS = 60
BLOCK_SIZE = 50
GRID_SIZE = 20

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
GREEN = (34, 139, 34)
RED = (220, 20, 60)
GRAY = (128, 128, 128)
BROWN = (139, 69, 19)
YELLOW = (255, 215, 0)
SKY_BLUE = (135, 206, 235)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Roblox на Python")
clock = pygame.time.Clock()


# Класс для блоков
class Block:
    def __init__(self, x, y, z, color):
        self.x = x
        self.y = y
        self.z = z
        self.color = color
        self.size = BLOCK_SIZE

    def draw_isometric(self, screen, camera_x, camera_y, camera_z):
        # Изометрическая проекция
        iso_x = (self.x - self.y) * self.size / 2
        iso_y = (self.x + self.y) * self.size / 4 - self.z * self.size / 2

        # Применение камеры
        screen_x = iso_x + WIDTH / 2 - camera_x
        screen_y = iso_y + HEIGHT / 2 - camera_y + camera_z

        # Рисование куба
        # Верхняя грань
        top_points = [
            (screen_x, screen_y),
            (screen_x + self.size / 2, screen_y + self.size / 4),
            (screen_x, screen_y + self.size / 2),
            (screen_x - self.size / 2, screen_y + self.size / 4)
        ]

        # Левая грань
        left_points = [
            (screen_x - self.size / 2, screen_y + self.size / 4),
            (screen_x, screen_y + self.size / 2),
            (screen_x, screen_y + self.size),
            (screen_x - self.size / 2, screen_y + self.size * 3 / 4)
        ]

        # Правая грань
        right_points = [
            (screen_x + self.size / 2, screen_y + self.size / 4),
            (screen_x, screen_y + self.size / 2),
            (screen_x, screen_y + self.size),
            (screen_x + self.size / 2, screen_y + self.size * 3 / 4)
        ]

        # Рисование граней с затемнением
        top_color = self.color
        left_color = tuple(max(0, c - 40) for c in self.color)
        right_color = tuple(max(0, c - 60) for c in self.color)

        pygame.draw.polygon(screen, left_color, left_points)
        pygame.draw.polygon(screen, right_color, right_points)
        pygame.draw.polygon(screen, top_color, top_points)

        # Обводка
        pygame.draw.polygon(screen, BLACK, top_points, 2)
        pygame.draw.polygon(screen, BLACK, left_points, 2)
        pygame.draw.polygon(screen, BLACK, right_points, 2)


# Класс для игрока
class Player:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.size = BLOCK_SIZE * 0.8
        self.speed = 0.3

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

    def jump(self):
        if self.z == 0:
            self.z = 2

    def update(self):
        # Гравитация
        if self.z > 0:
            self.z -= 0.1
        if self.z < 0:
            self.z = 0

    def draw_isometric(self, screen, camera_x, camera_y, camera_z):
        # Изометрическая проекция игрока
        iso_x = (self.x - self.y) * self.size / 2
        iso_y = (self.x + self.y) * self.size / 4 - self.z * self.size / 2

        screen_x = iso_x + WIDTH / 2 - camera_x
        screen_y = iso_y + HEIGHT / 2 - camera_y + camera_z

        # Рисование игрока (упрощенный персонаж)
        # Голова
        head_size = self.size / 3
        pygame.draw.circle(screen, RED, (int(screen_x), int(screen_y - self.size / 2)), int(head_size))

        # Тело
        body_rect = pygame.Rect(screen_x - head_size / 2, screen_y - self.size / 2, head_size, self.size / 2)
        pygame.draw.rect(screen, BLUE, body_rect)

        # Обводка
        pygame.draw.circle(screen, BLACK, (int(screen_x), int(screen_y - self.size / 2)), int(head_size), 2)
        pygame.draw.rect(screen, BLACK, body_rect, 2)


# Класс для палитры блоков
class BlockPalette:
    def __init__(self):
        self.blocks = [
            ("Трава", GREEN),
            ("Камень", GRAY),
            ("Дерево", BROWN),
            ("Золото", YELLOW),
            ("Вода", BLUE),
            ("Удалить", RED)
        ]
        self.selected = 0

    def draw(self, screen):
        x_offset = 10
        y_offset = 10

        for i, (name, color) in enumerate(self.blocks):
            # Рисование квадрата блока
            rect = pygame.Rect(x_offset, y_offset + i * 60, 50, 50)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK if i != self.selected else YELLOW, rect, 3)

            # Название блока
            font = pygame.font.Font(None, 24)
            text = font.render(name, True, BLACK)
            screen.blit(text, (x_offset + 60, y_offset + i * 60 + 15))

    def select_next(self):
        self.selected = (self.selected + 1) % len(self.blocks)

    def select_prev(self):
        self.selected = (self.selected - 1) % len(self.blocks)

    def get_selected_color(self):
        return self.blocks[self.selected][1]

    def is_delete_mode(self):
        return self.selected == len(self.blocks) - 1


# Инициализация игры
blocks = []
player = Player(0, 0, 0)
palette = BlockPalette()

# Создание начального пола
for x in range(-5, 6):
    for y in range(-5, 6):
        blocks.append(Block(x, y, -1, GRAY))

camera_x = 0
camera_y = 0
camera_z = 0

# Главный игровой цикл
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
            elif event.key == pygame.K_q:
                palette.select_prev()
            elif event.key == pygame.K_e:
                palette.select_next()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Размещение блоков
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Простое размещение блока в направлении игрока
            grid_x = round(player.x)
            grid_y = round(player.y)
            grid_z = round(player.z)

            if event.button == 1:  # Левая кнопка мыши
                if palette.is_delete_mode():
                    # Удаление ближайшего блока
                    for block in blocks[:]:
                        if abs(block.x - grid_x) <= 1 and abs(block.y - grid_y) <= 1 and abs(block.z - grid_z) <= 1:
                            blocks.remove(block)
                            break
                else:
                    # Размещение блока
                    blocks.append(Block(grid_x, grid_y, grid_z, palette.get_selected_color()))

    # Управление игроком
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0

    if keys[pygame.K_w]:
        dy += 1
    if keys[pygame.K_s]:
        dy -= 1
    if keys[pygame.K_a]:
        dx -= 1
    if keys[pygame.K_d]:
        dx += 1

    if dx != 0 or dy != 0:
        # Нормализация диагонального движения
        length = math.sqrt(dx * dx + dy * dy)
        dx /= length
        dy /= length
        player.move(dx, dy)

    player.update()

    # Камера следует за игроком
    camera_x = (player.x - player.y) * BLOCK_SIZE / 2
    camera_y = (player.x + player.y) * BLOCK_SIZE / 4
    camera_z = player.z * BLOCK_SIZE / 2

    # Отрисовка
    screen.fill(SKY_BLUE)

    # Сортировка блоков для правильного отображения
    blocks_sorted = sorted(blocks, key=lambda b: (b.x + b.y, -b.z))

    # Рисование блоков
    for block in blocks_sorted:
        block.draw_isometric(screen, camera_x, camera_y, camera_z)

    # Рисование игрока
    player.draw_isometric(screen, camera_x, camera_y, camera_z)

    # Рисование палитры
    palette.draw(screen)

    # Инструкции
    font = pygame.font.Font(None, 24)
    instructions = [
        "WASD - Движение",
        "Пробел - Прыжок",
        "Q/E - Выбор блока",
        "ЛКМ - Разместить/Удалить",
        "ESC - Выход"
    ]

    for i, instruction in enumerate(instructions):
        text = font.render(instruction, True, BLACK)
        screen.blit(text, (WIDTH - 220, 10 + i * 30))

    # Обработка выхода через ESC
    if keys[pygame.K_ESCAPE]:
        running = False

    pygame.display.flip()

pygame.quit()