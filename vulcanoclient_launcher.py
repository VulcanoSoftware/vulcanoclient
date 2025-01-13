import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import os
import requests
from PIL import Image, ImageTk
import ctypes
import platform

def download_image():
    # URL van de afbeelding
    image_url = "https://www.dropbox.com/scl/fi/157ujxatwxkztlni2eog4/8d22d753007f68c48eea910386b79ab3.png?rlkey=bkspxpwq57t1ngzd7m72qm3gk&st=b5qeindq&dl=1"
    
    # Pad waar de afbeelding moet worden opgeslagen
    image_path = os.path.join(os.path.dirname(__file__), "banner.png")
    
    # Download alleen als de afbeelding nog niet bestaat
    if not os.path.exists(image_path):
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(image_path, 'wb') as f:
                f.write(response.content)
    return image_path

def run_as_admin():
    vulcanoclient_path = os.path.join(os.path.dirname(__file__), "versions", "1.21.1", "vulcanoclient_1.21.1.exe")
    
    if sys.platform == 'win32':  # Windows
        try:
            shell32 = ctypes.windll.shell32
            params = f'"{vulcanoclient_path}"'
            ret = shell32.ShellExecuteW(
                None, 
                "runas",
                vulcanoclient_path,  # Direct het .exe bestand uitvoeren ipv via python
                None,               # Geen extra parameters nodig
                os.path.dirname(vulcanoclient_path),
                7
            )
            if ret <= 32:
                raise Exception(f"ShellExecute failed with code {ret}")
        except Exception as e:
            print(f"Windows admin start fout: {e}")
            return False
            
    elif sys.platform == 'darwin':  # macOS
        try:
            cmd = [
                'osascript',
                '-e',
                f'do shell script "python3 \'{vulcanoclient_path}\'" with administrator privileges'
            ]
            subprocess.Popen(cmd)
        except Exception as e:
            print(f"macOS admin start fout: {e}")
            return False
            
    else:  # Linux
        try:
            # Probeer eerst pkexec (aanbevolen voor desktop omgevingen)
            if os.system('which pkexec >/dev/null 2>&1') == 0:
                subprocess.Popen(['pkexec', sys.executable, vulcanoclient_path])
            # Anders, probeer gksudo
            elif os.system('which gksudo >/dev/null 2>&1') == 0:
                subprocess.Popen(['gksudo', '--', sys.executable, vulcanoclient_path])
            # Als laatste optie, gebruik sudo
            else:
                subprocess.Popen(['sudo', sys.executable, vulcanoclient_path])
        except Exception as e:
            print(f"Linux admin start fout: {e}")
            return False
            
    return True

def start_vulcanoclient():
    # Probeer te starten met admin rechten
    success = run_as_admin()
    
    if not success:
        # Fallback: start zonder admin rechten
        try:
            subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "vulcanoclient.py")])
        except Exception as e:
            print(f"Fallback start fout: {e}")
    
    # Functie om op te ruimen en af te sluiten
    def cleanup_and_close():
        try:
            banner_path = os.path.join(os.path.dirname(__file__), "banner.png")
            if os.path.exists(banner_path):
                os.remove(banner_path)
        except Exception as e:
            print(f"Fout bij verwijderen banner: {e}")
        root.destroy()
    
    root.after(1, cleanup_and_close)

def cleanup_and_quit():
    # Verwijder de banner.png
    try:
        banner_path = os.path.join(os.path.dirname(__file__), "banner.png")
        if os.path.exists(banner_path):
            os.remove(banner_path)
    except Exception as e:
        print(f"Fout bij verwijderen banner: {e}")
    
    # Sluit het programma
    root.destroy()

# Download de afbeelding voordat het programma start
banner_path = download_image()

# Maak hoofdvenster
root = tk.Tk()
root.title("VulcanoClient Launcher")
root.configure(bg="white")  # Hoofdvenster wit maken

# Koppel het kruisje aan dezelfde cleanup functie
root.protocol("WM_DELETE_WINDOW", cleanup_and_quit)

# Stel venstergrootte en positie in
window_width = 600
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width // 2) - (window_width // 2)
y_position = screen_height - window_height - 100
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Maak een hoofdframe met scrollbar
main_frame = tk.Frame(root, bg="white", highlightthickness=0)
main_frame.pack(fill=tk.BOTH, expand=1)

# Maak een canvas
canvas = tk.Canvas(main_frame, bg="white", highlightthickness=0)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Voeg scrollbar toe
scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configureer canvas
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Maak een tweede frame binnen de canvas
content_frame = tk.Frame(canvas, bg="white", highlightthickness=0)
canvas.create_window((0, 0), window=content_frame, anchor="nw", width=window_width-20)

# Voeg titel label toe met witte achtergrond
tk.Label(content_frame, 
         text="VulcanoClient Launcher", 
         font=("Arial", 20), 
         bg="white").pack(pady=20)

# Daarna de banner afbeelding
try:
    banner_image = Image.open(banner_path)
    banner_image = banner_image.resize((250, 250))
    banner_photo = ImageTk.PhotoImage(banner_image)
    banner_label = tk.Label(content_frame, image=banner_photo)
    banner_label.image = banner_photo
    banner_label.pack(pady=10)
except Exception as e:
    print(f"Fout bij laden van banner: {e}")

# Configureer de stijl
style = ttk.Style()
style.configure("TButton",
                background="#4CAF50",
                foreground="black",
                relief="flat",
                borderwidth=5,
                focusthickness=0,
                font=("Arial", 20))

style.map("TButton",
          background=[('active', '#45a049'), ('!active', '#4CAF50')])

# Start knop
version_button = ttk.Button(
    content_frame,
    text="Start VulcanoClient v1.21.1",
    command=start_vulcanoclient,
    style="TButton"
)
version_button.pack(pady=20)

# Afsluiten knop
close_button = ttk.Button(
    content_frame,
    text="Afsluiten",
    command=cleanup_and_quit,
    style="TButton"
)
close_button.pack(pady=10)

# Voeg muiswiel scrolling toe
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
canvas.bind_all("<MouseWheel>", _on_mousewheel)

# Start de GUI
root.mainloop()