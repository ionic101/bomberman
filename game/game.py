import tkinter as tk
from settings import *
from enemy import Enemy
from bomberman import Bomberman
from bomb import Bomb
import generator
import sound
import json


class Game:
    def __init__(self, root, difficulty):
        self.root = root
        self.game = True

        self.canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg='white')
        self.canvas.pack()

        self.walls = generator.generate_walls()
        self.boxes = generator.generate_boxes()
        self.blocks = self.walls + self.boxes
        self.enemys = [Enemy(1, 13), Enemy(23, 1), Enemy(23, 13)][:difficulty]
        self.player = Bomberman(1, 1)
        self.bombs = []
        self.explosions = []

        self.BOX_IMAGE = tk.PhotoImage(file="textures/box.png")
        self.WALL_IMAGE = tk.PhotoImage(file="textures/wall.png")
        self.BACKGROUND_IMAGE = tk.PhotoImage(file="textures/background.png")
        self.EXPLOSION_IMAGE = tk.PhotoImage(file="textures/explosion.png")
        self.ENEMY_IMAGE = tk.PhotoImage(file="textures/enemy.png")
        self.PLAYER_IMAGE = tk.PhotoImage(file="textures/player.png")
        self.BOMB_IMAGE = tk.PhotoImage(file="textures/bomb.png")

        self.get_settings()
        self.root.bind("<KeyPress>", self.get_key)
        self.update_game()

    def get_settings(self):
        control = {}
        with open('settings.json', 'r') as file:
            data = json.load(file)
        for event in data['control']:
            control[event] = data['control'][event]
        self.control = control

    def update_game(self):
        if self.game:
            for enemy in self.enemys:
                status = enemy.move(self.blocks, self.explosions, (self.player.x, self.player.y))
                if status:
                    sound.death_sound()
                    self.end_game(False)

            self.update_screen()
            self.root.after(700, self.update_game)

    def draw_with_color(self, x, y, color):
        x_start, y_start = x * SCALE, y * SCALE
        x_end, y_end = x_start + SCALE, y_start + SCALE
        self.canvas.create_rectangle(x_start, y_start, x_end, y_end, fill=color)

    def draw_with_texture(self, x, y, image):
        x_start, y_start = x * SCALE, y * SCALE
        self.canvas.create_image(x_start, y_start, anchor=tk.NW, image=image)

    def update_screen(self):
        if self.game:
            self.canvas.delete('all')

            self.canvas.create_image(0, 0, image=self.BACKGROUND_IMAGE, anchor=tk.NW)

            for wall in self.walls:
                self.draw_with_texture(*wall, self.WALL_IMAGE)

            for box in self.boxes:
                self.draw_with_texture(*box, self.BOX_IMAGE)

            for enemy in self.enemys:
                self.draw_with_texture(enemy.x, enemy.y, self.ENEMY_IMAGE)

            for bomb in self.bombs:
                self.draw_with_texture(bomb.x, bomb.y, self.BOMB_IMAGE)

            for explosion in self.explosions:
                for cord in explosion:
                    self.draw_with_texture(*cord, self.EXPLOSION_IMAGE)

            self.draw_with_texture(self.player.x, self.player.y, self.PLAYER_IMAGE)

    def kill(self, enemy):
        self.enemys.remove(enemy)
        sound.death_sound()

    def death_check(self, explosion):
        for cord in explosion:
            if cord in self.boxes:
                self.boxes.remove(cord)
                self.blocks.remove(cord)

        for enemy in self.enemys:
            if (enemy.x, enemy.y) in explosion:
                self.kill(enemy)
                if len(self.enemys) == 0:
                    self.end_game(True)

        if (self.player.x, self.player.y) in explosion:
            self.end_game(False)

    def death_player_check(self):
        player_cords = (self.player.x, self.player.y)

        for explosion in self.explosions:
            if (player_cords in explosion):
                sound.death_sound()
                self.end_game(False)

        for enemy in self.enemys:
            if player_cords == (enemy.x, enemy.y):
                sound.death_sound()
                self.end_game(False)

    def remove_explosion(self, explosion):
        self.explosions.remove(explosion)

    def explode_bomb(self, bomb):
        explosion = bomb.explode(self.walls)
        self.explosions.append(explosion)
        self.bombs.remove(bomb)
        self.player.count_bombs -= 1
        self.root.after(EXPLODE_TIME, self.remove_explosion, explosion)
        self.death_check(explosion)
        sound.explosion_sound()
        self.update_screen()

    def spawn_bomb(self, x, y):
        b = Bomb(x, y)
        self.bombs.append(b)
        self.root.after(BOMB_DELAY, self.explode_bomb, b)

    def get_key(self, event):
        key = event.keycode
        if key == self.control['forward']:
            self.player.move(0, -1, self.blocks)
        elif key == self.control['backward']:
            self.player.move(0, 1, self.blocks)
        elif key == self.control['left']:
            self.player.move(-1, 0, self.blocks)
        elif key == self.control['right']:
            self.player.move(1, 0, self.blocks)
        elif key == self.control['bomb']:
            if self.player.count_bombs < self.player.max_bombs:
                self.player.count_bombs += 1
                self.spawn_bomb(self.player.x, self.player.y)
        elif key == QUIT_KEY:
            self.quit_game()
        self.death_player_check()
        self.update_screen()

    def end_game(self, status):
        if status:
            text = 'ВЫ ВЫИГРАЛИ'
        else:
            text = 'ВЫ ПРОИГРАЛИ'
        self.game = False
        self.root.unbind("<KeyPress>")
        self.canvas.destroy()
        title_label = tk.Label(self.root)
        title_label.config(text=text, font=('Candara', 50, 'bold'))
        title_label.pack(pady=200)
        self.root.after(3000, self.quit_game)

    def quit_game(self):
        self.game = False
        sound.stop_sound()
        self.root.destroy()
