import pygame
import pygame_gui
import json
import os
from game import Game
from options import Options

def play_music(music_on):
    pygame.mixer.init()
    if music_on:
        pygame.mixer.music.load('../SNAKEGAME/Data/Flying Beagle - Snake Game.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
    else:
        pygame.mixer.music.stop()

class Menu:
    def __init__(self, width, height, cell_size=20):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((width * cell_size, height * cell_size))
        pygame.display.set_caption('Snake')
        self.ui_manager = pygame_gui.UIManager((width * cell_size, height * cell_size))

        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width * cell_size / 2 - 50, height * cell_size / 2 - 25), (100, 50)),
            text='Start',
            manager=self.ui_manager)

        self.options_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width * cell_size / 2 - 50, height * cell_size / 2 + 35), (100, 50)),
            text='Options',
            manager=self.ui_manager)

        self.scores_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width * cell_size / 2 - 50, height * cell_size / 2 + 95), (100, 50)),
            text='Scores',
            manager=self.ui_manager)
        
        self.resume_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width * cell_size / 2 - 50, height * cell_size / 2 - 85), (100, 50)),
            text='Resume',
            manager=self.ui_manager,
            visible=False)
        
        self.quit_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width * cell_size / 2 - 50, height * cell_size / 2 + 155), (100,50)),
            text = "Quit Game",
            manager = self.ui_manager,
            visible=True)
        
        self.running = True
    
    def load_game(self):
        try:
            with open('../SNAKEGAME/Data/saved_game.json', 'r') as save_file:
                save_data = save_file.read().strip()
                if save_data:
                    game_state = json.loads(save_data)
                    game_instance = Game(60, 30)
                    game_instance.load_game_state(game_state)
                    game_instance.run()
                else:
                    self.show_error_popup("No saved game found.")
        except FileNotFoundError:
            self.show_error_popup("No saved game found.")

    def show_error_popup(self, message):
        error_dialog = pygame_gui.windows.UIMessageWindow(
            rect=pygame.Rect(200, 200, 400, 200),
            manager=self.ui_manager,
            window_title='Error',
            html_message=message)
        error_dialog.set_blocking(True)

    def show(self):
        try:
            with open('../SNAKEGAME/Data/settings.json', 'r') as f:
                settings = json.load(f)
                music_on = settings.get('music_on', True)
        except FileNotFoundError:
            music_on = True
        play_music(music_on)

        saved_game_path = '../SNAKEGAME/Data/saved_game.json'
        if os.path.exists(saved_game_path) and os.path.getsize(saved_game_path) > 0:
            self.resume_game_button.visible = True
        else:
            self.resume_game_button.visible = False

        while self.running:
            time_delta = pygame.time.Clock().tick(10) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.start_button:
                        self.start_game()
                    elif event.ui_element == self.options_button:
                        self.show_options()
                    elif event.ui_element == self.scores_button:
                        # Mostrar puntajes más altos...
                        pass
                    elif event.ui_element == self.resume_game_button:
                        self.load_game()
                    elif event.ui_element == self.quit_game_button:
                        self.exit_game()

                self.ui_manager.process_events(event)

            if self.running:
                self.ui_manager.update(time_delta)
                self.screen.fill((0, 0, 0))
                self.ui_manager.draw_ui(self.screen)
                pygame.display.flip()

        pygame.quit()

    def start_game(self):
        game_instance = Game(60, 30)
        game_instance.run()
        self.running = False

    def show_options(self):
        options_instance = Options(60, 30, exit_callback=self.show)
        options_instance.show()    
        self.running = False

    def exit_game(self):
        self.running = False