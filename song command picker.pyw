import tkinter as tk
from tkinter import messagebox
import pyperclip
import webbrowser
import json

# Load commands from JSON file
with open("songs.json", "r") as f:
    commands = json.load(f)

# Paginate songs, 10 per page
songs_per_page = 10
song_titles = list(commands.keys())

# Function to save updated commands to JSON file
def save_commands():
    with open("songs.json", "w") as f:
        json.dump(commands, f, indent=4)

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

    # Navigation buttons and add song button at the bottom
    nav_frame = tk.Frame(root)
    nav_frame.pack(pady=10)

    if page > 0:
        btn_prev = tk.Button(nav_frame, text="Previous Page", command=lambda: display_page(page - 1))
        btn_prev.pack(side="left", padx=5)

    if end < len(song_titles):
        btn_next = tk.Button(nav_frame, text="Next Page", command=lambda: display_page(page + 1))
        btn_next.pack(side="left", padx=5)

    btn_add_song = tk.Button(nav_frame, text="Add Song", command=add_song_popup)
    btn_add_song.pack(side="left", padx=5)

# Function to copy command to clipboard and notify user
def copy_to_clipboard(command, title):
    pyperclip.copy(command)
    messagebox.showinfo("Copied", f"Copied command for '{title}' to clipboard, simply paste it into the #song-topic channel, upvote and bell it!")

# Function to open YouTube link
def open_youtube(link):
    webbrowser.open(link)

# Function to add a new song entry through a pop-up window
def add_song_popup():
    # Create a new window
    popup = tk.Toplevel(root)
    popup.title("Add New Song")

    # Song Title input
    tk.Label(popup, text="Song Title:").pack(pady=5)
    entry_title = tk.Entry(popup)
    entry_title.pack(pady=5)

    # Song Command input
    tk.Label(popup, text="Topic Command:").pack(pady=5)
    entry_command = tk.Entry(popup)
    entry_command.pack(pady=5)

    # Function to add the song and update the list
    def add_song():
        title = entry_title.get()
        command = entry_command.get()
        if title and command:
            commands[title] = command
            song_titles.append(title)
            save_commands()  # Save to JSON
            messagebox.showinfo("Success", f"Added '{title}' to the song list!")
            popup.destroy()
            display_page(0)  # Refresh display
        else:
            messagebox.showerror("Error", "Both title and command are required!")

    # Submit button
    btn_submit = tk.Button(popup, text="Add Song", command=add_song)
    btn_submit.pack(pady=10)

# GUI setup
root = tk.Tk()
root.title("Ai Sponge Rehydrated AI Song Picker")

# Start with the first page (page 0)
display_page(0)

# Start GUI loop
root.mainloop()
