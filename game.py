import pygame
from random import randrange

GAME_HEIGHT = 1000
GAME_WIDTH = 1000
TILE_SIZE = 25
COLS = int(GAME_WIDTH / TILE_SIZE)
ROWS = int(GAME_HEIGHT / TILE_SIZE)
TRAY_HEIGHT = 100
WIN_HEIGHT = GAME_HEIGHT + TRAY_HEIGHT
ITEM_POSSIBILITIES = ["body-part"]

clock = pygame.time.Clock()
speed = 10

pygame.init()
screen = pygame.display.set_mode([GAME_WIDTH, WIN_HEIGHT])
pygame.display.set_caption("Snake Battle")


class Tray:
    def draw(self):
        # Draw horizontal divider
        pygame.draw.line(screen, "black", (0, GAME_HEIGHT), (GAME_WIDTH, GAME_HEIGHT))
        # Draw vertical divider
        pygame.draw.line(screen, "black", ((COLS / 2) * TILE_SIZE, GAME_HEIGHT), ((COLS / 2) * TILE_SIZE, WIN_HEIGHT))

    def update(self):
        self.draw()


class Item_Manager:
    def __init__(self):
        self.items = []
        self.ITEM_LIMIT = 2

    def update(self, players):
        if len(self.items) < self.ITEM_LIMIT:
            for x in range(0, self.ITEM_LIMIT - len(self.items)):
                self.generateRandItem()
        for item in self.items:
            item.update()
        for player in players:
            self.checkPlayerCollision(player)

    def checkPlayerCollision(self, player):
        rect = player.rect
        for item in self.items:
            if rect.x == item.position[0] and rect.y == item.position[1]:
                item.action(player)
                self.removeItem(item)

    def generateRandItem(self):
        n = randrange(0, len(ITEM_POSSIBILITIES))
        i = ITEM_POSSIBILITIES[n]
        if i == "body-part":
            self.addItem(BodyPartItem(randSpawnPos(), ))

    def addItem(self, item):
        self.items.append(item)

    def removeItem(self, item):
        self.items.remove(item)


class BodyPartItem:
    def __init__(self, positionTup):
        self.position = positionTup
        self.rect = pygame.Rect(self.position[0], self.position[1], TILE_SIZE + 1, TILE_SIZE + 1)

    def action(self, player):
        player.bodypart_queue += 1

    def update(self):
        self.draw()

    def draw(self):
        pygame.draw.rect(screen, "green", self.rect)


class BodyPart:
    def __init__(self, start_x, start_y):
        self.rect = pygame.Rect(start_x, start_y, TILE_SIZE + 1, TILE_SIZE + 1)

    def draw(self):
        pygame.draw.rect(screen, '#CD3333', self.rect)

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Player_Manager:
    def __init__(self):
        self.players = []

    def addPlayer(self, spawn_x, spawn_y, up_key, down_key, left_key, right_key, color="blue", direction="right"):
        self.players.append(Player(spawn_x, spawn_y, up_key, down_key, left_key, right_key, color, direction))

    def removePlayer(self, player):
        self.players.remove(player)

    def update(self):
        for player in self.players:
            player.update()

    def keyEvent(self, event):
        for player in self.players:
            player.handleKeyEvent(event)


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
        self.bodypart_queue = 0

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def addNewParts(self, x, y):
        if self.bodypart_queue > 0:
            self.bodypart_queue -= 1
            self.parts.append(BodyPart(x, y))
            print(len(self.parts))

    def handleKeyEvent(self, event):
        if event.key == self.up_key:
            self.direction = "up"
        elif event.key == self.down_key:
            self.direction = "down"
        elif event.key == self.left_key:
            self.direction = "left"
        elif event.key == self.right_key:
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
                x = 0
            elif x < 0:
                x = GAME_WIDTH
            elif y + TILE_SIZE > GAME_HEIGHT:
                y = 0
            elif y < 0:
                y = GAME_HEIGHT

            temp_x, temp_y = self.rect.x, self.rect.y

            # Apply new position to HEAD
            self.rect.update((x, y), (TILE_SIZE, TILE_SIZE))

            # Add new parts
            l = len(self.parts)
            if l == 0:
                self.addNewParts(temp_x, temp_y)
            elif l >= 1:
                for part in self.parts:
                    n = self.parts[index - 1]
                    if index == 0:
                        part.update(temp_x, temp_y)
                    else:
                        p = self.parts[index - 1]
                        part.update(n.rect.x, n.rect.y)
                    index += 1
                self.addNewParts(n.rect.x, n.rect.y)

        self.draw()

        for part in self.parts:
            part.draw()


def randSpawnPos():
    x, y = 0, 0
    found = False
    while not found:
        found = True
        (x, y) = round(randrange(0, COLS)) * TILE_SIZE, round(randrange(0, ROWS)) * TILE_SIZE
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


item_manager = Item_Manager()
player_manager = Player_Manager()
tray = Tray()


def tick():
    screen.fill((255, 255, 255))
    tray.update()
    drawGrid()
    player_manager.update()
    item_manager.update(player_manager.players)


def init():
    # Make players
    x, y = randSpawnPos()
    player_manager.addPlayer(x, y, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, "red")
    x, y = randSpawnPos()
    player_manager.addPlayer(x, y, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, "blue")

    running = True
    while running:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                player_manager.keyEvent(event)

        # Content Update
        tick()

        # Engine Update
        pygame.display.flip()
        clock.tick(speed)

    pygame.quit()


init()
