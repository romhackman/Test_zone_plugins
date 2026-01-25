import os
import tkinter as tk
from tkinter import messagebox, filedialog

# ----------------- THEME BLUE TECH -----------------
BG_COLOR = "#0b132b"
BTN_COLOR = "#1c2541"
BTN_HOVER = "#3a506b"
TEXT_COLOR = "#ffffff"
TEXT_SECONDARY = "#cbd5e1"
ACCENT = "#5bc0be"

# ----------------- Contenu des scripts -----------------
INSTALL_SH = """#!/bin/bash
cd "$(dirname "$0")"

VENV_PYTHON="../../../.venv/bin/python"

if [ ! -f "$VENV_PYTHON" ]; then
    echo ".venv introuvable"
    exit 1
fi

"$VENV_PYTHON" -m pip install -r requirements.txt
"""

INSTALL_BAT = """@echo off
cd /d %~dp0

set VENV_PYTHON=..\\..\\..\\.venv\\Scripts\\python.exe

if not exist "%VENV_PYTHON%" (
    echo ERREUR : .venv introuvable
    exit /b 1
)

"%VENV_PYTHON%" -m pip install -r requirements.txt
"""

# ----------------- Fonctions utilitaires -----------------
def log(message):
    """Affiche les messages dans la console avec préfixe [TZ]"""
    print(f"[TZ] {message}")

# ----------------- Création de projet -----------------
def create_project():
    folder_name = entry.get().strip()
    log(f"Tentative de création du plugin : '{folder_name}'")
    
    if not folder_name:
        log("Erreur : le nom du dossier est vide")
        messagebox.showerror("Erreur", "Le nom du dossier ne peut pas être vide.")
        return
    
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    project_path = os.path.join(BASE_DIR, folder_name)
    
    if not os.path.exists(project_path):
        os.makedirs(project_path)
        log(f"Dossier créé : {project_path}")
    else:
        log(f"Attention : le dossier existe déjà : {project_path}")
        messagebox.showwarning("Attention", f"Le dossier '{folder_name}' existe déjà.")
    
    # Fichier principal Python
    py_file_path = os.path.join(project_path, f"{folder_name}.py")
    if not os.path.exists(py_file_path):
        with open(py_file_path, "w") as f:
            f.write("# Fichier principal du plugin\n")
        log(f"Fichier Python créé : {py_file_path}")
    
    # requirements.txt
    req_path = os.path.join(project_path, "requirements.txt")
    if not os.path.exists(req_path):
        open(req_path, "w").close()
        log("requirements.txt créé")
    
    # Scripts install
    sh_path = os.path.join(project_path, "install.sh")
    with open(sh_path, "w") as f:
        f.write(INSTALL_SH)
    log("install.sh créé")
    
    bat_path = os.path.join(project_path, "install.bat")
    with open(bat_path, "w") as f:
        f.write(INSTALL_BAT)
    log("install.bat créé")
    
    messagebox.showinfo("Succès", f"Le plugin '{folder_name}' a été créé dans '{BASE_DIR}' !")

# ----------------- Analyse et mise à jour requirements -----------------
def analyze_plugin_requirements():
    plugin_folder = filedialog.askdirectory(title="Sélectionner le dossier du plugin")
    if not plugin_folder:
        return
    
    log(f"Analyse des imports dans le dossier : {plugin_folder}")
    imports_set = set()
    
    for root_dir, _, files in os.walk(plugin_folder):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root_dir, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if line.startswith("import "):
                                parts = line.replace("import", "").split(",")
                                for part in parts:
                                    imports_set.add(part.strip().split(" ")[0])
                            elif line.startswith("from "):
                                parts = line.split()
                                if len(parts) >= 4 and parts[2] == "import":
                                    imports_set.add(parts[1])
                except Exception as e:
                    log(f"Erreur lecture {file_path}: {e}")
    
    if not imports_set:
        log("Aucun import détecté")
        messagebox.showinfo("Analyse terminée", "Aucun import détecté dans ce plugin.")
        return
    
    req_path = os.path.join(plugin_folder, "requirements.txt")
    if not os.path.exists(req_path):
        open(req_path, "w").close()
        log("requirements.txt créé")
    
    imports_list = "\n".join(sorted(imports_set))
    confirm = messagebox.askyesno(
        "Mise à jour requirements.txt",
        f"Modules détectés dans ce plugin :\n{imports_list}\n\nVoulez-vous mettre à jour le requirements.txt ?"
    )
    
    if confirm:
        with open(req_path, "r", encoding="utf-8") as f:
            existing_reqs = set(line.strip() for line in f if line.strip())
        all_reqs = existing_reqs.union(imports_set)
        with open(req_path, "w", encoding="utf-8") as f:
            for module in sorted(all_reqs):
                f.write(module + "\n")
        log(f"requirements.txt mis à jour avec {len(imports_set)} modules")
        messagebox.showinfo("Succès", f"requirements.txt mis à jour avec {len(imports_set)} modules.")
    else:
        log("Mise à jour requirements.txt annulée")
        messagebox.showinfo("Annulé", "Aucun module n'a été ajouté au requirements.txt.")

# ----------------- Interface -----------------
root = tk.Tk()
root.title("Créateur de plugin")
root.configure(bg=BG_COLOR)

# Label
label = tk.Label(root, text="Nom du plugin / dossier :", bg=BG_COLOR, fg=TEXT_COLOR)
label.pack(padx=10, pady=5)

# Entry
entry = tk.Entry(root, width=30, bg=BTN_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR)
entry.pack(padx=10, pady=5)

# Boutons avec hover
def on_enter(e):
    e.widget['bg'] = BTN_HOVER

def on_leave(e):
    e.widget['bg'] = BTN_COLOR

button_create = tk.Button(
    root,
    text="Créer le plugin",
    bg=BTN_COLOR,
    fg=TEXT_COLOR,
    activebackground=ACCENT,
    command=create_project
)
button_create.pack(padx=10, pady=10)
button_create.bind("<Enter>", on_enter)
button_create.bind("<Leave>", on_leave)

button_analyze = tk.Button(
    root,
    text="Analyser les imports et mettre à jour requirements",
    bg=BTN_COLOR,
    fg=TEXT_COLOR,
    activebackground=ACCENT,
    command=analyze_plugin_requirements
)
button_analyze.pack(padx=10, pady=5)
button_analyze.bind("<Enter>", on_enter)
button_analyze.bind("<Leave>", on_leave)

root.mainloop()
