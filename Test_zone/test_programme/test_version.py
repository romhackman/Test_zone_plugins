import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Racine Manga
MANGA_ROOT = os.path.abspath(
    os.path.join(BASE_DIR, "..", "..", "..", "..")
)

VERSION_FILE = os.path.join(MANGA_ROOT, "V3.1.manga")
LAUNCHER_PATH = os.path.join(MANGA_ROOT, "Launcher", "Launcher.py")

DEFAULT_VERSION = "3.1"

def save_version():
    new_version = entry.get().strip()

    if not new_version:
        messagebox.showerror("Erreur", "Version invalide")
        return

    if not allow_higher.get():
        if new_version > DEFAULT_VERSION:
            messagebox.showerror(
                "Erreur",
                "Version supérieure interdite sans autorisation"
            )
            return

    old_file = os.path.join(MANGA_ROOT, f"V{DEFAULT_VERSION}.manga")
    new_file = os.path.join(MANGA_ROOT, f"V{new_version}.manga")

    if not os.path.exists(old_file):
        messagebox.showerror(
            "Erreur",
            f"Fichier introuvable :\n{old_file}"
        )
        return

    try:
        os.rename(old_file, new_file)
    except Exception as e:
        messagebox.showerror("Erreur", str(e))
        return

    if messagebox.askyesno(
        "Launcher",
        f"Version modifiée : V{new_version}.manga\n\nLancer le Launcher ?"
    ):
        if os.path.exists(LAUNCHER_PATH):
            subprocess.Popen([sys.executable, LAUNCHER_PATH])
        else:
            messagebox.showerror(
                "Erreur",
                "Launcher.py introuvable"
            )

root = tk.Tk()
root.title("Test de version")

tk.Label(
    root,
    text="Version de l'application :"
).pack(pady=5)

entry = tk.Entry(root)
entry.insert(0, DEFAULT_VERSION)
entry.pack(pady=5)

allow_higher = tk.BooleanVar()
tk.Checkbutton(
    root,
    text="Autoriser une version supérieure",
    variable=allow_higher
).pack(pady=5)

tk.Button(
    root,
    text="Valider",
    command=save_version,
    width=25
).pack(pady=15)

root.mainloop()
