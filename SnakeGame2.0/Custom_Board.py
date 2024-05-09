from Snake1.snake import Snake
from Snake1.board import Board
from ABC_board import ABC_board
from Custom_Food import Custom_Food


class Custom_Board(Board, ABC_board):

    counter = 0

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.snake = Snake(initial_length=3, initial_position=(width // 2, height // 2))
        self.food = Custom_Food(self.width, self.height, self.snake)

    def update_ABC(self):
        global counter
        self.snake.move()
        if self.snake.body[0] == self.food.position:
            if self.food.color == (255, 0, 0):
                self.counter += 1
            elif self.food.color == (0, 255, 0):
                self.counter +=3
            elif self.food.color == (128, 0, 128):
                self.counter +=5
            self.snake.grow()
            self.food.color=self.food.change_color()
            self.food.position = self.food.spawn() # Actualiza la posición de la comida
    def is_game_over(self):
        return self.snake.check_collision(self.width, self.height)