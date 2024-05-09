import random
from Snake1.food import Food
from ABC_food import ABC_food

class Custom_Food(Food, ABC_food):
    def __init__(self, board_width, board_height, snake):
        super().__init__(board_width, board_height, snake)
        self.color = self.change_color() 
        
    def change_color(self):
        self.color = random.choice([(255, 0, 0), (0, 255, 0), (128, 0, 128)])  # Rojo, verde, morado
        return self.color