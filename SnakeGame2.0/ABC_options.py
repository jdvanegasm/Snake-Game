from abc import ABC, abstractmethod

class ABC_options(ABC):
    @abstractmethod
    def change_difficulty_ABC(self):
        pass

    def show_ABC(self):
        pass

    def toggle_music_ABC(self):
        pass