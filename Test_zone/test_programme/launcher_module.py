import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess
import sys
import os
import threading
import json

# ----------------- THEME BLUE TECH -----------------
BG_COLOR = "#0b132b"
TAB_COLOR = "#1c2541"
BTN_COLOR = "#1c2541"
BTN_HOVER = "#3a506b"
TEXT_COLOR = "#ffffff"
TEXT_SECONDARY = "#cbd5e1"
ACCENT = "#5bc0be"

# ----------------- CHEMINS -----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def find_manga_root(start_path):
    """
    Remonte l'arborescence pour trouver le dossier Manga,
    identifié par la présence des sous-dossiers clés.
    """
    current = start_path
    while True:
        if all(os.path.exists(os.path.join(current, d)) for d in ["Launcher", "anime_sama", "plugins"]):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            return None
        current = parent

MANGA_ROOT = find_manga_root(BASE_DIR)
if not MANGA_ROOT:
    raise FileNotFoundError("Impossible de trouver le dossier Manga depuis le launcher !")

PLUGINS_JSON = os.path.join(
    MANGA_ROOT,
    "plugins",
    "plugins",
    "instance_plugins.json"
)

# ----------------- FONCTION LOG -----------------
def log(message):
    """Affiche un message dans la console et dans la zone CMD"""
    print(f"[TZ] {message}")
    if 'cmd_text' in globals():
        cmd_text.configure(state='normal')
        cmd_text.insert(tk.END, f"[TZ] {message}\n")
        cmd_text.see(tk.END)
        cmd_text.configure(state='disabled')

def clear_cmd():
    cmd_text.configure(state='normal')
    cmd_text.delete(1.0, tk.END)
    cmd_text.configure(state='disabled')

