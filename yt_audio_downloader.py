"""
One-Click YouTube Audio Downloader (SELF-CONTAINED VERSION)
-------------------------------------------------------------
Everything this script needs (the venv, ffmpeg, and downloaded
files) lives inside this same folder. Delete the folder later
and nothing is left behind anywhere else on your PC.

Folder layout expected (see setup.bat which creates this for you):

    Music_saver\
      venv\
      ffmpeg\bin\ffmpeg.exe
      downloads\
      yt_audio_downloader.py   <-- this file

RUN: double-click run.bat (don't run this .py file directly unless
     your venv is already activated).
"""

import os
import re
import threading
import tkinter as tk
from tkinter import messagebox, filedialog

import yt_dlp

YOUTUBE_URL_PATTERN = re.compile(
    r"(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)[\w\-]+"
)

# ---- Everything is relative to THIS script's location ----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_FOLDER = os.path.join(BASE_DIR, "downloads")
FFMPEG_DIR = os.path.join(BASE_DIR, "ffmpeg", "bin")

os.makedirs(SAVE_FOLDER, exist_ok=True)


def download_audio(url: str, folder: str, status_callback, fast_mode: bool):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(folder, "%(title)s.%(ext)s"),
        "ffmpeg_location": FFMPEG_DIR,
        "quiet": True,
        "noprogress": True,
        "extractor_args": {"youtube": {"player_client": ["android", "web"]}},
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                           "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        },
        "concurrent_fragment_downloads": 8,
        "noplaylist": True,  # only download the single video, ignore any &list=... in the URL
    }

    if not fast_mode:
        # Convert to mp3 (slower, but a universal .mp3 file)
        ydl_opts["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ]
    else:
        # Still strip out any video track and keep audio only - just don't
        # re-encode it, so this stays fast. If the downloaded stream was
        # already audio-only, this is a no-op.
        ydl_opts["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "best",  # keep original audio codec, no re-encode
            }
        ]

    try:
        status_callback("Downloading... please wait")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        status_callback("Done! Saved to:\n" + folder)
    except Exception as e:
        status_callback(f"Error: {e}")


class App:
    def __init__(self, root):
        self.root = root
        root.title("YouTube Audio Downloader")
        root.geometry("420x220")
        root.resizable(False, False)

        tk.Label(root, text="Paste YouTube link:", font=("Segoe UI", 10)).pack(pady=(15, 5))
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack(pady=5)

        self.folder_var = tk.StringVar(value=SAVE_FOLDER)
        folder_frame = tk.Frame(root)
        folder_frame.pack(pady=5)
        tk.Label(folder_frame, textvariable=self.folder_var, font=("Segoe UI", 8), fg="gray").pack(side="left")
        tk.Button(folder_frame, text="Change folder", command=self.change_folder).pack(side="left", padx=5)

        self.fast_mode_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            root, text="Fast mode (skip mp3 conversion, saves original audio)",
            variable=self.fast_mode_var, font=("Segoe UI", 8)
        ).pack(pady=(0, 2))

        self.auto_download_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            root, text="Auto-download as soon as I copy a YouTube link",
            variable=self.auto_download_var, font=("Segoe UI", 8)
        ).pack(pady=(0, 5))

        self.last_clipboard = ""
        root.bind("<FocusIn>", self.check_clipboard)

        self.download_btn = tk.Button(
            root, text="\u2b07 Download", font=("Segoe UI", 11, "bold"),
            bg="#e53935", fg="white", command=self.on_download
        )
        self.download_btn.pack(pady=15, ipadx=10, ipady=5)

        self.status_label = tk.Label(root, text="", font=("Segoe UI", 9), fg="green", wraplength=380)
        self.status_label.pack(pady=5)

    def change_folder(self):
        chosen = filedialog.askdirectory()
        if chosen:
            self.folder_var.set(chosen)

    def check_clipboard(self, event=None):
        try:
            clip = self.root.clipboard_get()
        except tk.TclError:
            return
        if clip and clip != self.last_clipboard and YOUTUBE_URL_PATTERN.search(clip):
            self.last_clipboard = clip
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, clip)
            if self.auto_download_var.get():
                self.on_download()

    def set_status(self, text):
        self.status_label.config(text=text)

    def on_download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Missing link", "Paste a YouTube URL first.")
            return
        folder = self.folder_var.get()
        self.download_btn.config(state="disabled")
        self.set_status("Starting...")

        def worker():
            download_audio(url, folder, self.set_status, self.fast_mode_var.get())
            self.download_btn.config(state="normal")

        threading.Thread(target=worker, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()