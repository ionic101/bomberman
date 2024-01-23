import tkinter as tk
import json


def save_and_quit():
    with open('new_keys.json', 'w') as file:
        json.dump(keys, file)

    print(keys)
    root.destroy()


def bind(keycode, keyname):
    global keys

    keys[keycode] = keyname

    key_label.destroy()
    key_entry.destroy()
    key_button.destroy()
    wait_key()


def get_key(event):
    global key_label
    global key_entry
    global key_button

    root.unbind('<KeyPress>')
    wait_label.destroy()
    quit_button.destroy()
    code = event.keycode

    key_label = tk.Label(root, text=f'Keycode: {code}', font=('Roboto', 40))
    key_entry = tk.Entry(root, width=20, font=('Roboto', 30))
    key_button = tk.Button(root, text='bind', font=('Roboto', 20), command=lambda: bind(code, key_entry.get()))
    key_label.pack(pady=50)
    key_entry.pack(pady=30)
    key_button.pack()


def wait_key():
    global wait_label
    global quit_button

    root.bind('<KeyPress>', get_key)
    wait_label = tk.Label(root, text='Press Key', font=('Roboto', 70))
    quit_button = tk.Button(root, text='quit', width=10, font=('Roboto', 30), command=save_and_quit)

    wait_label.pack(pady=50)
    quit_button.pack(pady=50)


root = tk.Tk()
root.title('Get Key')
root.geometry(f'{800}x{800}')
root.resizable(False, False)

keys: dict = {}

wait_key()
root.mainloop()
