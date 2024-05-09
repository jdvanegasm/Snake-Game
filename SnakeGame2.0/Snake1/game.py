import pygame
import pygame_gui
import json
import os
from .board import Board
from .food import Food
from .pause import Pause

class Game:
    def __init__(self, width, height, cell_size=20):
        pygame.init()
        self.board = Board(width, height)
        self.cell_size = cell_size
        self.screen = pygame.display.set_mode((width * cell_size, height * cell_size))
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.paused = False

        # Leer la dificultad del archivo y configurar la velocidad
        try:
            with open('../SNAKEGAME/Data/settings.json', 'r') as f:
                settings = json.load(f)
                difficulty = settings.get('difficulty', 'Easy')
        except FileNotFoundError:
            difficulty = 'Easy'

        self.difficulty_speeds = {'Easy': 10, 'Medium': 30, 'Hard': 50}
        self.speed = self.difficulty_speeds[difficulty]

        self.ui_manager = pygame_gui.UIManager((width * cell_size, height * cell_size))
        self.pause_screen = Pause(self.screen, self.ui_manager, width, height, cell_size, self)

    def save_game(self):
        game_state = {
            'snake_body': self.board.snake.body,
            'snake_direction': self.board.snake.direction,
            'food_position': self.board.food.position,
            'score': self.board.counter
        }
        with open("../SNAKEGAME/Data/saved_game.json", 'w') as save_file:
            json.dump(game_state, save_file)

        pygame.display.set_caption('Snake')
    
    def load_game_state(self, game_state):
        self.board.snake.body = game_state['snake_body']
        self.board.snake.direction = game_state['snake_direction']
        self.board.food = Food(self.board.width, self.board.height, self.board.snake)  # Crear una nueva instancia de Food
        self.board.counter = game_state['score']

    def run(self):
        while not self.game_over:
            time_delta = self.clock.tick(self.speed) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                        if self.paused:
                            self.pause_screen.show()
                        else:
                            self.pause_screen.hide()

                    if not self.paused:
                        if event.key == pygame.K_UP:
                            self.board.snake.change_direction('UP')
                        elif event.key == pygame.K_DOWN:
                            self.board.snake.change_direction('DOWN')
                        elif event.key == pygame.K_LEFT:
                            self.board.snake.change_direction('LEFT')
                        elif event.key == pygame.K_RIGHT:
                            self.board.snake.change_direction('RIGHT')

                if self.paused:
                    self.pause_screen.handle_events(event)

                self.ui_manager.process_events(event)

            if not self.paused:
                game_lose_boolean = False
                self.update()
                self.draw()
                if self.board.is_game_over():
                    self.game_over = True
                    print("Game Over!")
                    pygame.time.wait(1000)
                    game_lose_boolean = True
            
            self.ui_manager.update(time_delta)
            self.ui_manager.draw_ui(self.screen)
            pygame.display.update()

        if(game_lose_boolean == True):
            if os.path.exists('../SNAKEGAME/Data/saved_game.json'):
                with open('../SNAKEGAME/Data/saved_game.json', 'w') as save_file:
                    save_file.write('')  # Vacía el contenido del archivo        

    def update(self):
        self.board.update()

    def draw(self):
        self.screen.fill((0, 0, 0))
        for y in range(self.board.height):
            for x in range(self.board.width):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                if (x, y) == self.board.snake.body[0]:
                    pygame.draw.rect(self.screen, (0, 255, 0), rect)
                elif (x, y) in self.board.snake.body:
                    pygame.draw.rect(self.screen, (0, 200, 0), rect)
                elif (x, y) == self.board.food.position:
                    pygame.draw.rect(self.screen, (255, 0, 0), rect)

        text_counter = self.board.counter
        font = pygame.font.Font(None, 36)
        text = font.render(str(text_counter), True, (255, 255, 255))
        self.screen.blit(text, (10, 10))
        pygame.display.update()