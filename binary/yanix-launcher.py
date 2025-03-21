import subprocess
import os
import tkinter as tk
from tkinter import messagebox, filedialog
import webbrowser
import pygame  # Adicionando pygame para tocar o som de startup
from playsound import playsound
import time

SEARCH_DIRS = [
    os.path.expanduser("~"),
    os.path.expanduser("~/Documents"),
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/.local/share")
]

def find_yanix_launcher():
    for directory in SEARCH_DIRS:
        possible_path = os.path.join(directory, "yanix-launcher")
        if os.path.exists(possible_path):
            return possible_path
    return None

def clone_yanix_launcher():
    home_dir = os.path.expanduser("~")
    target_path = os.path.join(home_dir, "yanix-launcher")
    subprocess.run(["git", "clone", "https://github.com/NikoYandere/Yanix-Launcher.git", target_path], check=True)
    script_path = os.path.abspath(__file__)
    os.remove(script_path)

YANIX_PATH = find_yanix_launcher()
if not YANIX_PATH:
    clone_yanix_launcher()
    exit()

CONFIG_PATH = os.path.join(YANIX_PATH, "binary/data/game_path.txt")
LANG_PATH = os.path.join(YANIX_PATH, "binary/data/multilang.txt")
VERSION_PATH = os.path.join(YANIX_PATH, "binary/data/version.txt")
GITHUB_REPO = "https://github.com/NikoYandere/Yanix-Launcher"
SUPPORT_URL = "https://github.com/NikoYandere/Yanix-Launcher/issues"
DISCORD_URL = "https://discord.gg/bRkXxcTFQM"
ICON_PATH = os.path.join(YANIX_PATH, "binary/data/Yanix-Launcher.png")
BG_PATH = os.path.join(YANIX_PATH, "binary/data/Background.png")
LANGUAGES = {
    "en": {"welcome": "Welcome to Yanix Launcher", "loading": "Loading", "play": "Play", "github": "GitHub", "settings": "Settings", "download": "Download Game", "select_language": "Select Language", "select_exe": "Select .exe for WINE", "support": "Support", "discord": "Discord", "lang_changed": "Language changed! Restart the launcher.", "exit": "Exit", "missing_path": "Uh oh, try extract in home folder"},
    "es": {"welcome": "Bienvenido a Yanix Launcher", "loading": "Cargando", "play": "Jugar", "github": "GitHub", "settings": "Configuración", "download": "Descargar Juego", "select_language": "Seleccionar Idioma", "select_exe": "Seleccionar .exe para WINE", "support": "Soporte", "discord": "Discord", "lang_changed": "¡Idioma cambiado! Reinicie el lanzador.", "exit": "Salir", "missing_path": "Uh oh, intenta extraerlo en tu carpeta personal"},
    "pt": {"welcome": "Bem-vindo ao Yanix Launcher", "loading": "Carregando", "play": "Jogar", "github": "GitHub", "settings": "Configurações", "download": "Baixar Jogo", "select_language": "Selecionar Idioma", "select_exe": "Selecionar .exe para WINE", "support": "Suporte", "discord": "Discord", "lang_changed": "Idioma alterado! Reinicie o lançador.", "exit": "Sair", "missing_path": "Uh oh... tente extrai-lo na sua pasta pessoal."}
}

def load_language():
    return open(LANG_PATH).read().strip() if os.path.exists(LANG_PATH) else "en"

def load_version():
    if os.path.exists(VERSION_PATH):
        with open(VERSION_PATH, 'r') as version_file:
            return version_file.read().strip()
    return "Unknown Version"

def open_support():
    webbrowser.open(SUPPORT_URL)

def open_discord():
    webbrowser.open(DISCORD_URL)

def launch_game():
    if os.path.exists(CONFIG_PATH):
        game_path = open(CONFIG_PATH).read().strip()
        if os.path.exists(game_path):
            # Esconde a janela do launcher
            top.withdraw()

            # Executa o Wine e espera terminar
            subprocess.run(["wine", game_path], check=True)
            
            # Restaura a janela após a execução do Wine
            top.deiconify()
            return
    messagebox.showerror("Error", "No valid executable selected!")

def open_github():
    webbrowser.open(GITHUB_REPO)

def open_settings():
    settings_window = tk.Toplevel(top)
    settings_window.title(LANGUAGES[current_lang]["settings"])
    settings_window.geometry("300x200")
    
    tk.Button(settings_window, text=LANGUAGES[current_lang]["select_language"], command=select_language).pack(pady=10)
    tk.Button(settings_window, text=LANGUAGES[current_lang]["select_exe"], command=select_exe).pack(pady=10)

