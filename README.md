# youtube-audio-downloader

A simple app with one button. Copy a YouTube link, click the app, and the
audio gets saved to your Downloads folder automatically. That's it.

## Setup

1. **Download Python** — get it from https://www.python.org/downloads/ and
   install it. On the first install screen, make sure to check **"Add
   python.exe to PATH"**.

2. **Download the three files** in this repo (`yt_audio_downloader.py`,
   `run.bat`, `setup.bat`) into a folder.

3. **Create a folder named `ffmpeg`** inside that same folder.

4. **Get ffmpeg:**
   - Go to https://www.gyan.dev/ffmpeg/builds/
   - Under "release builds", download `ffmpeg-release-essentials.zip`
   - Once downloaded, right-click the zip file → **Extract All**

5. **Copy the `bin` folder** from inside the extracted ffmpeg files, and
   place it in your `ffmpeg` folder as-is — so you end up with
   `ffmpeg\bin\ffmpeg.exe`.

6. **Double-click `setup.bat`** — this installs everything the app needs.

## Using it

1. Just click on the `run.bat` file.
2. Copy a video link, then click the app icon.
3. The audio file downloads automatically into the `downloads` folder.

## Something not working?

- **"python is not recognized"** → Python wasn't added to PATH during
  install. Reinstall Python and make sure to check that box this time.
- **"pip is not recognized"** → Same fix as above.
- **Download fails with a 403 error** → Run `pip install --upgrade yt-dlp`
  inside your activated virtual environment. YouTube changes things often
  and yt-dlp needs to stay up to date.
- **App downloads a video instead of just audio** → Make sure "Fast mode"
  is ticked in the app, and that you have the latest version of this script.

If you're still stuck, open an Issue on this GitHub repo describing exactly
what happened — copy-paste any error message you see.

---

## A note on responsible use

Only download audio you actually have the right to save — your own
recordings, royalty-free tracks, or content a creator has explicitly made
downloadable. Downloading copyrighted material without permission can
violate YouTube's Terms of Service and copyright law where you live.

## License

MIT — see [LICENSE](LICENSE). Free to use, modify, and share.
