import tkinter as tk
import subprocess
import os
import sys
from tkinter import messagebox

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEST_VERSION_PATH = os.path.join(
    BASE_DIR,
    "test_programme",
    "test_version.py"
)

PLUGIN_MAKER_PATH = os.path.join(
    BASE_DIR,
    "test_programme",
    "plugin_maker.py"
)

def launch_test_version():
    if not os.path.exists(TEST_VERSION_PATH):
        messagebox.showerror(
            "Erreur",
            f"test_version.py introuvable :\n{TEST_VERSION_PATH}"
        )
        return

    subprocess.Popen([sys.executable, TEST_VERSION_PATH])

def launch_plugin_maker():
    if not os.path.exists(PLUGIN_MAKER_PATH):
        messagebox.showerror(
            "Erreur",
            f"plugin_maker.py introuvable :\n{PLUGIN_MAKER_PATH}"
        )
        return

    subprocess.Popen([sys.executable, PLUGIN_MAKER_PATH])

root = tk.Tk()
root.title("Test Zone")

tk.Button(
    root,
    text="Lancer le test de version",
    command=launch_test_version,
    width=35,
    height=2
).pack(padx=20, pady=(20, 10))

tk.Button(
    root,
    text="plugin maker",
    command=launch_plugin_maker,
    width=35,
    height=2
).pack(padx=20, pady=(10, 20))

root.mainloop()
