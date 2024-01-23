from threading import Thread
import simpleaudio as sa


def play_sound_once(path):
    sa.WaveObject.from_wave_file(path).play()


def play_sound_for_loop(path):
    sound = sa.WaveObject.from_wave_file(path).play()
    sound.wait_done()
    if play_status:
        play_sound_for_loop(path)


def play_sound(path, repeat=False):
    if repeat:
        sound = Thread(target=play_sound_for_loop, args=[path])
    else:
        sound = Thread(target=play_sound_once, args=[path])
    sound.start()


def stop_sound():
    global play_status

    play_status = False
    sa.stop_all()


def death_sound():
    play_sound('sounds\death.wav')


def explosion_sound():
    play_sound("sounds\explosion.wav")


def background_sound():
    play_sound('sounds\music.wav', repeat=True)


play_status = True
