import os
import tkinter as tk
from tkinter import messagebox, filedialog

# Contenu des fichiers install.sh et install.bat (inchangé)
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

# ----------------- Création de projet -----------------
def create_project():
    folder_name = entry.get().strip()
    if not folder_name:
        messagebox.showerror("Erreur", "Le nom du dossier ne peut pas être vide.")
        return
    
    # Dossier du plugin
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    project_path = os.path.join(BASE_DIR, folder_name)
    
    if not os.path.exists(project_path):
        os.makedirs(project_path)
    else:
        messagebox.showwarning("Attention", f"Le dossier '{folder_name}' existe déjà.")
    
    py_file_path = os.path.join(project_path, f"{folder_name}.py")
    if not os.path.exists(py_file_path):
        with open(py_file_path, "w") as f:
            f.write("# Fichier principal du plugin\n")
    
    req_path = os.path.join(project_path, "requirements.txt")
    if not os.path.exists(req_path):
        open(req_path, "w").close()
    
    sh_path = os.path.join(project_path, "install.sh")
    with open(sh_path, "w") as f:
        f.write(INSTALL_SH)
    
    bat_path = os.path.join(project_path, "install.bat")
    with open(bat_path, "w") as f:
        f.write(INSTALL_BAT)
    
    messagebox.showinfo("Succès", f"Le plugin '{folder_name}' a été créé dans '{BASE_DIR}' !")

# ----------------- Analyse et mise à jour requirements -----------------
def analyze_plugin_requirements():
    plugin_folder = filedialog.askdirectory(title="Sélectionner le dossier du plugin")
    if not plugin_folder:
        return
    
    imports_set = set()
    
    # Parcours tous les fichiers .py du dossier plugin
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
                    print(f"Erreur lecture {file_path}: {e}")
    
    if not imports_set:
        messagebox.showinfo("Analyse terminée", "Aucun import détecté dans ce plugin.")
        return
    
    req_path = os.path.join(plugin_folder, "requirements.txt")
    if not os.path.exists(req_path):
        open(req_path, "w").close()
    
    # Popup demandant confirmation
    imports_list = "\n".join(sorted(imports_set))
    confirm = messagebox.askyesno(
        "Mise à jour requirements.txt",
        f"Modules détectés dans ce plugin :\n{imports_list}\n\nVoulez-vous mettre à jour le requirements.txt ?"
    )
    
    if confirm:
        # Lire requirements existants
        with open(req_path, "r", encoding="utf-8") as f:
            existing_reqs = set(line.strip() for line in f if line.strip())
        # Ajouter sans doublons
        all_reqs = existing_reqs.union(imports_set)
        # Écrire dans requirements.txt
        with open(req_path, "w", encoding="utf-8") as f:
            for module in sorted(all_reqs):
                f.write(module + "\n")
        messagebox.showinfo("Succès", f"requirements.txt mis à jour avec {len(imports_set)} modules.")
    else:
        messagebox.showinfo("Annulé", "Aucun module n'a été ajouté au requirements.txt.")

# ----------------- Interface -----------------
root = tk.Tk()
root.title("Créateur de plugin")

label = tk.Label(root, text="Nom du plugin / dossier :")
label.pack(padx=10, pady=5)

entry = tk.Entry(root, width=30)
entry.pack(padx=10, pady=5)

button_create = tk.Button(root, text="Créer le plugin", command=create_project)
button_create.pack(padx=10, pady=10)

button_analyze = tk.Button(root, text="Analyser les imports et mettre à jour requirements", command=analyze_plugin_requirements)
button_analyze.pack(padx=10, pady=5)

root.mainloop()
