import tkinter as tk
from settings import *
import menu

root = tk.Tk()
root.title('Bomberman')
root.geometry(f'{SCREEN_WIDTH}x{SCREEN_HEIGHT}')
root.resizable(False, False)

menu = menu.Menu(root)
menu.spawn_main_menu()

root.mainloop()
