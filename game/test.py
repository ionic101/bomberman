import simpleaudio as sa

wave_obj = sa.WaveObject.from_wave_file("sounds/music.wav")

play_obj = wave_obj.play()

play_obj.stop()