# ----------------- FONCTION DE LANCEMENT -----------------
def launch_script(script_path):
    # Si chemin absolu → on l’utilise tel quel
    if os.path.isabs(script_path):
        full_path = script_path
    else:
        full_path = os.path.join(MANGA_ROOT, script_path)

    if not os.path.exists(full_path):
        log(f"[ERREUR] Fichier introuvable : {full_path}")
        return


    def run_script():
        log(f"[INFO] Lancement : {full_path}")
        try:
            process = subprocess.Popen(
                [sys.executable, full_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Lecture stdout et stderr en parallèle
            def read_stream(stream):
                for line in iter(stream.readline, ''):
                    log(line.rstrip())
                stream.close()

            threading.Thread(target=read_stream, args=(process.stdout,), daemon=True).start()
            threading.Thread(target=read_stream, args=(process.stderr,), daemon=True).start()

            process.wait()
            log(f"[INFO] Script terminé : {script_path}")
        except Exception as e:
            log(f"[ERREUR] {str(e)}")

    threading.Thread(target=run_script, daemon=True).start()
def load_plugins():
    """Charge les plugins depuis instance_plugins.json"""
    if not os.path.exists(PLUGINS_JSON):
        log("[ERREUR] instance_plugins.json introuvable")
        return {}

    try:
        with open(PLUGINS_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        log(f"[ERREUR] Lecture JSON plugins : {e}")
        return {}

# ----------------- INTERFACE -----------------
root = tk.Tk()
root.title("Lanceur Manga")
root.configure(bg=BG_COLOR)
root.geometry("900x500")
root.resizable(False, False)

# Frame principale
main_frame = tk.Frame(root, bg=BG_COLOR)
main_frame.pack(expand=True, fill="both")

# ----------------- Onglets -----------------
notebook_frame = tk.Frame(main_frame, bg=BG_COLOR)
notebook_frame.pack(side="left", fill="both", expand=True, padx=(10,5), pady=10)

style = ttk.Style()
style.theme_use("default")
style.configure("TNotebook", background=BG_COLOR, borderwidth=0)
style.configure("TNotebook.Tab", background=TAB_COLOR, foreground=TEXT_COLOR, padding=[10,5])
style.map("TNotebook.Tab", background=[("selected", ACCENT)], foreground=[("selected", TEXT_COLOR)])

notebook = ttk.Notebook(notebook_frame)
notebook.pack(expand=True, fill="both")

# ----- Onglet Lanceur de Base -----
frame_base = tk.Frame(notebook, bg=BG_COLOR)
notebook.add(frame_base, text="Lanceur de Base")

base_scripts = [
    ("Launcher.py", "Launcher/Launcher.py"),
    ("Lecture.py", "anime_sama/lecture.py"),
    ("Mangadex.py", "mangadex/main.py"),
    ("Plugin Interface.py", "plugins/plugin_interface.py"),
    ("PDF V2.py", "programme/pdfV2.py"),
    ("Update.py", "update.py"),
]

for name, path in base_scripts:
    btn = tk.Button(
        frame_base, text=name, bg=BTN_COLOR, fg=TEXT_COLOR, activebackground=ACCENT,
        width=30, height=2, command=lambda p=path: launch_script(p)
    )
    btn.pack(pady=5)
    btn.bind("<Enter>", lambda e, b=btn: b.config(bg=BTN_HOVER))
    btn.bind("<Leave>", lambda e, b=btn: b.config(bg=BTN_COLOR))

# ----- Onglet Anime Sama -----
frame_anime = tk.Frame(notebook, bg=BG_COLOR)
notebook.add(frame_anime, text="Anime Sama")

anime_scripts = [
    ("MangaV3.py", "anime_sama/mangaV3.py"),
    ("ShareV2.py", "anime_sama/shareV2.py"),
    ("APPV3.py", "anime_sama/APP/APPV3.py"),
    ("Scraper Domaine.py", "anime_sama/APP/scraper_domaine.py"),
    ("Launcher Anime Sama.py", "anime_sama/launcher.py"),
    ("State_Extra.py", "anime_sama/APP/State_Scan/State_Extra.py"),
]

for name, path in anime_scripts:
    btn = tk.Button(
        frame_anime, text=name, bg=BTN_COLOR, fg=TEXT_COLOR, activebackground=ACCENT,
        width=30, height=2, command=lambda p=path: launch_script(p)
    )
    btn.pack(pady=5)
    btn.bind("<Enter>", lambda e, b=btn: b.config(bg=BTN_HOVER))
    btn.bind("<Leave>", lambda e, b=btn: b.config(bg=BTN_COLOR))

# ----- Onglet Plugins -----
frame_plugins = tk.Frame(notebook, bg=BG_COLOR)
notebook.add(frame_plugins, text="Plugins")

plugins = load_plugins()

if not plugins:
    tk.Label(
        frame_plugins,
        text="Aucun plugin trouvé",
        bg=BG_COLOR,
        fg=TEXT_SECONDARY
    ).pack(pady=20)
else:
    for plugin_name, plugin_path in plugins.items():
        btn = tk.Button(
            frame_plugins,
            text=plugin_name,
            bg=BTN_COLOR,
            fg=TEXT_COLOR,
            activebackground=ACCENT,
            width=30,
            height=2,
            command=lambda p=plugin_path: launch_script(p)
        )
        btn.pack(pady=5)
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg=BTN_HOVER))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg=BTN_COLOR))

# ----------------- Zone CMD -----------------
cmd_frame = tk.Frame(main_frame, bg="#1a1a1a", width=350)
cmd_frame.pack(side="right", fill="y", padx=(5,10), pady=10)

cmd_label = tk.Label(cmd_frame, text="CMD", bg="#1a1a1a", fg=ACCENT, font=("Segoe UI", 12, "bold"))
cmd_label.pack(pady=5)

cmd_text = scrolledtext.ScrolledText(cmd_frame, bg="#0b132b", fg=TEXT_COLOR,
                                     state='disabled', width=40, height=30, font=("Consolas", 10))
cmd_text.pack(fill="both", expand=True, padx=5, pady=5)

# Bouton Effacer CMD
clear_btn = tk.Button(cmd_frame, text="Effacer CMD", bg=BTN_COLOR, fg=TEXT_COLOR,
                      activebackground=ACCENT, command=clear_cmd)
clear_btn.pack(pady=5)
clear_btn.bind("<Enter>", lambda e: clear_btn.config(bg=BTN_HOVER))
clear_btn.bind("<Leave>", lambda e: clear_btn.config(bg=BTN_COLOR))

root.mainloop()
