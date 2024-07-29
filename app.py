import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from pygame import mixer
from mutagen.mp3 import MP3


class MediaPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Player")
        self.root.geometry("800x400")

        mixer.init()
        self.playlist = []
        self.current_track_index = -1
        self.is_paused = False

        self.create_widgets()

    def create_widgets(self):
        playlist_frame = tk.Frame(self.root)
        playlist_frame.pack(pady=20)

        self.playlist_box = tk.Listbox(
            playlist_frame,
            selectmode=tk.SINGLE,
            width=60,
            height=10,
            font=("Helvetica", 12),
        )
        self.playlist_box.pack(side=tk.LEFT, padx=10)

        playlist_scrollbar = tk.Scrollbar(playlist_frame)
        playlist_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.playlist_box.config(yscrollcommand=playlist_scrollbar.set)
        playlist_scrollbar.config(command=self.playlist_box.yview)

        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=20)

        self.play_button = tk.Button(
            control_frame,
            text="Play",
            command=self.play_audio,
            width=10,
            font=("Helvetica", 12),
        )
        self.play_button.grid(row=0, column=0, padx=10)

        self.pause_button = tk.Button(
            control_frame,
            text="Pause",
            command=self.pause_audio,
            width=10,
            font=("Helvetica", 12),
        )
        self.pause_button.grid(row=0, column=1, padx=10)

        self.stop_button = tk.Button(
            control_frame,
            text="Stop",
            command=self.stop_audio,
            width=10,
            font=("Helvetica", 12),
        )
        self.stop_button.grid(row=0, column=2, padx=10)

        self.add_button = tk.Button(
            control_frame,
            text="Add Track",
            command=self.add_track,
            width=10,
            font=("Helvetica", 12),
        )
        self.add_button.grid(row=1, column=0, padx=10, pady=10)

        self.remove_button = tk.Button(
            control_frame,
            text="Remove Track",
            command=self.remove_track,
            width=10,
            font=("Helvetica", 12),
        )
        self.remove_button.grid(row=1, column=1, padx=10, pady=10)

        volume_frame = tk.Frame(self.root)
        volume_frame.pack(pady=20)

        self.volume_label = tk.Label(
            volume_frame, text="Volume", font=("Helvetica", 12)
        )
        self.volume_label.pack(side=tk.LEFT)

        self.volume_slider = tk.Scale(
            volume_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            command=self.set_volume,
            length=200,
        )
        self.volume_slider.set(50)
        self.volume_slider.pack(side=tk.LEFT, padx=10)

        self.seek_bar = ttk.Scale(
            self.root,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            command=self.seek,
            length=500,
        )
        self.seek_bar.pack(pady=20)

        self.track_label = tk.Label(
            self.root, text="No track loaded", font=("Helvetica", 12)
        )
        self.track_label.pack(pady=20)

        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Load", command=self.load_audio)
        self.file_menu.add_command(label="Exit", command=self.root.quit)

    def add_track(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Audio Files", "*.mp3;*.wav")]
        )
        if file_path:
            self.playlist.append(file_path)
            self.playlist_box.insert(tk.END, os.path.basename(file_path))

    def remove_track(self):
        selected_index = self.playlist_box.curselection()
        if selected_index:
            self.playlist_box.delete(selected_index)
            self.playlist.pop(selected_index[0])

    def load_audio(self):
        selected_index = self.playlist_box.curselection()
        if selected_index:
            self.current_track_index = selected_index[0]
            track = self.playlist[self.current_track_index]
            mixer.music.load(track)
            self.track_label.config(text=os.path.basename(track))
            audio = MP3(track)
            self.seek_bar.config(to=int(audio.info.length))
            self.display_metadata(track)

    def display_metadata(self, file_path):
        audio = MP3(file_path)
        metadata = f"Title: {audio.get('TIT2', 'Unknown')}\nArtist: {audio.get('TPE1', 'Unknown')}\nAlbum: {audio.get('TALB', 'Unknown')}"
        messagebox.showinfo("Track Info", metadata)

    def play_audio(self):
        if self.current_track_index == -1:
            self.load_audio()
        if self.current_track_index != -1:
            mixer.music.play()
            self.is_paused = False
            self.update_seek_bar()
            messagebox.showinfo("Playback", "Playback started")
        else:
            messagebox.showwarning("No Track", "No track loaded")

    def pause_audio(self):
        if self.current_track_index != -1:
            if not self.is_paused:
                mixer.music.pause()
                self.is_paused = True
                messagebox.showinfo("Playback", "Playback paused")
            else:
                mixer.music.unpause()
                self.is_paused = False
                messagebox.showinfo("Playback", "Playback resumed")
        else:
            messagebox.showwarning("No Track", "No track loaded")

    def stop_audio(self):
        if self.current_track_index != -1:
            mixer.music.stop()
            messagebox.showinfo("Playback", "Playback stopped")
        else:
            messagebox.showwarning("No Track", "No track loaded")

    def set_volume(self, val):
        volume = int(val) / 100
        mixer.music.set_volume(volume)

    def seek(self, val):
        if self.current_track_index != -1:
            mixer.music.play(start=int(val))
            messagebox.showinfo("Seek", f"Seeked to {val} seconds")

    def update_seek_bar(self):
        if mixer.music.get_busy():
            current_pos = mixer.music.get_pos() / 1000
            self.seek_bar.set(current_pos)
            self.root.after(1000, self.update_seek_bar)


def main():
    root = tk.Tk()
    app = MediaPlayer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
