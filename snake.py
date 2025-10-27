from collections import deque
from doublylinkedlist import DoublyLinkedList, Node
from random import randint
import pyxel

# Game constants
GAME_WIDTH = 30
GAME_HEIGHT = 50
GAME_TITLE = "Gumshoe's Snake Game OwO"
GAME_FPS = 20
GAME_HUD_HEIGHT = 7

# Color constants
COL_BLACK = 0
COL_DARK_BLUE = 1
COL_DARK_PURPLE = 2
COL_DARK_GREEN = 3
COL_BROWN = 4
COL_DARK_GRAY = 5
COL_LIGHT_GRAY = 6
COL_WHITE = 7
COL_RED = 8
COL_ORANGE = 9
COL_YELLOW = 10
COL_GREEN = 11
COL_BLUE = 12
COL_INDIGO = 13
COL_PINK = 14
COL_PEACH = 15


class Snake:
    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY
        self.coords = DoublyLinkedList()
        self.coords.insert_at_beginning({"x": posX, "y": posY})
        self.direction = "left"


class Apple:
    def __init__(self):
        self.draw_random_apple()

    def draw_random_apple(self):
        self.posX = randint(2, pyxel.width)
        self.posY = randint(GAME_HUD_HEIGHT + 1, pyxel.height - 2)


class Game:
    def __init__(self):
        pyxel.init(
            width=GAME_WIDTH,
            height=GAME_HEIGHT,
            title=GAME_TITLE,
            fps=GAME_FPS,
            capture_scale=6,
        )
        self.score = 0
        self.gameOver = False
        self.snake = Snake(10, 10)
        self.apple = Apple()
        pyxel.run(self.update, self.draw)

    def remove_tail(self):
        curr = self.snake.coords.head
        # If only one node, do not remove only node
        if not curr or not curr.next:
            return

        while curr.next:
            curr = curr.next

        if curr.prev:
            curr.prev.next = None

    def apple_collected(self):
        return (
            self.apple.posX == self.snake.coords.head.data["x"]
            and self.apple.posY == self.snake.coords.head.data["y"]
        )

    def set_snake_position(self):
        if not self.gameOver:
            head = self.snake.coords.head.data
            x, y = head["x"], head["y"]

            if self.snake.direction == "left":
                x -= 1
            elif self.snake.direction == "right":
                x += 1
            elif self.snake.direction == "up":
                y -= 1
            elif self.snake.direction == "down":
                y += 1

            # Insert new head
            self.snake.coords.insert_at_beginning({"x": x, "y": y})
            self.snake.posX = x
            self.snake.posY = y

            # Remove tail if no apple collected, standard movement
            if not self.apple_collected():
                self.remove_tail()
            else:
                self.score += 1
                self.apple.draw_random_apple()

    def get_player_input(self):
        if pyxel.btn(pyxel.KEY_A) and self.snake.direction != "right":
            self.snake.direction = "left"
        if pyxel.btn(pyxel.KEY_D) and self.snake.direction != "left":
            self.snake.direction = "right"
        if pyxel.btn(pyxel.KEY_W) and self.snake.direction != "down":
            self.snake.direction = "up"
        if pyxel.btn(pyxel.KEY_S) and self.snake.direction != "up":
            self.snake.direction = "down"

    def spawn_apple(self):
        pyxel.rect(self.apple.posX, self.apple.posY, 1, 1, 8)

    def spawn_snake(self):
        curr = self.snake.coords.head
        while curr:
            if not curr.prev:
                pyxel.rect(curr.data["x"], curr.data["y"], 1, 1, 3)
            else:
                pyxel.rect(curr.data["x"], curr.data["y"], 1, 1, 11)
            curr = curr.next

    def snake_hit_wall(self):
        head = self.snake.coords.head.data
        x, y = head["x"], head["y"]
        return x < 0 or x >= pyxel.width or y < GAME_HUD_HEIGHT + 1 or y >= pyxel.height

    def snake_hit_self(self):
        curr = self.snake.coords.head.next
        while curr:
            if (
                curr.data["x"] == self.snake.coords.head.data["x"]
                and curr.data["y"] == self.snake.coords.head.data["y"]
            ):
                self.gameOver = True
            else:
                curr = curr.next

    def check_game_over(self):
        if self.snake_hit_wall() or self.snake_hit_self():
            self.gameOver = True

    def update(self):
        if not self.gameOver:
            self.get_player_input()
            self.set_snake_position()
            self.check_game_over()
            # self.handle_game_over()

    def draw_score(self):
        pyxel.text(1, 1, f"{self.score}", 10)

    def draw_hud(self):
        pyxel.rect(0, 0, pyxel.width, GAME_HUD_HEIGHT, 1)

    def draw(self):
        pyxel.cls(0)
        self.draw_hud()
        self.draw_score()
        self.spawn_snake()
        self.spawn_apple()


Game()
