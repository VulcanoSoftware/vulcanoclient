import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
import requests
from PIL import Image, ImageTk
import ctypes
import platform
import time
import threading
import pygame

class InfiniteProgressWindow:
    def __init__(self):
        self.stop_event = None
        self.thread = None

    def start(self):
        """Start de voortgangsbalk in een aparte thread."""
        if self.thread is None or not self.thread.is_alive():
            self.stop_event = threading.Event()  # Maak een nieuwe stop-event
            self.thread = threading.Thread(target=self._create_window, daemon=True)
            self.thread.start()
            print("Voortgangsbalk gestart.")
        else:
            print("Voortgangsbalk is al actief.")

    def stop(self):
        """Stop de voortgangsbalk en sluit het venster."""
        if self.thread is not None and self.thread.is_alive():
            self.stop_event.set()  # Zet het stop-event
            self.thread.join()  # Wacht tot de thread is gestopt
            self.thread = None  # Reset de thread
            print("Voortgangsbalk gestopt.")
        else:
            print("Voortgangsbalk is niet actief.")

    def _create_window(self):
        """Maak en beheer het venster in een aparte thread."""
        pygame.init()

        # Creëer een scherm voor de voortgangsbalk
        screen = pygame.display.set_mode((500, 50))  # Venster met standaard vensterbalk
        pygame.display.set_caption("VulcanoClient wordt gestart ... ")

        # Kleurdefinities (stijl geïnspireerd op Windows 7)
        background_color = (240, 240, 240)  # Lichtgrijze achtergrond
        block_color = (0, 120, 215)  # Windows 7 blauw
        highlight_color = (173, 216, 230)  # Lichtblauwe highlight

        # Afmetingen van het bewegende blok
        block_width = 100
        block_height = 30
        block_x = 0  # Startpositie
        block_y = (screen.get_height() - block_height) // 2

        # Variabele voor snelheid van het blok
        speed = 5

        # Hoofdloop voor het scherm
        while not self.stop_event.is_set():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Negeer de sluitgebeurtenis
                    print("Sluiten van het venster is geblokkeerd.")
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # Optioneel: ESC-toets kan worden gebruikt om het venster te stoppen
                    print("ESC-toets ingedrukt, venster wordt gestopt.")
                    self.stop_event.set()

            # Scherm verversen
            screen.fill(background_color)

            # Teken de achtergrondbalk (Windows 7 stijl met lichte gradient)
            pygame.draw.rect(screen, highlight_color, (0, block_y, screen.get_width(), block_height))

            # Teken het bewegende blok
            pygame.draw.rect(screen, block_color, (block_x, block_y, block_width, block_height))

            # Update de positie van het blok
            block_x += speed
            if block_x > screen.get_width():
                block_x = -block_width  # Laat het blok opnieuw beginnen van links

            # Update het scherm
            pygame.display.flip()

            # Wacht even voor de volgende update
            time.sleep(0.03)

        pygame.quit()

def is_admin():
    try:
        if platform.system() == 'Windows':
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:
            return os.getuid() == 0  # 0 is root/admin op Unix systemen
    except:
        return False

# Controleer admin rechten direct na imports
if not is_admin():
    root = tk.Tk()
    root.withdraw()  # Verberg het hoofdvenster
    messagebox.showerror("Fout", "Dit programma kan enkel worden uitgevoerd door een administrator")
    sys.exit(1)

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
    # Controleer en maak de versions map aan indien nodig
    versions_path = os.path.join(os.path.dirname(__file__), "versions")
    version_specific_path = os.path.join(versions_path, "1.21.1")
    
    # Maak de mappen aan als ze niet bestaan
    os.makedirs(version_specific_path, exist_ok=True)
    
    vulcanoclient_path = os.path.join(version_specific_path, "vulcanoclient_1.21.1.exe")
    
    # Controleer of het executable bestand bestaat
    if not os.path.exists(vulcanoclient_path):
        print(f"Waarschuwing: VulcanoClient executable niet gevonden in: {vulcanoclient_path}")
        return False
        
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
    # Controleer en download/start versie 1.21.1
    executable_path = os.path.join(os.path.dirname(__file__), "versions/1.21.1/vulcanoclient_1.21.1.exe")
    
    if not os.path.exists(executable_path):
        print("VulcanoClient wordt gedownload...")
        if download_version_1_21_1():
            print("Download voltooid!")
        else:
            print("Download mislukt!")
            return
    
    # Probeer te starten met admin rechten
    success = run_as_admin()
    
    if not success:
        # Fallback: start zonder admin rechten
        try:
            subprocess.Popen([executable_path])
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

def download_version_1_21_1():
    """Download versie 1.21.1 van de VulcanoClient"""
    url = "https://github.com/VulcanoSoftware/vulcanoclient/releases/download/1.6/vulcanoclient_1.21.1.exe"
    local_path = "versions/1.21.1/vulcanoclient_1.21.1.exe"
    
    # Maak een instantie van de voortgangsbalk
    progress_window = InfiniteProgressWindow()
    progress_window.start()
    
    # Maak de directory structuur aan als deze nog niet bestaat
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Controleer op HTTP fouten
        
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Stop de voortgangsbalk
        progress_window.stop()
        
        # Start de client direct na succesvolle download
        success = run_as_admin()
        if not success:
            # Fallback: probeer zonder admin rechten te starten
            try:
                subprocess.Popen([local_path])
            except Exception as e:
                print(f"Fout bij het starten na download: {e}")
                return False
        return True
    except Exception as e:
        # Stop de voortgangsbalk ook bij een fout
        progress_window.stop()
        print(f"Fout bij het downloaden: {e}")
        return False

def launch_1_21_1():
    """Start versie 1.21.1 van de VulcanoClient"""
    executable_path = "versions/1.21.1/vulcanoclient_1.21.1.exe"
    
    if not os.path.exists(executable_path):
        print("Versie 1.21.1 wordt gedownload...")
        if download_version_1_21_1():
            print("Download voltooid!")
        else:
            print("Download mislukt!")
            return
    
    try:
        subprocess.Popen(executable_path)
    except Exception as e:
        print(f"Fout bij het starten: {e}")

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
