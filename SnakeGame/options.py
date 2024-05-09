import pygame
import pygame_gui
import json

class Options:
    def __init__(self, width, height, cell_size=20, exit_callback=None,):
        pygame.init()
        self.screen = pygame.display.set_mode((width * cell_size, height * cell_size))
        pygame.display.set_caption('Snake - Options')
        self.ui_manager = pygame_gui.UIManager((width * cell_size, height * cell_size))
        self.exit_callback = exit_callback
        self.difficulty_speeds = {'Easy': 10, 'Medium': 20, 'Hard': 30}

        try:
            with open('../SNAKEGAME/Data/settings.json', 'r') as f:
                settings = json.load(f)
                self.music_on = settings.get('music_on', True)
        except FileNotFoundError:
            self.music_on = True 
        
        button_width = 170
        button_height = 50

        self.music_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width * cell_size / 2 - button_width / 2, height * cell_size / 2 - 25), (button_width, button_height)),
            text='Music: On',
            manager=self.ui_manager)

        self.difficulty_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width * cell_size / 2 - button_width / 2, height * cell_size / 2 + 35), (button_width, button_height)),
            text='Difficulty: Easy',
            manager=self.ui_manager)

        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((width * cell_size / 2 - button_width / 2, height * cell_size / 2 + 95), (button_width, button_height)),
            text='Back to Menu',
            manager=self.ui_manager)

        self.running = True
        self.music_button.set_text(f'Music: {"On" if self.music_on else "Off"}')
        self.difficulty = 'Easy'

    def show(self):
        while self.running and pygame.get_init():
            time_delta = pygame.time.Clock().tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.music_button:
                        self.toggle_music()
                    elif event.ui_element == self.difficulty_button:
                        self.change_difficulty()
                    elif event.ui_element == self.back_button:
                        self.exit_to_menu()

                self.ui_manager.process_events(event)

            if self.running and pygame.get_init():
                self.ui_manager.update(time_delta)
                self.screen.fill((0, 0, 0))
                self.ui_manager.draw_ui(self.screen)
                pygame.display.flip()

        if pygame.get_init():
            pygame.quit()

    def change_difficulty(self):
        difficulties = ['Easy', 'Medium', 'Hard']
        current_index = difficulties.index(self.difficulty)
        new_index = (current_index + 1) % len(difficulties)
        self.difficulty = difficulties[new_index]
        self.difficulty_button.set_text(f'Difficulty: {self.difficulty}')
        # Guardar la dificultad seleccionada en un archivo
        with open('../SNAKEGAME/Data/settings.json', 'w') as f:
            json.dump({'difficulty': self.difficulty}, f)
    
    def toggle_music(self):
        self.music_on = not self.music_on
        self.music_button.set_text(f'Music: {"On" if self.music_on else "Off"}')

        try:
            with open('../SNAKEGAME/Data/settings.json', 'r') as f:
                settings = json.load(f)
        except FileNotFoundError:
            settings = {}
        settings['music_on'] = self.music_on
        with open('../SNAKEGAME/Data/settings.json', 'w') as f:
            json.dump(settings, f)

    def exit_to_menu(self):
        if self.exit_callback:
            self.exit_callback()