import tkinter as tk
import game
import json
import sound
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class SetNewKey:
    def __init__(self, link, event):
        self.link = link
        self.root = link.root
        self.event = event
        self.root.bind("<KeyPress>", self.get_key)
        self.spawn_wait_menu()

    def spawn_wait_menu(self):
        clear_window(self.link.frames)

        self.wait_bg = tk.Canvas(bg='gray', width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.wait_bg.place(x=0, y=0)

        self.wait_label = tk.Label(self.root)
        self.wait_label.configure(text='НАЖМИТЕ КЛАВИШУ', font=('Candara', 40, 'bold'), bg='gray', fg='white')
        self.wait_label.place(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT//2, anchor=tk.CENTER)

    def close_window(self, new_key):
        self.root.unbind('<KeyPress>')
        self.wait_bg.destroy()
        self.wait_label.destroy()
        self.link.spawn_settings_menu()

    def get_key(self, new_key):
        with open('settings.json', 'r') as file:
            data = json.load(file)
        data['control'][self.event] = new_key.keycode
        with open('settings.json', 'w') as file:
            json.dump(data, file)

        self.close_window(new_key.keysym)


class Button:
    def __init__(self, root, text, command=None):
        self.button = tk.Button(root)
        self.button.config(
            text=text,
            width=20,
            height=1,
            font=('Candara', 20),
            background='gray',
            foreground='white',
            borderwidth=0,
            highlightthickness=0,
            command=command)

    def pack(self):
        self.button.pack(pady=20)


class Menu:
    def __init__(self, root):
        self.root = root
        self.frames = []

        self.title_label = tk.Label(root)
        self.title_label.config(text='Bomberman', font=('Candara', 50, 'bold'))
        self.title_label.pack(pady=10)

        with open('keys.json') as file:
            self.keys = json.load(file)

    def spawn_main_menu(self):
        clear_window(self.frames)

        main_menu_frame = tk.Frame(self.root)
        self.frames.append(main_menu_frame)

        play_button = Button(main_menu_frame, 'Играть', self.spawn_level_menu)
        settings_button = Button(main_menu_frame, 'Настройки', self.spawn_settings_menu)
        rules_button = Button(main_menu_frame, 'Правила', self.spawn_rules_menu)
        quit_button = Button(main_menu_frame, 'Выход', self.quit_game)

        play_button.pack()
        settings_button.pack()
        rules_button.pack()
        quit_button.pack()
        main_menu_frame.pack()

    def spawn_level_menu(self):
        clear_window(self.frames)

        level_menu_frame = tk.Frame(self.root)
        self.frames.append(level_menu_frame)

        easy_level_button = Button(level_menu_frame, 'Easy уровень', lambda: self.start_game(1))
        normal_level_button = Button(level_menu_frame, 'Medium уровень', lambda: self.start_game(2))
        hard_level_button = Button(level_menu_frame, 'Hard уровень', lambda: self.start_game(3))
        back_menu_button = Button(level_menu_frame, 'Назад в меню', self.spawn_main_menu)

        easy_level_button.pack()
        normal_level_button.pack()
        hard_level_button.pack()
        back_menu_button.pack()
        level_menu_frame.pack()

    def spawn_settings_menu(self):

        def get_keyname(keycode: str):
            if keycode in self.keys:
                return self.keys[keycode]
            else:
                return chr(key)

        def change_volume():
            if self.volume == 'on':
                self.volume = 'off'
            else:
                self.volume = 'on'
            data['volume'] = self.volume
            with open('settings.json', 'w') as file:
                json.dump(data, file)
            volume_button.configure(text=self.volume)

        clear_window(self.frames)

        settings_menu_frame = tk.Frame(self.root)
        self.frames.append(settings_menu_frame)

        with open('settings.json') as file:
            data = json.load(file)

        self.volume = data['volume']

        volume_frame = tk.Frame(settings_menu_frame)
        volume_label = tk.Label(volume_frame, text='SOUND', font=('Candara', 20, 'bold'))
        volume_button = tk.Button(volume_frame,
                                  width=10,
                                  text=self.volume,
                                  font=('Candara', 20),
                                  bg='gray',
                                  fg='white',
                                  borderwidth=0,
                                  highlightthickness=0,
                                  command=change_volume)
        volume_label.grid(row=0, column=0, padx=20)
        volume_button.grid(row=0, column=1, padx=20)
        volume_frame.pack(pady=5, anchor=tk.E)

        for event in data['control']:
            key = data['control'][event]
            event_frame = tk.Frame(settings_menu_frame)
            event_label = tk.Label(event_frame, text=event, font=('Candara', 20, 'bold'))
            self.event_button = tk.Button(event_frame,
                                          width=10,
                                          text=get_keyname(str(key)),
                                          font=('Candara', 20),
                                          bg='gray',
                                          fg='white',
                                          borderwidth=0,
                                          highlightthickness=0,
                                          command=lambda x=event: SetNewKey(self, x))
            event_label.grid(row=0, column=0, padx=20)
            self.event_button.grid(row=0, column=1, padx=20)
            event_frame.pack(pady=5, anchor=tk.E)

        back_menu_button = Button(settings_menu_frame, 'Назад в меню', self.spawn_main_menu)
        back_menu_button.pack()
        settings_menu_frame.pack()

    def spawn_rules_menu(self):
        clear_window(self.frames)

        rules_menu_frame = tk.Frame(self.root)
        self.frames.append(rules_menu_frame)

        text = ''.join(open('rules.txt', encoding='utf-8').readlines())

        rules_label = tk.Label(rules_menu_frame)
        rules_label.config(text=text, font=('Candara', 20))

        back_menu_button = Button(rules_menu_frame, 'Назад в меню', self.spawn_main_menu)

        rules_label.pack(pady=50)
        back_menu_button.pack()
        rules_menu_frame.pack()

    def quit_game(self):
        self.root.quit()

    def start_game(self, difficulty):
        clear_window(self.frames)
        self.title_label.destroy()
        game.Game(self.root, difficulty)
        with open('settings.json', 'r') as file:
            data = json.load(file)
        if data['volume'] == 'on':
            sound.background_sound()


def clear_window(frames):
    for frame in frames:
        frame.destroy()
