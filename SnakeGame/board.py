from snake import Snake
from food import Food

class Board:

    counter = 0

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.snake = Snake(initial_length=3, initial_position=(width // 2, height // 2))
        self.food = Food(board_width=width, board_height=height, snake=self.snake)

    def update(self):
        self.snake.move()
        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.counter += 1
            self.food.position = self.food.spawn()

    def is_game_over(self):
        return self.snake.check_collision(self.width, self.height)