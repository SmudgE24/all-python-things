import pygame
import os

MUSIC_FOLDER = "assets/music"

pygame.mixer.init()


def play_music(filename, loops=-1, fade_ms=500):
    """Stop current music and play a new track."""

    path = os.path.join(MUSIC_FOLDER, filename)

    if not os.path.exists(path):
        print(f"Music not found: {path}")
        return

    # Stop whatever is currently playing
    pygame.mixer.music.stop()

    # Load the new track
    pygame.mixer.music.load(path)

    # Play it
    pygame.mixer.music.play(loops, fade_ms=fade_ms)


def stop_music(fade_ms=500):
    """Stop the current music."""

    pygame.mixer.music.fadeout(fade_ms)


def pause_music():
    pygame.mixer.music.pause()


def resume_music():
    pygame.mixer.music.unpause()


def set_music_volume(volume):
    """Volume from 0.0 to 1.0."""

    pygame.mixer.music.set_volume(volume)