def exit_launcher():
    top.quit()

def select_language():
    lang_window = tk.Toplevel(top)
    lang_window.title("Select Language")
    lang_window.geometry("200x150")
    
    def set_language(lang):
        with open(LANG_PATH, "w") as f:
            f.write(lang)
        messagebox.showinfo("Success", LANGUAGES[lang]["lang_changed"])
        lang_window.destroy()
    
    for lang in ["en", "es", "pt"]:
        tk.Button(lang_window, text=lang.upper(), command=lambda l=lang: set_language(l)).pack(pady=5)

def select_exe():
    file_path = filedialog.askopenfilename(title=LANGUAGES[current_lang]["select_exe"], filetypes=[["Executables", "*.exe"]])
    if file_path:
        with open(CONFIG_PATH, "w") as file:
            file.write(file_path)
        messagebox.showinfo("Success", "Executable saved!")

def show_buttons():
    welcome_label.destroy()
    loading_label.destroy()
    for button, pos in zip(buttons, [(0.5, 0.3), (0.5, 0.4), (0.5, 0.5), (0.5, 0.6), (0.5, 0.7)]):  
        button.place(relx=pos[0], rely=pos[1], anchor=tk.CENTER)
    
    exit_button.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

def animate_welcome(duration=4):  # Alterado para 7 segundos
    step_time = duration * 1000 // 40
    def update_text(step=0):
        if step < 40:
            dots = "." * (step % 4)
            loading_label.config(text=f"{LANGUAGES[current_lang]['loading']}{dots}")
            top.after(step_time, update_text, step + 1)
        else:
            show_buttons()
    update_text()

# Função para tocar o som de inicialização
def play_startup_sound():
    pygame.mixer.init()  # Inicializa o mixer do pygame
    sound_path = os.path.join(YANIX_PATH, "binary/data/startup.wav")
    if os.path.exists(sound_path):
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()

top = tk.Tk()
top.title("Yanix-Launcher")
top.geometry("400x600")
top.resizable(False, False)

if not os.path.exists(YANIX_PATH):
    messagebox.showerror("Error", LANGUAGES[load_language()]["missing_path"])
    top.destroy()
else:
    if os.path.exists(ICON_PATH):
        top.iconphoto(True, tk.PhotoImage(file=ICON_PATH))
    
    if os.path.exists(BG_PATH):
        bg_image = tk.PhotoImage(file=BG_PATH)
        bg_label = tk.Label(top, image=bg_image)
        bg_label.place(relwidth=1, relheight=1)
    
    current_lang = load_language()
    
    welcome_label = tk.Label(top, text=LANGUAGES[current_lang]["welcome"], font=("", 20, "normal"), bg="white")
    welcome_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    
    loading_label = tk.Label(top, text=LANGUAGES[current_lang]["loading"], font=("Futura", 14, "normal"), bg="white")
    loading_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    buttons = [
        tk.Button(top, text=LANGUAGES[current_lang]["play"], font=("Futura", 30, "normal"), command=launch_game),
        tk.Button(top, text=LANGUAGES[current_lang]["download"], font=("Futura", 10, "normal"), command=lambda: subprocess.run(["x-terminal-emulator", "-e", "sh", "-c", "cd yanix-launcher && wget https://yanderesimulator.com/dl/latest.zip"], check=True)),
        tk.Button(top, text=LANGUAGES[current_lang]["github"], font=("Futura", 10, "normal"), command=open_github),
        tk.Button(top, text=LANGUAGES[current_lang]["discord"], font=("Futura", 10, "normal"), command=open_discord),
        tk.Button(top, text=LANGUAGES[current_lang]["settings"], font=("Futura", 10, "normal"), command=open_settings)
    ]
    
    # Adicionando o botão de Exit
    exit_button = tk.Button(top, text=LANGUAGES[current_lang]["exit"], font=("Futura", 10, "normal"), command=exit_launcher)

    # Adicionando a versão no rodapé
    version_label = tk.Label(top, text=f"Version: {load_version()}", font=("Futura", 8), bg="white")
    version_label.place(relx=0.5, rely=0.95, anchor=tk.CENTER)

    play_startup_sound()  # Tocar o som de startup
    animate_welcome()  # Duração de 7 segundos para a animação
    top.mainloop()

