import os
import json
from pygame import mixer

STATE_FILE = "player_state.json"


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


def save_state(file_path, track, volume, playlist):
    state = {"track": track, "volume": volume, "playlist": playlist}
    with open(file_path, "w") as f:
        json.dump(state, f)
    print("State saved")


def load_state(file_path):
    if os.path.isfile(file_path):
        with open(file_path, "r") as f:
            state = json.load(f)
        print("State loaded")
        return state
    else:
        print("No saved state found")
        return None


def main():
    initialize_mixer()

    state = load_state(STATE_FILE)
    sound = None
    file_path = None
    playlist = []

    if state:
        file_path = state.get("track")
        volume = state.get("volume", 0.5)
        playlist = state.get("playlist", [])
        if file_path and os.path.isfile(file_path):
            sound = load_audio(file_path)
            if sound:
                set_volume(volume)
        else:
            file_path = input("Enter the path to the audio file: ")
            sound = load_audio(file_path)
            if sound:
                set_volume(volume)
                playlist.append(file_path)
    else:
        file_path = input("Enter the path to the audio file: ")
        sound = load_audio(file_path)
        if sound:
            volume = 0.5
            set_volume(volume)
            playlist.append(file_path)

    while True:
        command = (
            input(
                "Enter command (play, pause, resume, stop, load, playlist, volume, info, save, exit): "
            )
            .strip()
            .lower()
        )

        if command == "play":
            if sound:
                play_audio()
            else:
                print("No track loaded. Use the 'load' command to load an audio file.")
        elif command == "pause":
            pause_audio()
        elif command == "resume":
            resume_audio()
        elif command == "stop":
            stop_audio()
        elif command == "load":
            file_path = input("Enter the path to the audio file: ")
            sound = load_audio(file_path)
            if sound:
                set_volume(volume)
                playlist.append(file_path)
        elif command == "playlist":
            print("Current Playlist:")
            for i, track in enumerate(playlist, 1):
                print(f"{i}. {track}")
        elif command == "volume":
            try:
                volume = float(input("Enter volume (0.0 to 1.0): "))
                set_volume(volume)
            except ValueError:
                print("Invalid volume value")
        elif command == "info":
            if sound:
                display_track_info(sound)
            else:
                print("No track loaded")
        elif command == "save":
            save_state(STATE_FILE, file_path, get_volume(), playlist)
        elif command == "exit":
            stop_audio()
            save_state(STATE_FILE, file_path, get_volume(), playlist)
            break
        else:
            print("Invalid command")


if __name__ == "__main__":
    main()
