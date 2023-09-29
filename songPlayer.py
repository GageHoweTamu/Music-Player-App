# ensure Python is installed
# run "pip install pygame" or "pip3 install pygame"

import os
import pygame
import signal
import sys
import atexit
import random
import tkinter as tk
from tkinter import filedialog
import time

os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'

volume = 1

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

def play_songs(songs, folder_path, shuffle):
    random.seed(time.time())
    if shuffle:
        random.shuffle(songs)
    pygame.mixer.init()
    pygame.mixer.music.set_volume(volume)  # Adjust the volume
    paused = False
    current_song_index = 0

    while True:
        if paused:
            while True:
                command = input("Type 'r' to resume: ").lower()
                if command == "r":
                    pygame.mixer.music.unpause()
                    paused = False
                    break

        if not pygame.mixer.music.get_busy():
            current_song_index += 1
            if current_song_index >= len(songs):
                current_song_index = 0
                if shuffle:
                    random.shuffle(songs)
            pygame.mixer.music.load(songs[current_song_index])
            pygame.mixer.music.play()
            print(f"\nNow playing: {os.path.basename(songs[current_song_index])}\n")

        if not paused:
            while pygame.mixer.music.get_busy():
                command = input("Type 'search' to search for a song, \n'p' to pause, \n'r' to resume, \n's' to skip, \n'q' to quit, \n'v' to adjust volume, or \n'sh' to toggle shuffle: ").lower()
                if command == "search":
                    query = input("Enter a search query: ")
                    matching_songs = [file for file in music_files if query.lower() in os.path.basename(file).lower()]
                    if len(matching_songs) == 0:
                        print("No matching songs found.")
                    else:
                        songs = matching_songs
                        current_song_index = 0
                        if shuffle:
                            random.shuffle(songs)

                        pygame.mixer.music.load(songs[current_song_index])
                        pygame.mixer.music.play()
                        print(f"\nNow playing: {os.path.basename(songs[current_song_index])}\n")
                        break
                elif command == "p":
                    pygame.mixer.music.pause()
                    paused = True
                    break
                elif command == "r":
                    pygame.mixer.music.unpause()
                    paused = False
                    break
                elif command == "s":
                    pygame.mixer.music.stop()
                    current_song_index += 1
                    if current_song_index >= len(songs):
                        current_song_index = 0
                        if shuffle:
                            random.shuffle(songs)
                    pygame.mixer.music.load(songs[current_song_index])
                    pygame.mixer.music.play()
                    print(f"\nNow playing: {os.path.basename(songs[current_song_index])}\n")
                    break
                elif command == "q":
                    pygame.mixer.music.stop()
                    pygame.mixer.quit()
                    sys.exit(0)
                elif command == "sh":
                    shuffle = not shuffle
                    if shuffle:
                        random.shuffle(songs)
                    print(f"Shuffle {'on' if shuffle else 'off'}")
                elif command == "v":
                    pygame.mixer.music.set_volume(float(input("Enter a volume between 0 and 1: ")))
                    break

        if current_song_index == len(songs) - 1 and not pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            break

if __name__ == "__main__":
    folder_path = ""
    music_files = find_music_files(folder_path)

    if len(music_files) == 0:
        print("No music files were found in the specified folder.")
    else:
        print(f"Found {len(music_files)} music files in the folder and its subfolders.")
        play_songs(music_files, folder_path, shuffle=True)

    atexit.register(pygame.mixer.quit)