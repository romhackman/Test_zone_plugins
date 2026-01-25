import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import sys

# ----------------- THEME BLUE TECH -----------------
BG_COLOR = "#0b132b"
BTN_COLOR = "#1c2541"
BTN_HOVER = "#3a506b"
TEXT_COLOR = "#ffffff"
TEXT_SECONDARY = "#cbd5e1"
ACCENT = "#5bc0be"

# ----------------- Variables -----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MANGA_ROOT = os.path.abspath(
    os.path.join(BASE_DIR, "..", "..", "..", "..")
)

VERSION_FILE = os.path.join(MANGA_ROOT, "V5.1.manga")
LAUNCHER_PATH = os.path.join(MANGA_ROOT, "Launcher", "Launcher.py")

DEFAULT_VERSION = "5.1"

# ----------------- Fonctions -----------------
def log(message):
    """Affiche le message dans la console avec préfixe [TZ]"""
    print(f"[TZ] {message}")

def save_version():
    new_version = entry.get().strip()
    log(f"Tentative de changement de version vers : {new_version}")

    if not new_version:
        log("Erreur : Version invalide")
        messagebox.showerror("Erreur", "Version invalide")
        return

    if not allow_higher.get() and new_version > DEFAULT_VERSION:
        log("Erreur : Version supérieure interdite sans autorisation")
        messagebox.showerror(
            "Erreur",
            "Version supérieure interdite sans autorisation"
        )
        return

    old_file = os.path.join(MANGA_ROOT, f"V{DEFAULT_VERSION}.manga")
    new_file = os.path.join(MANGA_ROOT, f"V{new_version}.manga")

    if not os.path.exists(old_file):
        log(f"Erreur : Fichier introuvable : {old_file}")
        messagebox.showerror(
            "Erreur",
            f"Fichier introuvable :\n{old_file}"
        )
        return

    try:
        os.rename(old_file, new_file)
        log(f"Version modifiée avec succès : V{new_version}.manga")
    except Exception as e:
        log(f"Erreur lors du renommage : {str(e)}")
        messagebox.showerror("Erreur", str(e))
        return

    if messagebox.askyesno(
        "Launcher",
        f"Version modifiée : V{new_version}.manga\n\nLancer le Launcher ?"
    ):
        if os.path.exists(LAUNCHER_PATH):
            log("Lancement de Launcher.py")
            subprocess.Popen([sys.executable, LAUNCHER_PATH])
        else:
            log("Erreur : Launcher.py introuvable")
            messagebox.showerror(
                "Erreur",
                "Launcher.py introuvable"
            )

# ----------------- Interface -----------------
root = tk.Tk()
root.title("Gestion de version")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

# Label
tk.Label(
    root,
    text="Version de l'application :",
    bg=BG_COLOR,
    fg=TEXT_COLOR,
    font=("Segoe UI", 11)
).pack(pady=5)

# Entry
entry = tk.Entry(
    root,
    bg=BTN_COLOR,
    fg=TEXT_COLOR,
    insertbackground=TEXT_COLOR,
    font=("Segoe UI", 11),
    width=15,
    justify="center"
)
entry.insert(0, DEFAULT_VERSION)
entry.pack(pady=5)

# Checkbox
allow_higher = tk.BooleanVar()
tk.Checkbutton(
    root,
    text="Autoriser une version supérieure",
    variable=allow_higher,
    bg=BG_COLOR,
    fg=TEXT_SECONDARY,
    selectcolor=BTN_COLOR,
    activebackground=BG_COLOR,
    font=("Segoe UI", 10)
).pack(pady=5)

# Bouton avec hover
def on_enter(e):
    e.widget['bg'] = BTN_HOVER

def on_leave(e):
    e.widget['bg'] = BTN_COLOR

button = tk.Button(
    root,
    text="Valider",
    bg=BTN_COLOR,
    fg=TEXT_COLOR,
    activebackground=ACCENT,
    font=("Segoe UI", 11),
    width=20,
    command=save_version
)
button.pack(pady=15)
button.bind("<Enter>", on_enter)
button.bind("<Leave>", on_leave)

root.mainloop()
