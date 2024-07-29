import os
import time
from pygame import mixer


def initialize_mixer():
    mixer.init()


def load_audio(file_path):
    if os.path.isfile(file_path):
        mixer.music.load(file_path)
        print(f"Loaded {file_path}")
    else:
        print("File not found")


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


def main():
    initialize_mixer()
    file_path = input("Enter the path to the audio file: ")
    load_audio(file_path)

    while True:
        command = (
            input("Enter command (play, pause, resume, stop, exit): ").strip().lower()
        )

        if command == "play":
            play_audio()
        elif command == "pause":
            pause_audio()
        elif command == "resume":
            resume_audio()
        elif command == "stop":
            stop_audio()
        elif command == "exit":
            stop_audio()
            break
        else:
            print("Invalid command")


if __name__ == "__main__":
    main()
