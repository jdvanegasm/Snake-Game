import pygame
import pygame_gui
import json
import os
from Custom_Game import Competitive, set_user
from Snake1.game import Game
from Custom_options import CustomOptions

difficulty=''
user=""
def play_music(music_on):
    pygame.mixer.init()
    if music_on:
        pygame.mixer.music.load('../SNAKEGAME2.0/DATA/FLYING BEAGLE - SNAKE GAME.WAV')
        pygame.mixer.music.play(-1)  # Reproduce la música en bucle si está activada.
        pygame.mixer.music.set_volume(0.5)
    else:
        pygame.mixer.music.stop()  # Detiene la música si está desactivada.
def Menu_set_user(actual_user):
        global user
        user= actual_user
class Menu:
    def __init__(self, width, height, cell_size=20):
        pygame.init()
        pygame.mixer.init()  # Inicializar el mixer aquí
        self.screen = pygame.display.set_mode((width * cell_size, height * cell_size))
        pygame.display.set_caption('Snake')
        self.ui_manager = pygame_gui.UIManager((width * cell_size, height * cell_size))

        # Crear botones
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
        global difficulty, user
        try:
            with open('../SNAKEGAME/Data/saved_game.json', 'r') as save_file:
                save_data = save_file.read().strip()
                if save_data:  # Verifica si el archivo no está vacío
                    try:
                        with open('../SNAKEGAME/Data/settings.json', 'r') as f:
                            settings = json.load(f)
                            difficulty = settings.get('difficulty', 'Easy')
                    except FileNotFoundError:
                        difficulty = 'Easy'
                    game_state = json.loads(save_data)
                    #STRATEGY PARA CADA MODO DE JUEGO
                    if difficulty == 'Easy' or 'Medium' or 'Hard':
                        game_instance = Game(60, 30)
                    elif difficulty == 'Competitive':
                        set_user(user)
                        game_instance = Competitive(60, 30)
                    else:
                        print("It doesn't work")
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
        global difficulty
        try:
            with open('../SNAKEGAME/Data/settings.json', 'r') as f:
                settings = json.load(f)
                difficulty = settings.get('difficulty', 'Easy')
                music_on = settings.get('music_on', True)
        except FileNotFoundError:
            difficulty = 'Easy'
            music_on = True
        play_music(music_on)
        # Verificar si existe un juego guardado
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
                        self.exit_game()  # Agregar esta línea

                self.ui_manager.process_events(event)

            if self.running:  # Verifica si el bucle debe continuar antes de actualizar la UI
                self.ui_manager.update(time_delta)
                self.screen.fill((0, 0, 0))
                self.ui_manager.draw_ui(self.screen)
                pygame.display.flip()

        pygame.quit()

    def start_game(self):
        global difficulty,user
        #STRATEGY PARA CADA MODO DE JUEGO
        if difficulty == 'Easy' or difficulty =='Medium' or difficulty =='Hard':
            game_instance = Game(60, 30)
        elif difficulty == 'Competitive':
            set_user(user)
            game_instance = Competitive(60, 30)
        else:
            print("It doesn't work")

        game_instance.run()
        self.running = False

    def show_options(self):
        options_instance = CustomOptions(60, 30, exit_callback=self.show)
        options_instance.show_ABC()    
        self.running = False

    def exit_game(self):
        self.running = False