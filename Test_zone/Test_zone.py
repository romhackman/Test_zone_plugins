import tkinter as tk
import subprocess
import os
import sys
from tkinter import messagebox
from PIL import Image, ImageTk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEST_VERSION_PATH = os.path.join(BASE_DIR, "test_programme", "test_version.py")
PLUGIN_MAKER_PATH = os.path.join(BASE_DIR, "test_programme", "plugin_maker.py")
IMAGE_PATH = os.path.join(BASE_DIR, "image.png")  # Image principale
LOGO_PATH = os.path.join(BASE_DIR, "logo.png")    # Logo de la fenêtre

# 🎨 THEME BLUE TECH
BG_COLOR = "#0b132b"
BTN_COLOR = "#1c2541"
BTN_HOVER = "#3a506b"
TEXT_COLOR = "#ffffff"
TEXT_SECONDARY = "#cbd5e1"
ACCENT = "#5bc0be"

# --- Fonction de log ---
def log(message):
    print(f"[TZ] {message}")  # Remplace [LOG] par [TZ]

def launch_test_version():
    log("Tentative de lancement de test_version.py")
    if not os.path.exists(TEST_VERSION_PATH):
        messagebox.showerror("Erreur", "test_version.py introuvable")
        log("Erreur : test_version.py introuvable")
        return
    subprocess.Popen([sys.executable, TEST_VERSION_PATH])
    log("test_version.py lancé")

def launch_plugin_maker():
    log("Tentative de lancement de plugin_maker.py")
    if not os.path.exists(PLUGIN_MAKER_PATH):
        messagebox.showerror("Erreur", "plugin_maker.py introuvable")
        log("Erreur : plugin_maker.py introuvable")
        return
    subprocess.Popen([sys.executable, PLUGIN_MAKER_PATH])
    log("plugin_maker.py lancé")

def on_enter(e):
    e.widget.configure(bg=BTN_HOVER)

def on_leave(e):
    e.widget.configure(bg=BTN_COLOR)

# --- Fenêtre principale ---
log("Initialisation de la fenêtre principale")
root = tk.Tk()
root.title("Test Zone")
root.configure(bg=BG_COLOR)
root.geometry("900x500")
root.resizable(False, False)

# --- Logo de la fenêtre ---
if os.path.exists(LOGO_PATH):
    try:
        logo_img = Image.open(LOGO_PATH)
        logo_img = logo_img.resize((64, 64), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_img)
        root.iconphoto(True, logo_photo)
        log("Logo chargé avec succès")
    except Exception as e:
        log(f"Impossible de charger le logo: {e}")

# --- Frame principale ---
main_frame = tk.Frame(root, bg=BG_COLOR)
main_frame.pack(fill="both", expand=True)

# --- Partie gauche : boutons ---
left_frame = tk.Frame(main_frame, bg=BG_COLOR)
left_frame.pack(side="left", padx=20, pady=20)

title = tk.Label(left_frame, text="TEST ZONE", bg=BG_COLOR, fg=ACCENT,
                 font=("Segoe UI", 16, "bold"))
title.pack(pady=(0, 10))

subtitle = tk.Label(left_frame, text="Interface de lancement des tests",
                    bg=BG_COLOR, fg=TEXT_SECONDARY, font=("Segoe UI", 9))
subtitle.pack(pady=(0, 15))

btn1 = tk.Button(left_frame, text="Lancer le test de version",
                 command=launch_test_version,
                 bg=BTN_COLOR, fg=TEXT_COLOR,
                 activebackground=BTN_HOVER, activeforeground=TEXT_COLOR,
                 width=32, height=2, relief="flat")
btn1.pack(pady=6)

btn2 = tk.Button(left_frame, text="Plugin Maker",
                 command=launch_plugin_maker,
                 bg=BTN_COLOR, fg=TEXT_COLOR,
                 activebackground=BTN_HOVER, activeforeground=TEXT_COLOR,
                 width=32, height=2, relief="flat")
btn2.pack(pady=6)

for btn in (btn1, btn2):
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

# --- Partie droite : image redimensionnée ---
right_frame = tk.Frame(main_frame, bg=BG_COLOR)
right_frame.pack(side="right", padx=20, pady=20, fill="both", expand=True)

if os.path.exists(IMAGE_PATH):
    img_orig = Image.open(IMAGE_PATH)

    # Taille maximale pour l'image
    max_width = 400
    max_height = 460

    ratio_orig = img_orig.width / img_orig.height
    ratio_max = max_width / max_height

    if ratio_orig > ratio_max:
        new_width = max_width
        new_height = int(max_width / ratio_orig)
    else:
        new_height = max_height
        new_width = int(max_height * ratio_orig)

    img_resized = img_orig.resize((new_width, new_height), Image.LANCZOS)
    photo = ImageTk.PhotoImage(img_resized)

    image_label = tk.Label(right_frame, image=photo, bg=BG_COLOR)
    image_label.image = photo  # référence nécessaire pour Tkinter
    image_label.pack(expand=True)
    log("Image principale chargée")
else:
    tk.Label(right_frame, text="(Aucune image)", bg=BG_COLOR,
             fg=TEXT_COLOR, font=("Segoe UI", 12)).pack(expand=True)
    log("Aucune image trouvée")

log("Interface prête")
root.mainloop()
log("Programme terminé")
