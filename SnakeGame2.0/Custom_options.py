import pygame
import pygame_gui
import json
from Snake1.options import Options
from ABC_options import ABC_options
music_on = False
class CustomOptions(Options,ABC_options):
    def __init__(self, width, height, cell_size=20, exit_callback=None):
        global music_on
        super().__init__(width, height, cell_size, exit_callback)
        self.difficulty_speeds['Competitive'] = 20
        try:
            with open('../SNAKEGAME/Data/settings.json', 'r') as f:
                settings = json.load(f)
                self.difficulty = settings.get('difficulty', 'Easy')
                self.music_on = settings.get('music_on', True)
        except FileNotFoundError:
            self.difficulty = 'Easy'
            self.music_on = True
        if self.music_on:
            self.difficulty_button.set_text("Music: On")
        else:
            self.difficulty_button.set_text("Music: Off")
        
        self.difficulty_button.set_text(self.difficulty)

    def show_ABC(self):
        while self.running and pygame.get_init():  # Verificar que Pygame esté inicializado
            time_delta = pygame.time.Clock().tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.music_button:
                        self.toggle_music_ABC()
                    elif event.ui_element == self.difficulty_button:
                        self.change_difficulty_ABC()
                    elif event.ui_element == self.back_button:
                        self.exit_to_menu()

                self.ui_manager.process_events(event)

            if self.running and pygame.get_init():  # Verificar de nuevo antes de actualizar y dibujar
                self.ui_manager.update(time_delta)
                self.screen.fill((0, 0, 0))
                self.ui_manager.draw_ui(self.screen)
                pygame.display.flip()

        if pygame.get_init():  # Asegurarse de que Pygame esté inicializado antes de cerrarlo
            pygame.quit() 

    def change_difficulty_ABC(self):  
        # Agregar una nueva dificultad a la lista
        new_difficulties = ['Easy', 'Medium', 'Hard', 'Competitive']
        current_index = new_difficulties.index(self.difficulty)
        new_index = (current_index + 1) % len(new_difficulties) 
        self.difficulty = new_difficulties[new_index]
        self.difficulty_button.set_text(self.difficulty)

        # Guardar la dificultad seleccionada en un archivo
        try:
            with open('../SNAKEGAME/Data/settings.json', 'r') as f:
                settings = json.load(f)
        except FileNotFoundError:
            settings = {}
        settings['difficulty'] = self.difficulty 
        with open('../SNAKEGAME/Data/settings.json', 'w') as f:
                json.dump(settings, f)  

    def toggle_music_ABC(self):
        global music_on
        self.music_on = not self.music_on
        self.music_button.set_text(f'Music: {"On" if self.music_on else "Off"}')
        # Lee el archivo de configuración actual, actualiza el estado de la música y guarda los cambios.
        try:
            with open('../SNAKEGAME/Data/settings.json', 'r') as f:
                settings = json.load(f)
        except FileNotFoundError:
            settings = {}
        settings['music_on'] = self.music_on
        with open('../SNAKEGAME/Data/settings.json', 'w') as f:
            json.dump(settings, f)