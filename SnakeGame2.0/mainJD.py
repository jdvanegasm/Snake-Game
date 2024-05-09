from Snake1.menu import Menu
from Snake1.menu import play_music

def main():
    # Establece las dimensiones del juego
    width, height = 60, 30
    cell_size = 20

    # Crea una instancia del menú principal
    main_menu = Menu(width, height, cell_size)
    music_on = ("music_on", True)
    play_music(music_on)

    # Muestra el menú principal y comienza el juego
    main_menu.show()


if __name__ == '__main__':
    main()