import pygame
from random import randrange

GAME_HEIGHT = 800
GAME_WIDTH = 800
TILE_SIZE = 25
COLS = int(GAME_WIDTH / TILE_SIZE)
ROWS = int(GAME_HEIGHT / TILE_SIZE)

clock = pygame.time.Clock()
speed = 10

pygame.init()
screen = pygame.display.set_mode([GAME_HEIGHT, GAME_WIDTH])


class Player:
    def __init__(self, spawn_x, spawn_y, up_key, down_key, left_key, right_key, color="blue", direction="right"):
        self.alive = True
        self.parts = []
        self.color = color
        self.up_key = up_key
        self.down_key = down_key
        self.left_key = left_key
        self.right_key = right_key

        self.rect = pygame.Rect(spawn_x, spawn_y, TILE_SIZE, TILE_SIZE)
        self.direction = direction

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def addPart(self):
        self.parts.append()

    def handleKeyEvent(self, event):
        if event.key == pygame.K_UP:
            self.direction = "up"
        elif event.key == pygame.K_DOWN:
            self.direction = "down"
        elif event.key == pygame.K_LEFT:
            self.direction = "left"
        elif event.key == pygame.K_RIGHT:
            self.direction = "right"

    def update(self):
        if self.alive:
            # Determine next position
            d = self.direction
            x, y = self.rect.x, self.rect.y
            if d == "up":
                y -= TILE_SIZE
            elif d == "down":
                y += TILE_SIZE
            elif d == "left":
                x -= TILE_SIZE
            elif d == "right":
                x += TILE_SIZE

            # Test new position for collisions
            if x + TILE_SIZE > GAME_WIDTH:
                x -= TILE_SIZE
                self.alive = False
            elif x < 0:
                x += TILE_SIZE
                self.alive = False
            elif y + TILE_SIZE > GAME_HEIGHT:
                y -= TILE_SIZE
                self.alive = False
            elif y < 0:
                y += TILE_SIZE
                self.alive = False

            # Apply new position
            self.rect.update((x, y), (TILE_SIZE, TILE_SIZE))

        self.draw()


def randSpawnPos():
    x, y = 0, 0
    found = False
    while not found:
        found = True
        (x, y) = round(randrange(0, COLS)) * TILE_SIZE, round(randrange(0, ROWS)) * TILE_SIZE
        # if head.rect.x == x or head.rect.y == y:
        #     print("Head Convergence")
        #     found = False
        # for apple in apples:
        #     if apple.position == (x, y):
        #         print("Apple Convergence")
        #         found = False
    # Test position for collisions to prevent overlap
    return x, y


def drawGrid():
    for col in range(0, COLS):
        x1 = TILE_SIZE * col
        y1 = 0
        x2 = TILE_SIZE * col
        y2 = GAME_HEIGHT
        pygame.draw.line(screen, "black", (x1, y1), (x2, y2))
    for row in range(0, ROWS):
        x1 = 0
        y1 = TILE_SIZE * row
        x2 = GAME_WIDTH
        y2 = TILE_SIZE * row
        pygame.draw.line(screen, "black", (x1, y1), (x2, y2))


players = []


def tick():
    screen.fill((255, 255, 255))
    drawGrid()
    for player in players:
        player.update()


def init():
    x, y = randSpawnPos()
    players.append(Player(x, y, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, "red"))
    x, y = randSpawnPos()
    players.append(Player(x, y, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, "red"))
    running = True
    while running:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                for player in players:
                    player.handleKeyEvent(event)

        # Content Update
        tick()

        # Engine Update
        pygame.display.flip()
        clock.tick(speed)

    pygame.quit()


init()
