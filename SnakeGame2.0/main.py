import tkinter as tk
from tkinter import ttk


from menu import Menu, play_music, Menu_set_user

def main():
    # Captura el dato del usuario en una ventana separada
    usuario = capturar_dato()

    width, height = 60, 30
    cell_size = 20
    Menu_set_user(usuario)
    main_menu = Menu(width, height, cell_size)
    music_on = ("music_on", True)
    play_music(music_on)

    # Muestra el menú principal y comienza el juego
    main_menu.show()

def capturar_dato():
    # Crea una ventana temporal para capturar el nombre de usuario
    temp_root = tk.Tk()
    temp_root.title("Captura de dato")
    temp_root.geometry("300x130")

    tk.Label(temp_root, text="Ingrese un nombre de usuario:").pack(pady=10)
    entry = tk.Entry(temp_root)
    entry.pack(pady=5)

    # Variable para almacenar el nombre de usuario
    usuario = None

    def on_submit():
        nonlocal usuario  # Indica que se va a modificar la variable "usuario" definida fuera de la función
        if entry.get().strip():  # Verifica si se ingresó un nombre de usuario
            usuario = entry.get().strip()
            temp_root.quit()  # Sale del bucle principal de eventos

    submit_button = ttk.Button(temp_root, text="OK", command=on_submit)
    submit_button.pack(pady=10)

    temp_root.mainloop()  # Espera hasta que la ventana se cierre
    temp_root.destroy()  # Destruye la ventana explícitamente
    return usuario


if __name__ == '__main__':
    main()
