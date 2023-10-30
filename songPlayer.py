import os
import pygame
import signal
import sys
import atexit
import random
import tkinter as tk
from tkinter import filedialog
import time

def find_music_files(folder_path=None, query=None):
    print("\n\n\n\n\n\n\n\n\n\n\n\n")
    print("Select your music folder.")
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    if not folder_path:
        return []
    music_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith((".mp3", ".wav", ".ogg")):
                if query is None or query.lower() in file.lower():
                    music_files.append(os.path.join(root, file))
    return music_files

def set_volume(vol):
    global volume
    volume = float(vol)
    pygame.mixer.music.set_volume(volume)


def shuffle_playlist():
    global shuffle
    shuffle = not shuffle
    if shuffle:
        random.shuffle(songs)
    print(f"Shuffle {'on' if shuffle else 'off'}")

def pause_play():
    global paused
    if not paused:
        pygame.mixer.music.pause()
        paused = True
        print("Paused")
    else:
        pygame.mixer.music.unpause()
        paused = False
        print("Unpaused")

def play_next_song():
    global current_song_index
    if current_song_index < len(songs) - 1:
        current_song_index += 1
        play_song()

def play_prev_song():
    global current_song_index
    if current_song_index > 0:
        current_song_index -= 1
        play_song()

def play_song():
    global paused
    if not paused:
        pygame.mixer.music.load(songs[current_song_index])
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    pygame.mixer.music.play()
    print(f"\nNow playing: {os.path.basename(songs[current_song_index])}\n")

def stop_music(): 
    pygame.mixer.music.stop()
    print("Stopped")
    exit_app()

def exit_app():
    pygame.mixer.quit()
    root.destroy()
    sys.exit()

pygame.mixer.init()
os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'
set_volume(0)
paused = False
shuffle = False
current_song_index = 0

songs = find_music_files()

if not songs:
    print("No music files found in the selected folder.")
    sys.exit()

root = tk.Tk()
root.title("Music Player")

# Create and configure the GUI elements
frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

play_button = tk.Button(frame, text="Play", command=play_song)
pause_play_button = tk.Button(frame, text="Pause/Unpause", command=pause_play)
next_button = tk.Button(frame, text="Next", command=play_next_song)
prev_button = tk.Button(frame, text="Previous", command=play_prev_song)
shuffle_button = tk.Button(frame, text="Shuffle", command=shuffle_playlist)
volume_scale = tk.Scale(frame, from_=0, to=1, resolution=0.01, orient="horizontal", label="Volume", command=set_volume)

stop_button = tk.Button(frame, text="Stop", command=quit)

play_button.pack(side="left", fill="both", expand=True, padx=5, pady=5, ipadx=10, ipady=10)
pause_play_button.pack(side="left", fill="both", expand=True, padx=5, pady=5, ipadx=10, ipady=10)
prev_button.pack(side="left", fill="both", expand=True, padx=5, pady=5, ipadx=10, ipady=10)
next_button.pack(side="left", fill="both", expand=True, padx=5, pady=5, ipadx=10, ipady=10)
shuffle_button.pack(side="left", fill="both", expand=True, padx=5, pady=5, ipadx=10, ipady=10)
volume_scale.pack(side="right", fill="both", expand=True, padx=5, pady=5, ipadx=10, ipady=10)
stop_button.pack(side="right", fill="both", expand=True, padx=5, pady=5, ipadx=10, ipady=10)

atexit.register(exit_app)
root.protocol("WM_DELETE_WINDOW", exit_app)
root.mainloop()
