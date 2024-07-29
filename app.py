import os
import time
from pygame import mixer


def initialize_mixer():
    mixer.init()


def load_audio(file_path):
    if os.path.isfile(file_path):
        mixer.music.load(file_path)
        sound = mixer.Sound(file_path)
        return sound
    else:
        print("File not found")
        return None


def play_audio():
    mixer.music.play()
    print("Playback started")


def pause_audio():
    mixer.music.pause()
    print("Playback paused")


def resume_audio():
    mixer.music.unpause()
    print("Playback resumed")


def stop_audio():
    mixer.music.stop()
    print("Playback stopped")


def set_volume(volume):
    if 0.0 <= volume <= 1.0:
        mixer.music.set_volume(volume)
        print(f"Volume set to {volume}")
    else:
        print("Volume must be between 0.0 and 1.0")


def get_volume():
    return mixer.music.get_volume()


def display_track_info(sound):
    if mixer.music.get_busy():
        position = mixer.music.get_pos() / 1000
        length = sound.get_length()
        print(f"Current Position: {position:.2f} s / Total Length: {length:.2f} s")
    else:
        print("No track is playing")


def main():
    initialize_mixer()
    file_path = input("Enter the path to the audio file: ")

    sound = load_audio(file_path)
    if not sound:
        return

    while True:
        command = (
            input("Enter command (play, pause, resume, stop, volume, info, exit): ")
            .strip()
            .lower()
        )

        if command == "play":
            play_audio()
        elif command == "pause":
            pause_audio()
        elif command == "resume":
            resume_audio()
        elif command == "stop":
            stop_audio()
        elif command == "volume":
            try:
                volume = float(input("Enter volume (0.0 to 1.0): "))
                set_volume(volume)
            except ValueError:
                print("Invalid volume value")
        elif command == "info":
            display_track_info(sound)
        elif command == "exit":
            stop_audio()
            break
        else:
            print("Invalid command")


if __name__ == "__main__":
    main()
