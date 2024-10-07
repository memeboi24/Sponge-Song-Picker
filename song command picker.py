import tkinter as tk
import pyperclip
from tkinter import messagebox
import webbrowser
import json

# Load commands from JSON file
with open("songs.json", "r") as f:
    commands = json.load(f)

# Paginate songs, 10 per page
songs_per_page = 10
song_titles = list(commands.keys())

# Function to display songs on the current page
def display_page(page):
    for widget in root.winfo_children():
        widget.destroy()

    start = page * songs_per_page
    end = start + songs_per_page
    page_songs = song_titles[start:end]

    for title in page_songs:
        command = commands[title]
        link = command.split()[-1]

        frame = tk.Frame(root)
        frame.pack(pady=5)

        btn_copy = tk.Button(frame, text=title, command=lambda t=title, c=command: copy_to_clipboard(c, t))
        btn_copy.pack(side="left", padx=5)

        btn_preview = tk.Button(frame, text="Preview", command=lambda l=link: open_youtube(l))
        btn_preview.pack(side="left", padx=5)

    # Navigation buttons
    if page > 0:
        btn_prev = tk.Button(root, text="Previous Page", command=lambda: display_page(page - 1))
        btn_prev.pack(pady=5)

    if end < len(song_titles):
        btn_next = tk.Button(root, text="Next Page", command=lambda: display_page(page + 1))
        btn_next.pack(pady=5)

# Function to copy command to clipboard and notify user
def copy_to_clipboard(command, title):
    pyperclip.copy(command)
    messagebox.showinfo("Copied", f"Copied command for '{title}' to clipboard, simply paste it into the #song-topic channel, upvote and bell it!")

# Function to open YouTube link
def open_youtube(link):
    webbrowser.open(link)

# GUI setup
root = tk.Tk()
root.title("Ai Sponge Rehydrated AI Song Picker")

# Start with the first page (page 0)
display_page(0)

# Start GUI loop
root.mainloop()
