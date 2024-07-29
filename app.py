import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pygame import mixer

class MediaPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Player")
        self.root.geometry("800x400")

        mixer.init()
        self.track = None
        self.is_paused = False

        self.create_widgets()

    def create_widgets(self):
        self.play_button = tk.Button(self.root, text="Play", command=self.play_audio)
        self.play_button.pack(pady=10)

        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_audio)
        self.pause_button.pack(pady=10)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_audio)
        self.stop_button.pack(pady=10)

        self.volume_label = tk.Label(self.root, text="Volume")
        self.volume_label.pack()

        self.volume_slider = tk.Scale(
            self.root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_volume
        )
        self.volume_slider.set(50)
        self.volume_slider.pack(pady=10)

        self.track_label = tk.Label(self.root, text="No track loaded")
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
            mixer.music.load(self.track)
            self.track_label.config(text=os.path.basename(self.track))
            messagebox.showinfo("Loaded", f"Loaded {os.path.basename(self.track)}")

    def play_audio(self):
        if self.track:
            mixer.music.play()
            self.is_paused = False
            messagebox.showinfo("Playback", "Playback started")
        else:
            messagebox.showwarning("No Track", "No track loaded")

    def pause_audio(self):
        if self.track and not self.is_paused:
            mixer.music.pause()
            self.is_paused = True
            messagebox.showinfo("Playback", "Playback paused")
        elif self.is_paused:
            mixer.music.unpause()
            self.is_paused = False
            messagebox.showinfo("Playback", "Playback resumed")
        else:
            messagebox.showwarning("No Track", "No track loaded")

    def stop_audio(self):
        if self.track:
            mixer.music.stop()
            messagebox.showinfo("Playback", "Playback stopped")
        else:
            messagebox.showwarning("No Track", "No track loaded")

    def set_volume(self, val):
        volume = int(val) / 100
        mixer.music.set_volume(volume)


def main():
    root = tk.Tk()
    app = MediaPlayer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
