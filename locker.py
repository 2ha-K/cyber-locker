
import os
import sys
import ctypes
import tkinter as tk
import pygame
from PIL import Image, ImageTk, ImageSequence, ImageDraw

# ===== CONFIG =====
FOLDER = r"D:\secret"
PASSWORD = "KEVIn0120!!"

WIDTH = 768
HEIGHT = 480

PURPLE = "#C56BFF"
CYAN = "#68F5FF"
WHITE = "#F3E8FF"
RED = "#FF5277"
DARK = "#160B26"

# Login panel: left-center
PANEL_X = 175
PANEL_Y = HEIGHT // 2
PANEL_WIDTH = 310
PANEL_HEIGHT = 225

# Music settings
MUSIC_VOLUME = 0.35


def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)

    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        filename
    )


# ===== WINDOW =====
root = tk.Tk()
root.iconbitmap(resource_path("icon.ico"))
root.title("CYBER LOCKER")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)
root.configure(bg=DARK)


# ===== BLACK WINDOWS TITLE BAR =====
def set_dark_title_bar(window):
    if sys.platform != "win32":
        return

    window.update()

    hwnd = ctypes.windll.user32.GetParent(
        window.winfo_id()
    )

    dwm = ctypes.windll.dwmapi

    def set_attribute(attribute, value):
        data = ctypes.c_int(value)

        return dwm.DwmSetWindowAttribute(
            hwnd,
            attribute,
            ctypes.byref(data),
            ctypes.sizeof(data)
        )

    try:
        # Enable dark title bar
        result = set_attribute(20, 1)

        # Older Windows 10 compatibility
        if result != 0:
            set_attribute(19, 1)

        # Black title bar
        set_attribute(35, 0x000000)

        # White title text
        set_attribute(36, 0x00FFFFFF)

        # Black window border
        set_attribute(34, 0x000000)

    except (OSError, AttributeError):
        pass


set_dark_title_bar(root)


# ===== BACKGROUND MUSIC =====
music_started = False

try:
    pygame.mixer.init()

    pygame.mixer.music.load(
        resource_path("music.mp3")
    )

    pygame.mixer.music.set_volume(MUSIC_VOLUME)

    # -1 means loop forever
    pygame.mixer.music.play(loops=-1)

    music_started = True

except (pygame.error, OSError) as error:
    print("Music unavailable:", error)


def stop_music():
    if music_started:
        pygame.mixer.music.stop()
        pygame.mixer.quit()


def close_app():
    stop_music()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", close_app)


# ===== CANVAS =====
canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    highlightthickness=0,
    bd=0
)

canvas.pack(fill="both", expand=True)


# ===== GIF BACKGROUND =====
gif = Image.open(resource_path("background.gif"))

frames = []
durations = []

for frame in ImageSequence.Iterator(gif):
    image = frame.convert("RGBA")

    # Preserve original aspect ratio
    image.thumbnail(
        (WIDTH, HEIGHT),
        Image.Resampling.NEAREST
    )

    background = Image.new(
        "RGBA",
        (WIDTH, HEIGHT),
        DARK
    )

    x = (WIDTH - image.width) // 2
    y = (HEIGHT - image.height) // 2

    background.alpha_composite(image, (x, y))

    # Semi-transparent login panel
    overlay = Image.new(
        "RGBA",
        (WIDTH, HEIGHT),
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(overlay)

    left = PANEL_X - PANEL_WIDTH // 2
    top = PANEL_Y - PANEL_HEIGHT // 2
    right = PANEL_X + PANEL_WIDTH // 2
    bottom = PANEL_Y + PANEL_HEIGHT // 2

    draw.rectangle(
        (left, top, right, bottom),
        fill=(18, 8, 35, 205),
        outline=(197, 107, 255, 255),
        width=2
    )

    # Purple neon top border
    draw.rectangle(
        (left, top, right, top + 4),
        fill=(197, 107, 255, 255)
    )

    background = Image.alpha_composite(
        background,
        overlay
    )

    frames.append(
        ImageTk.PhotoImage(background)
    )

    durations.append(
        max(40, frame.info.get("duration", 100))
    )

gif.close()


# ===== BACKGROUND ANIMATION =====
background_id = canvas.create_image(
    0, 0,
    anchor="nw",
    image=frames[0]
)


def animate(index=0):
    canvas.itemconfig(
        background_id,
        image=frames[index]
    )

    root.after(
        durations[index],
        animate,
        (index + 1) % len(frames)
    )


animate()


# ===== LOGIN TITLE =====
canvas.create_text(
    PANEL_X,
    PANEL_Y - 75,
    text="◈ PRIVATE ACCESS",
    fill=WHITE,
    font=("Consolas", 15, "bold")
)

canvas.create_text(
    PANEL_X,
    PANEL_Y - 45,
    text="[ ENTER ACCESS CODE ]",
    fill=PURPLE,
    font=("Consolas", 9, "bold")
)


# ===== PASSWORD INPUT =====
password_entry = tk.Entry(
    root,
    show="*",
    font=("Consolas", 13),
    justify="center",
    bg=DARK,
    fg=WHITE,
    insertbackground=CYAN,
    relief="flat",
    highlightthickness=2,
    highlightbackground=PURPLE,
    highlightcolor=CYAN
)

canvas.create_window(
    PANEL_X,
    PANEL_Y - 5,
    window=password_entry,
    width=250,
    height=34
)

password_entry.focus_set()


# ===== STATUS =====
status_id = canvas.create_text(
    PANEL_X,
    PANEL_Y + 35,
    text="◈ SYSTEM READY",
    fill=CYAN,
    font=("Consolas", 9, "bold")
)


# ===== UNLOCK FUNCTION =====
def unlock(event=None):
    if password_entry.get() == PASSWORD:
        try:
            os.startfile(FOLDER)
            close_app()

        except OSError:
            canvas.itemconfig(
                status_id,
                text="✕ FOLDER NOT FOUND",
                fill=RED
            )

    else:
        canvas.itemconfig(
            status_id,
            text="✕ ACCESS DENIED",
            fill=RED
        )

        password_entry.delete(0, tk.END)
        password_entry.focus_set()


def reset_status(event=None):
    canvas.itemconfig(
        status_id,
        text="◈ SYSTEM READY",
        fill=CYAN
    )


password_entry.bind("<Key>", reset_status)
root.bind("<Return>", unlock)


# ===== UNLOCK BUTTON =====
button = tk.Button(
    root,
    text="[ UNLOCK ]",
    command=unlock,
    font=("Consolas", 11, "bold"),
    bg="#7435B5",
    fg="white",
    activebackground=PURPLE,
    activeforeground="white",
    relief="flat",
    bd=0,
    cursor="hand2"
)

canvas.create_window(
    PANEL_X,
    PANEL_Y + 75,
    window=button,
    width=170,
    height=32
)


# ===== BUTTON HOVER EFFECT =====
button.bind(
    "<Enter>",
    lambda e: button.config(bg=PURPLE)
)

button.bind(
    "<Leave>",
    lambda e: button.config(bg="#7435B5")
)


# ===== START APPLICATION =====
root.mainloop()
