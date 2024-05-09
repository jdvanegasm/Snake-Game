import pygame
import pygame_gui

class Pause:
    def __init__(self, screen, ui_manager, width, height, cell_size, game_instance):
        global screen_width,screen_height,My_cell_size
        self.screen = screen
        self.ui_manager = ui_manager
        self.is_visible = False
        self.game_instance = game_instance
        screen_width = width * cell_size
        screen_height = height * cell_size

        # Crear botones centrados
        self.resume_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((screen_width / 2 - 50, screen_height / 2 - 75), (100, 50)),
            text='Resume',
            manager=ui_manager)

        self.save_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((screen_width / 2 - 50, screen_height / 2 - 25), (100, 50)),
            text='Save Game',
            manager=ui_manager)

        self.quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((screen_width / 2 - 50, screen_height / 2 + 25), (100, 50)),
            text='Quit Game',
            manager=ui_manager)

        # Ocultar botones inicialmente
        self.hide()

    def show(self):
        self.is_visible = True
        self.resume_button.show()
        self.save_button.show()
        self.quit_button.show()

    def hide(self):
        self.is_visible = False
        self.resume_button.hide()
        self.save_button.hide()
        self.quit_button.hide()

    def handle_events(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.resume_button:
                self.resume_game()
            elif event.ui_element == self.save_button:
                self.game_instance.save_game()
                print("Game saved.")
            elif event.ui_element == self.quit_button:
                self.exit_to_menu()

    def resume_game(self):
        self.hide()
        self.game_instance.paused = False

    def exit_to_menu(self):
        self.game_instance.game_over = True
        self.hide()