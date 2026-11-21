# Cyber Locker

A simple cyberpunk-themed folder launcher built with Python.

## Summary

Cyber Locker is a small desktop application that uses a password interface to open a hidden folder in Windows. It features an animated GIF background, looping music, and a cyberpunk-style interface.

**Note:** This is a fun project, not a real folder-locking or encryption tool. It does not prevent users from accessing the folder directly. It simply provides a password-gated interface for opening a folder that has been hidden using Windows settings.

## Motivation

I wanted to create a fun way to access my hidden folders instead of opening them directly through File Explorer. This project was also an opportunity to experiment with Python desktop applications and multimedia features.

## Technologies

- **Python / Tkinter** — GUI and password verification
- **Pillow** — Animated GIF background and image processing
- **Pygame** — Background music with infinite looping
- **PyInstaller** — Packaging the application into a Windows executable
- **Windows API (ctypes)** — Dark title bar customization

## How to Use

**1. Hide your folder**

In Windows File Explorer, right-click the folder you want to hide, select **Properties**, and enable **Hidden**.

Make sure **View → Show → Hidden items** is turned off.

**2. Download and install dependencies**

Clone the repository and install the required packages:

```bash
git clone https://github.com/YOUR_USERNAME/cyber-locker.git
cd cyber-locker
python -m pip install Pillow pygame-ce pyinstaller
```

**3. Configure the application**

Open `locker.py` and modify:

```python
FOLDER = r"D:\secret"
PASSWORD = "YOUR_PASSWORD"
```

Replace these values with your folder path and desired password.

Place your `background.gif` and `music.mp3` files in the same directory as `locker.py`.

**4. Run the application**

```bash
python locker.py
```

Enter the correct password to open your hidden folder.

**5. Build an executable (optional)**

```powershell
python -m PyInstaller --onefile --windowed --name Locker --add-data "background.gif;." --add-data "music.mp3;." locker.py
```

The executable will be generated at `dist/Locker.exe`.

---

*For entertainment and learning purposes only. Hidden folders and hardcoded passwords do not provide actual file security.*