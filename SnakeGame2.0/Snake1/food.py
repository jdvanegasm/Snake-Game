import random

class Food:
    def __init__(self, board_width, board_height, snake):
        self.board_width = board_width
        self.board_height = board_height
        self.snake = snake
        self.position = self.spawn()

    def spawn(self):
        min_distance = 4  # Establece la distancia mínima deseada entre la comida y la serpiente
        while True:
            x = random.randint(0, self.board_width - 1)
            y = random.randint(0, self.board_height - 1)
            food_position = (x, y)

            # Calcula la distancia entre la comida y la cabeza de la serpiente
            distance = abs(food_position[0] - self.snake.body[0][0]) + abs(food_position[1] - self.snake.body[0][1])

            # Verifica si la distancia es suficientemente grande
            if distance >= min_distance:
                return food_position