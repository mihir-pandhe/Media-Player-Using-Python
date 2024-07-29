import os
import tkinter as tk
from tkinter import filedialog
from pygame import mixer
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

class MediaPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Player")
        self.root.geometry("500x400")
        self.root.configure(bg="white")

        mixer.init()
        self.track = None
        self.is_paused = False

        self.create_widgets()

    def create_widgets(self):
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(expand=True)

        self.control_frame = tk.Frame(self.main_frame, bg="white")
        self.control_frame.pack(pady=20)

        self.play_button = tk.Button(
            self.control_frame,
            text="Play",
            command=self.play_audio,
            font=("Arial", 14),
            bg="lightgray",
            borderwidth=2,
            relief="raised",
            width=10,
            height=2,
        )
        self.play_button.grid(row=0, column=0, padx=10)

        self.pause_button = tk.Button(
            self.control_frame,
            text="Pause",
            command=self.pause_audio,
            font=("Arial", 14),
            bg="lightgray",
            borderwidth=2,
            relief="raised",
            width=10,
            height=2,
        )
        self.pause_button.grid(row=0, column=1, padx=10)

        self.stop_button = tk.Button(
            self.control_frame,
            text="Stop",
            command=self.stop_audio,
            font=("Arial", 14),
            bg="lightgray",
            borderwidth=2,
            relief="raised",
            width=10,
            height=2,
        )
        self.stop_button.grid(row=0, column=2, padx=10)

        self.volume_label = tk.Label(
            self.main_frame, text="Volume", bg="white", font=("Arial", 14)
        )
        self.volume_label.pack(pady=5)

        self.volume_slider = tk.Scale(
            self.main_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            command=self.set_volume,
            bg="white",
            fg="black",
            length=400,
        )
        self.volume_slider.set(50)
        self.volume_slider.pack(pady=10)

        self.track_label = tk.Label(
            self.main_frame, text="No track loaded", bg="white", font=("Arial", 14)
        )
        self.track_label.pack(pady=10)

        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Load", command=self.load_audio)
        self.file_menu.add_command(label="Exit", command=self.root.quit)

    def load_audio(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Audio Files", "*.mp3;*.wav")]
        )
        if file_path:
            self.track = file_path
            try:
                mixer.music.load(self.track)
                self.update_track_info(file_path)
                self.set_volume(self.volume_slider.get())
            except Exception as e:
                self.track_label.config(text=f"Error loading file: {e}")

    def update_track_info(self, file_path):
        try:
            audio = MP3(file_path, ID3=ID3)
            title = audio.get("TIT2", "Unknown Title")
            artist = audio.get("TPE1", "Unknown Artist")
            album = audio.get("TALB", "Unknown Album")
            info = f"{title} - {artist} ({album})"
        except:
            info = os.path.basename(file_path)
        self.track_label.config(text=info)

    def play_audio(self):
        if self.track:
            try:
                mixer.music.play()
                self.is_paused = False
            except Exception as e:
                self.track_label.config(text=f"Error during playback: {e}")

    def pause_audio(self):
        if self.track and not self.is_paused:
            try:
                mixer.music.pause()
                self.is_paused = True
            except Exception as e:
                self.track_label.config(text=f"Error pausing playback: {e}")
        elif self.is_paused:
            try:
                mixer.music.unpause()
                self.is_paused = False
            except Exception as e:
                self.track_label.config(text=f"Error resuming playback: {e}")

    def stop_audio(self):
        if self.track:
            try:
                mixer.music.stop()
            except Exception as e:
                self.track_label.config(text=f"Error stopping playback: {e}")

    def set_volume(self, val):
        try:
            volume = int(val) / 100
            mixer.music.set_volume(volume)
        except Exception as e:
            self.track_label.config(text=f"Error setting volume: {e}")


def main():
    root = tk.Tk()
    app = MediaPlayer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
