import os
import platform
import subprocess
import tkinter as tk
from tkinter import messagebox, Toplevel, Label, PhotoImage, Canvas, Scrollbar, Frame
from tkinter import ttk
import urllib.request
import shutil
import requests
import zipfile
from io import BytesIO
import ctypes
import sys
from PIL import Image, ImageTk
import time
import threading
from queue import Queue
import psutil
import pygame
import signal
import webbrowser
import ssl

class InfiniteProgressWindow:
    def __init__(self):
        self.stop_event = None
        self.thread = None

    def start(self):
        if self.thread is None or not self.thread.is_alive():
            self.stop_event = threading.Event()
            self.thread = threading.Thread(target=self._create_window, daemon=True)
            self.thread.start()
            print("Voortgangsbalk gestart.")
        else:
            print("Voortgangsbalk is al actief.")

    def stop(self):
        if self.thread is not None and self.thread.is_alive():
            self.stop_event.set()
            self.thread.join()
            self.thread = None
            print("Voortgangsbalk gestopt.")
        else:
            print("Voortgangsbalk is niet actief.")

    def _create_window(self):
        pygame.init()

        screen = pygame.display.set_mode((500, 50))
        pygame.display.set_caption("VulcanoClient wordt gestart ... ")

        background_color = (240, 240, 240)
        block_color = (0, 120, 215)
        highlight_color = (173, 216, 230)

        block_width = 100
        block_height = 30
        block_x = 0
        block_y = (screen.get_height() - block_height) // 2

        speed = 5

        while not self.stop_event.is_set():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Sluiten van het venster is geblokkeerd.")
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    print("ESC-toets ingedrukt, venster wordt gestopt.")
                    self.stop_event.set()

            screen.fill(background_color)

            pygame.draw.rect(screen, highlight_color, (0, block_y, screen.get_width(), block_height))

            pygame.draw.rect(screen, block_color, (block_x, block_y, block_width, block_height))

            block_x += speed
            if block_x > screen.get_width():
                block_x = -block_width

            pygame.display.flip()

            time.sleep(0.03)

        pygame.quit()

class ChocoLoader:
    def __init__(self):
        self._choco_process = None

    def get_resource_path_choco_win(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def download_choco_loader(self):
        return True

    def start_choco_loadingpg_win(self):
        if sys.platform != 'win32':
            print("Choco loader is alleen beschikbaar voor Windows")
            return
            
        if self._choco_process is None:
            try:
                choco_exe = self.get_resource_path_choco_win('choco_loading.exe')
                self._choco_process = subprocess.Popen([choco_exe])
                print("Choco loading proces gestart")
            except Exception as e:
                print(f"Fout bij het starten van choco_loading.exe: {e}")
        else:
            print("Choco loading proces draait al")

    def stop_choco_loadingpg_win(self):
        if self._choco_process is not None:
            try:
                parent = psutil.Process(self._choco_process.pid)
                children = parent.children(recursive=True)
                
                for child in children:
                    try:
                        child.kill()
                    except psutil.NoSuchProcess:
                        pass
                        
                if sys.platform == 'win32':
                    self._choco_process.kill()
                else:
                    self._choco_process.send_signal(signal.SIGKILL)
                    
                psutil.wait_procs(children, timeout=3)
                self._choco_process.wait(timeout=3)
                
                self._choco_process = None
                print("Choco loading proces en alle subprocessen gestopt")
            except Exception as e:
                print(f"Fout bij het stoppen van choco_loading.exe: {e}")
                try:
                    self._choco_process.kill()
                    self._choco_process = None
                except:
                    pass
        else:
            print("Geen actief choco loading proces gevonden")

class JavaLoader:
    def __init__(self):
        self._java_process = None

    def get_resource_path_java_win(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def download_java_loader(self):
        return True

    def start_java_loadingpg_win(self):
        if sys.platform != 'win32':
            print("Java loader is alleen beschikbaar voor Windows")
            return
            
        if self._java_process is None:
            try:
                java_exe = self.get_resource_path_java_win('java_loading.exe')
                self._java_process = subprocess.Popen([java_exe])
                print("Java loading proces gestart")
            except Exception as e:
                print(f"Fout bij het starten van java_loading.exe: {e}")
        else:
            print("Java loading proces draait al")

    def stop_java_loadingpg_win(self):
        if self._java_process is not None:
            try:
                parent = psutil.Process(self._java_process.pid)
                children = parent.children(recursive=True)
                
                for child in children:
                    try:
                        child.kill()
                    except psutil.NoSuchProcess:
                        pass
                        
                if sys.platform == 'win32':
                    self._java_process.kill()
                else:
                    self._java_process.send_signal(signal.SIGKILL)
                    
                psutil.wait_procs(children, timeout=3)
                self._java_process.wait(timeout=3)
                
                self._java_process = None
                print("Java loading proces en alle subprocessen gestopt")
            except Exception as e:
                print(f"Fout bij het stoppen van java_loading.exe: {e}")
                try:
                    self._java_process.kill()
                    self._java_process = None
                except:
                    pass
        else:
            print("Geen actief java loading proces gevonden")

FABRIC_INSTALLER_URL = "https://github.com/VulcanoSoftware/vulcanoclient/raw/refs/heads/main/fabric-installer-0.11.2.jar"

URL_CLIENT = "https://github.com/VulcanoSoftware/vulcanoclient/releases/download/1.6/vulcanoclient.zip"

lunar_vulcanoclient_url = "https://github.com/VulcanoSoftware/vulcanoclient/releases/download/1.6/vulcanoclient_lunar.zip"

IMAGE_URLS = {
    "step2": "https://www.dropbox.com/scl/fi/dqqdkg9szyunwpqm0jalv/step2.png?rlkey=0gkoxa2tcvsh1np6uo6lspu5r&st=2t5rirs5&dl=1",
    "step3": "https://www.dropbox.com/scl/fi/31yvorfga25deggv19c8n/step3.png?rlkey=71c3nc5mnk59otnmzx5f2flpp&st=4torqxn8&dl=1",
    "step4": "https://www.dropbox.com/scl/fi/4cobagvk6v2gjj6p00hxu/step4.png?rlkey=34lx0wntdcb4jc1u2ldqnern8&st=ku5rp7dr&dl=1",
    "step2_mc": "https://www.dropbox.com/scl/fi/aa7yrqozvf5rj0p249ppx/step2_mc.png?rlkey=re6l7ctybklev8ibk0hvyzncy&st=03dscwik&dl=1",
    "step3_mc": "https://www.dropbox.com/scl/fi/2dlgpejy71fxj1rhri7pl/step3_mc.png?rlkey=y3xrc1k35vtob794r2tgtkta0&st=jzjyp79l&dl=1",
    "example_image": "https://www.dropbox.com/scl/fi/157ujxatwxkztlni2eog4/8d22d753007f68c48eea910386b79ab3.png?rlkey=bkspxpwq57t1ngzd7m72qm3gk&st=b5qeindq&dl=1",
    "step1_lunar": "https://www.dropbox.com/scl/fi/f4dek84e3tvm9yonojvk1/step1_lunar.png?rlkey=atuct9d9g4688e7vrqheilmde&st=umvf44z5&dl=1",
    "step2_lunar": "https://www.dropbox.com/scl/fi/c9lln24pgtmzncmses7mg/step2_lunar.png?rlkey=b6bkjfzyml7lct2x5hzwhyofs&st=t5jtbks7&dl=1",
    "step3_lunar": "https://www.dropbox.com/scl/fi/2xxoirttlzmfl0yd7wriw/step3_lunar.png?rlkey=zvonzwmbv6qoz2yymvoe0rsgj&st=z1xt2lvw&dl=1",
    "step4_lunar": "https://www.dropbox.com/scl/fi/uc06daqgagpbj6sjz9usl/step4_lunar.png?rlkey=a26lgnlzt4jznltyex1jn46we&st=q9wa88hv&dl=1",
    "step5_lunar": "https://www.dropbox.com/scl/fi/lrb53ezi4tq4g2e4dqu2v/step5_lunar.png?rlkey=19z6ffcws5dzse8srsudoai5u&st=iu4uxdhi&dl=1",
    "step6_lunar": "https://www.dropbox.com/scl/fi/1thidh1126htl0o7full8/step6_lunar.png?rlkey=8mop2plmtg8s5zcar1jhx48s1&st=xag1f74y&dl=1",
    "step7_lunar": "https://www.dropbox.com/scl/fi/7r58it8b8qxhmkksiyv2r/step7_lunar.png?rlkey=o6cvqsb5lf9ukzujeiqspxoc0&st=asml51d6&dl=1"
}

def kill_lunar_client():
    os_name = platform.system()
    
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            proc_name = proc.info['name'].lower()
            
            lunar_processes = {
                "Windows": ['lunar client.exe', 'javaw.exe'],
                "Darwin": ['LunarClient', 'java'],
                "Linux": ['lunarclient', 'java']
            }.get(os_name, [])
            
            if any(name in proc_name for name in lunar_processes):
                if 'java' in proc_name:
                    cmdline = proc.cmdline()
                    if not any('lunar' in cmd.lower() for cmd in cmdline):
                        continue
                proc.kill()
                print(f"Proces beëindigd: {proc_name}")
                
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

def create_progress_window(title, maximum=100):
    def create_window():
        nonlocal progress_window, progress_bar, label, console
        progress_window = Toplevel()
        progress_window.title(title)
        window_width = 500
        window_height = 400
        screen_width = progress_window.winfo_screenwidth()
        screen_height = progress_window.winfo_screenheight()
        x_position = (screen_width // 2) - (window_width // 2)
        y_position = (screen_height // 2) - (window_height // 2)
        progress_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        
        label = ttk.Label(progress_window, text="Even geduld...")
        label.pack(pady=10)
        
        progress_bar = ttk.Progressbar(progress_window, length=400, mode='determinate', maximum=maximum)
        progress_bar.pack(pady=10)
        
        console_frame = ttk.Frame(progress_window)
        console_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(console_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        console = tk.Text(console_frame, height=15, width=50, yscrollcommand=scrollbar.set)
        console.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=console.yview)

    progress_window = None
    progress_bar = None
    label = None
    console = None
    
    root.after(0, create_window)
    
    while progress_window is None:
        root.update()
    
    return progress_window, progress_bar, label, console

def update_progress(progress_bar, label, value, text=None, console=None, console_text=None):
    def do_update():
        progress_bar['value'] = value
        if text:
            label['text'] = text
        if console and console_text:
            console.insert(tk.END, console_text + "\n")
            console.see(tk.END)
        progress_bar.update()
    
    root.after(0, do_update)
    root.update()

def is_choco_installed():
    try:
        choco_paths = [
            os.path.join(os.environ.get('ProgramData', ''), 'chocolatey', 'bin', 'choco.exe'),
            os.path.join(os.environ.get('ChocolateyInstall', ''), 'bin', 'choco.exe'),
        ]
        
        for choco_path in choco_paths:
            if os.path.exists(choco_path):
                return True
        return False
    except Exception:
        return False

def install_choco():
    try:
        cloader = ChocoLoader()
        cloader.start_choco_loadingpg_win()
        print("choco maken")
        install_command = """
        Set-ExecutionPolicy Bypass -Scope Process -Force;
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072;
        iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        """
        
        subprocess.run([
            'powershell.exe',
            '-NoProfile',
            '-ExecutionPolicy', 'Bypass',
            '-Command', install_command
        ], check=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        time.sleep(2)
        
        os.environ['PATH'] = os.pathsep.join([
            os.environ['PATH'],
            os.path.join(os.environ.get('ProgramData', ''), 'chocolatey', 'bin')
        ])
        
        cloader.stop_choco_loadingpg_win()
        time.sleep(2)
        return True
    except Exception as e:
        print(f"Fout bij installeren van Chocolatey: {e}")
        return False

def ensure_choco_installed():
    if not is_choco_installed():
        print("Chocolatey is niet geïnstalleerd. Bezig met installeren...")
        if install_choco():
            print("Chocolatey is succesvol geïnstalleerd!")
            if install_ffmpeg():
                print("FFmpeg is succesvol geïnstalleerd!")
                return True
            else:
                print("Fout bij het installeren van FFmpeg")
                return False
        else:
            print("Fout bij het installeren van Chocolatey")
            return False
    else:
        if install_ffmpeg():
            print("FFmpeg is succesvol geïnstalleerd!")
            return True
        else:
            print("Fout bij het installeren van FFmpeg")
            return False
    return True

def install_ffmpeg():  
    print("FFmpeg wordt geïnstalleerd...")
    try:
        subprocess.run(['choco', 'install', 'ffmpeg', '-y', '--no-progress'], 
                      check=True, 
                      creationflags=subprocess.CREATE_NO_WINDOW)
        print("FFmpeg is succesvol geïnstalleerd!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Er is een fout opgetreden bij het installeren van FFmpeg: {e}")
        return False
    except FileNotFoundError:
        print("Chocolatey is niet geïnstalleerd. Zorg ervoor dat Chocolatey eerst is geïnstalleerd.")
        return False

def java_install():
    if not ensure_choco_installed():
        messagebox.showerror("Fout", "Kon Chocolatey niet installeren. Java installatie kan niet doorgaan.")
        return

    def is_java_installed():
        try:
            java_path = subprocess.run(['which', 'java'], stdout=subprocess.PIPE, stderr=subprocess.PIPE) if platform.system() != 'Windows' else subprocess.run(['where', 'java'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return java_path.returncode == 0
        except Exception as e:
            print(f"Fout bij het controleren van Java-installatie: {e}")
            return False

    def install_java_windows():
        try:
            jloader = JavaLoader()
            jloader.start_java_loadingpg_win()
            subprocess.run(['choco', 'install', 'openjdk', '--version=21', '-y'], 
                          check=True,
                          creationflags=subprocess.CREATE_NO_WINDOW)
            print("Java 21 is succesvol geïnstalleerd op Windows.")
            jloader.stop_java_loadingpg_win()
            time.sleep(2)
        except subprocess.CalledProcessError as e:
            print(f"Fout bij het installeren van Java 21 op Windows: {e}")
            sys.exit(1)

    def install_java_linux():
        try:
            subprocess.run(['sudo', 'apt', 'update'], check=True)  
            subprocess.run(['sudo', 'apt', 'install', 'openjdk-21-jdk', '-y'], check=True)
            print("Java 21 is succesvol geïnstalleerd op Linux.")
        except subprocess.CalledProcessError as e:
            print(f"Fout bij het installeren van Java 21 op Linux: {e}")
            sys.exit(1)

    def install_homebrew_macos():
        try:
            subprocess.run(['/bin/bash', '-c', 
                            "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"], 
                            check=True)
            print("Homebrew is succesvol geïnstalleerd op macOS.")
        except subprocess.CalledProcessError as e:
            print(f"Fout bij het installeren van Homebrew: {e}")
            sys.exit(1)

    def install_java_macos():
        try:
            subprocess.run(['brew', 'install', 'openjdk@21'], check=True)
            print("Java 21 is succesvol geïnstalleerd op macOS.")
        
            print("Java 21 wordt toegevoegd aan de PATH...")
            subprocess.run(['sudo', 'ln', '-s', '/usr/local/opt/openjdk@21/bin/java', '/usr/local/bin/java'], check=True)
            subprocess.run(['sudo', 'ln', '-s', '/usr/local/opt/openjdk@21/bin/javac', '/usr/local/bin/javac'], check=True)
            
            shell_config = os.path.expanduser("~/.zshrc") if os.path.exists(os.path.expanduser("~/.zshrc")) else os.path.expanduser("~/.bash_profile")
            with open(shell_config, 'a') as f:
                f.write(f'\n# Homebrew Java 21\nexport PATH="/usr/local/opt/openjdk@21/bin:$PATH"\n')
            
            print("Java 21 is succesvol toegevoegd aan de PATH.")
            
        except subprocess.CalledProcessError as e:
            print(f"Fout bij het installeren van Java 21 op macOS: {e}")
            sys.exit(1)


    def main():
        os_platform = platform.system()

        if platform.system() == 'Windows':
            if ctypes.windll.shell32.IsUserAnAdmin():
                print("Het script wordt uitgevoerd als administrator op Windows.")
            else:
                print("\n!!! WAARSCHUWING !!!")
                print("Het script wordt niet uitgevoerd als administrator op Windows.")
                response = messagebox.askokcancel("Waarschuwing", 
                    "Het script wordt niet uitgevoerd als administrator op Windows.\n\n"
                    "Dit kan problemen veroorzaken bij de installatie.\n"
                    "Het wordt STERK AANGERADEN om het script als administrator uit te voeren.\n\n"
                    "Wil je toch doorgaan zonder administrator rechten?")
                if not response:
                    print("Installatie afgebroken. Start het programma opnieuw als administrator.")
                    sys.exit(1)
        
        elif platform.system() in ['Linux', 'Darwin']:
            if os.geteuid() == 0:
                print("Het script wordt uitgevoerd als root op Linux/macOS.")
            else:
                print("\n!!! WAARSCHUWING !!!")
                print("Het script wordt niet uitgevoerd als root op Linux/macOS.")
                response = messagebox.askokcancel("Waarschuwing",
                    "Het script wordt niet uitgevoerd als root op Linux/macOS.\n\n"
                    "Dit kan problemen veroorzaken bij de installatie.\n"
                    "Het wordt STERK AANGERADEN om het script als root uit te voeren.\n\n"
                    "Wil je toch doorgaan zonder root rechten?")
                if not response:
                    print("Installatie afgebroken. Start het programma opnieuw met sudo.")
                    sys.exit(1)
        
        if not is_java_installed():
            print("Java 21 is nog niet geïnstalleerd.")

            if os_platform == 'Windows':
                install_java_windows()
            
            elif os_platform == 'Linux':
                install_java_linux()
            
            elif os_platform == 'Darwin':  
                if not os.path.exists('/opt/homebrew/bin/brew') and not os.path.exists('/usr/local/bin/brew'):
                    print("Homebrew is nog niet geïnstalleerd. Dit zal nu gebeuren...")
                    install_homebrew_macos()
                install_java_macos()
            
            else:
                print(f"Onbekend besturingssysteem: {os_platform}")
                sys.exit(1)

        else:
            print("Java 21 is al geïnstalleerd.")

    if __name__ == "__main__":
        if platform.system() == "Darwin":
            messagebox.showinfo("Niet ondersteund", "You are using mac? fr? just don't be a poor apple fan and just use windows. you can use this program when you have windows")
            sys.exit()
        main()
        
java_install()

def detect_os():
    return platform.system()


def get_minecraft_directory(launcher):
    os_name = platform.system()
    home = os.path.expanduser("~")
    
    paths = {
        "Windows": {
            "Minecraft": os.path.join(os.getenv('APPDATA'), '.minecraft'),
            "TLauncher": os.path.join(os.getenv('APPDATA'), '.minecraft'),
            "Lunar": os.path.join(home, '.lunarclient')
        },
        "Darwin": {
            "Minecraft": os.path.join(home, 'Library', 'Application Support', 'minecraft'),
            "TLauncher": os.path.join(home, 'Library', 'Application Support', '.minecraft'),
            "Lunar": os.path.join(home, '.lunarclient')
        },
        "Linux": {
            "Minecraft": os.path.join(home, '.minecraft'),
            "TLauncher": os.path.join(home, '.minecraft'),
            "Lunar": os.path.join(home, '.lunarclient')
        }
    }
    
    return paths.get(os_name, {}).get(launcher)

def download_fabric_installer():
    try:
        installer_path = os.path.join(os.getcwd(), "fabric-installer.jar")
        urllib.request.urlretrieve(FABRIC_INSTALLER_URL, installer_path)
        return installer_path
    except Exception as e:
        messagebox.showerror("Fout", f"Kon de Fabric-installer niet downloaden: {e}")
        return None

def download_images():
    if platform.system() == "Darwin":
        ssl._create_default_https_context = ssl._create_unverified_context
    
    for key, url in IMAGE_URLS.items():
        local_path = os.path.join(os.getcwd(), f"{key}.png")
        
        if not os.path.exists(local_path):
            try:
                urllib.request.urlretrieve(url, local_path)
                IMAGE_URLS[key] = local_path 
            except Exception as e:
                print(f"Afbeelding {key} kon niet worden gedownload: {e}")
        else:
            IMAGE_URLS[key] = local_path 

def show_tlauncher_instructions():
    instructions_window = Toplevel()
    instructions_window.title("Instructies voor TLauncher")
    window_width = 820 
    window_height = 600 
    screen_width = instructions_window.winfo_screenwidth()
    screen_height = instructions_window.winfo_screenheight()

    if window_height + 20 > screen_height:
        window_height = screen_height - 20 

    x_position = (screen_width // 2) - (window_width // 2)

    y_position = screen_height - window_height - 100

    instructions_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    canvas = Canvas(instructions_window)
    scrollbar = Scrollbar(instructions_window, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def on_mouse_wheel(event):
        if event.num == 5 or event.delta < 0:
            canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            canvas.yview_scroll(-1, "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)  
    canvas.bind_all("<Button-4>", on_mouse_wheel)  
    canvas.bind_all("<Button-5>", on_mouse_wheel)  

    tk.Label(scrollable_frame, text="Volg de onderstaande stappen om Fabric te installeren in TLauncher:", wraplength=400, justify="left", font=("Arial", 20)).pack(pady=10)

    steps = [
        ("1. Open TLauncher\n", None),
        ("2. Geef je nickname in\n", IMAGE_URLS.get("step2")),
        ("3. Selecteer bij versies Fabric 1.21.1\n", IMAGE_URLS.get("step3")),
        ("4. Klik op spelen\n", IMAGE_URLS.get("step4")),
        ("5. Veel plezier\n", None)
    ]

    for step in steps:
        step_text, image_file = step
        tk.Label(scrollable_frame, text=step_text, wraplength=400, justify="left", font=("Arial", 20)).pack(pady=5)
        if image_file:
            try:
                pil_image = Image.open(image_file)
                img_width, img_height = pil_image.size
                scale_factor = min(800/img_width, 600/img_height)
                new_width = int(img_width * scale_factor)
                new_height = int(img_height * scale_factor)
                
                pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(pil_image)
                
                img_label = Label(scrollable_frame, image=img)
                img_label.image = img
                img_label.pack(pady=5)
                img_label.pack(anchor="center")
            except Exception as e:
                tk.Label(scrollable_frame, text=f"Afbeelding kon niet worden geladen: {image_file}", font=("Arial", 20)).pack(pady=5)

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

    ttk.Button(scrollable_frame, text="Sluiten", command=instructions_window.destroy, style="TButton").pack(pady=10)


def show_lunar_instructions():
    instructions_window = Toplevel()
    instructions_window.title("Instructies voor Lunar Client")
    window_width = 820 
    window_height = 600 
    screen_width = instructions_window.winfo_screenwidth()
    screen_height = instructions_window.winfo_screenheight()

    if window_height + 20 > screen_height:
        window_height = screen_height - 20 

    x_position = (screen_width // 2) - (window_width // 2)

    y_position = screen_height - window_height - 100

    instructions_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    canvas = Canvas(instructions_window)
    scrollbar = Scrollbar(instructions_window, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def on_mouse_wheel(event):
        if event.num == 5 or event.delta < 0:
            canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            canvas.yview_scroll(-1, "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)  
    canvas.bind_all("<Button-4>", on_mouse_wheel)  
    canvas.bind_all("<Button-5>", on_mouse_wheel)  

    tk.Label(scrollable_frame, text="Volg de onderstaande stappen om Fabric te installeren in TLauncher:", wraplength=400, justify="left", font=("Arial", 20)).pack(pady=10)

    steps = [
        ("1. Open Lunar Client\n", None),
        ("2. Klik op accept all purposes\n", IMAGE_URLS.get("step1_lunar")),
        ("3. Klik op 'click to login'\n", IMAGE_URLS.get("step2_lunar")),
        ("4. Log hier in met je microsoft account waar je minecraft account op staat\n", IMAGE_URLS.get("step3_lunar")),
        ("5. Klik op het pijltje\n", IMAGE_URLS.get("step4_lunar")),
        ("6. Verander hier de versie naar 1.21.1\n", IMAGE_URLS.get("step5_lunar")),
        ("7. Klik hier op 'lunar + fabric'\n", IMAGE_URLS.get("step6_lunar")),
        ("8. Klik op 'launch game'\n", IMAGE_URLS.get("step7_lunar")),
        ("9. Veel plezier\n", None)
    ]

    for step in steps:
        step_text, image_file = step
        tk.Label(scrollable_frame, text=step_text, wraplength=400, justify="left", font=("Arial", 20)).pack(pady=5)
        if image_file:
            try:
                pil_image = Image.open(image_file)
                img_width, img_height = pil_image.size
                scale_factor = min(800/img_width, 600/img_height)
                new_width = int(img_width * scale_factor)
                new_height = int(img_height * scale_factor)
                
                pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(pil_image)
                
                img_label = Label(scrollable_frame, image=img)
                img_label.image = img
                img_label.pack(pady=5)
                img_label.pack(anchor="center")
            except Exception as e:
                tk.Label(scrollable_frame, text=f"Afbeelding kon niet worden geladen: {image_file}", font=("Arial", 20)).pack(pady=5)

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

    ttk.Button(scrollable_frame, text="Sluiten", command=instructions_window.destroy, style="TButton").pack(pady=10)


def show_minecraft_instructions():
    instructions_window = Toplevel()
    instructions_window.title("Instructies voor Minecraft")
    window_width = 1000 
    window_height = 600 
    screen_width = instructions_window.winfo_screenwidth()
    screen_height = instructions_window.winfo_screenheight()

    if window_height + 20 > screen_height:
        window_height = screen_height - 20  

    x_position = (screen_width // 2) - (window_width // 2)

    y_position = screen_height - window_height - 100

    instructions_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")


    canvas = Canvas(instructions_window)
    scrollbar = Scrollbar(instructions_window, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def on_mouse_wheel(event):
        if event.num == 5 or event.delta < 0:
            canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            canvas.yview_scroll(-1, "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)  
    canvas.bind_all("<Button-4>", on_mouse_wheel)   
    canvas.bind_all("<Button-5>", on_mouse_wheel)   

    tk.Label(scrollable_frame, text="Volg de onderstaande stappen om Fabric te installeren in TLauncher:", wraplength=400, justify="left", font=("Arial", 20)).pack(pady=10)

    steps = [
        ("1. Open de Minecraft launcher\n", None),
        ("2. Selecteer bij versies Fabric 1.21.1\n", IMAGE_URLS.get("step2_mc")),
        ("3. Klik op spelen\n", IMAGE_URLS.get("step3_mc")),
        ("4. Veel plezier\n", None)
    ]

    for step in steps:
        step_text, image_file = step
        tk.Label(scrollable_frame, text=step_text, wraplength=400, justify="left", font=("Arial", 20)).pack(pady=5)
        if image_file:
            try:
                pil_image = Image.open(image_file)
                img_width, img_height = pil_image.size
                scale_factor = min(800/img_width, 600/img_height)
                new_width = int(img_width * scale_factor)
                new_height = int(img_height * scale_factor)
                
                pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(pil_image)
                
                img_label = Label(scrollable_frame, image=img)
                img_label.image = img
                img_label.pack(pady=5)
                img_label.pack(anchor="center")
            except Exception as e:
                tk.Label(scrollable_frame, text=f"Afbeelding kon niet worden geladen: {image_file}", font=("Arial", 20)).pack(pady=5)

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

    ttk.Button(scrollable_frame, text="Sluiten", command=instructions_window.destroy, style="TButton").pack(pady=10)


def ask_for_vulcano_client():
    install_vulcanoclient()

def show_tlauncher_download_dialog():
    dialog = Toplevel()
    dialog.title("TLauncher Installatie")
    
    window_width = 400
    window_height = 150
    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()
    x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)
    dialog.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    Label(dialog, text="Installeer TLauncher voordat je verder gaat:", wraplength=350, pady=10).pack()
    
    link_label = Label(dialog, text="https://tlauncher.org/en/", fg="blue", cursor="hand2")
    link_label.pack(pady=5)
    link_label.configure(font=('TkDefaultFont', 10, 'underline'))
    
    def open_link(event):
        webbrowser.open("https://tlauncher.org/en/")
    
    link_label.bind("<Button-1>", open_link)
    
    ttk.Button(dialog, text="Sluiten", command=dialog.destroy).pack(pady=10)
    
    dialog.transient(dialog.master)
    dialog.grab_set()
    dialog.focus_set()

def install_fabric(launcher):
    if launcher == "Minecraft":
        minecraft_response = messagebox.askyesno("Minecraft Launcher Installatie", "Heb je de Minecraft Launcher al geïnstalleerd?")
        if not minecraft_response:
            try:
                progress_window, progress_bar, label, console = create_progress_window("Minecraft Launcher Setup")
                update_progress(progress_bar, label, 0, "Start installatie proces...", 
                              console, "Start Minecraft Launcher installatie proces...")
                
                update_progress(progress_bar, label, 20, "Controleren van Winget...", 
                              console, "Controleren of Winget is geïnstalleerd...")
                install_winget_as_admin()
                
                update_progress(progress_bar, label, 50, "Installeren van Minecraft Launcher...", 
                              console, "Start Minecraft Launcher installatie...")
                
                process = subprocess.Popen(
                    ['winget', 'install', '--id=Mojang.MinecraftLauncher', '-e'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                
                progress = 60
                while True:
                    output = process.stdout.readline()
                    error = process.stderr.readline()
                    
                    if output:
                        progress += 5
                        if progress > 90:
                            progress = 90
                        update_progress(progress_bar, label, progress, "Bezig met installeren...", 
                                      console, output.strip())
                    if error:
                        update_progress(progress_bar, label, progress, "Waarschuwing ontvangen", 
                                      console, f"Waarschuwing: {error.strip()}")
                        
                    if output == '' and error == '' and process.poll() is not None:
                        break
                
                if process.returncode == 0:
                    update_progress(progress_bar, label, 100, "Minecraft Launcher is succesvol geïnstalleerd!", 
                                  console, "Minecraft Launcher installatie succesvol afgerond!")
                else:
                    update_progress(progress_bar, label, 100, "Er is een fout opgetreden", 
                                  console, "Er is een fout opgetreden tijdens de installatie.")
                
                time.sleep(2)
                progress_window.destroy()
                
            except Exception as e:
                if 'progress_window' in locals():
                    progress_window.destroy()
                messagebox.showerror("Fout", f"Er is een fout opgetreden bij het installeren van Minecraft Launcher: {str(e)}")
                return

    if launcher == "TLauncher":
        tlauncher_response = messagebox.askyesno("TLauncher Installatie", "Heb je TLauncher al geïnstalleerd?")
        if tlauncher_response:
            ask_for_vulcano_client()
            show_tlauncher_instructions()
        else:
            show_tlauncher_download_dialog()
        return

    minecraft_dir = get_minecraft_directory(launcher)
    if not minecraft_dir or not os.path.exists(minecraft_dir):
        messagebox.showerror("Fout", f"Minecraft-map niet gevonden voor {launcher}.")
        return

    installer_path = download_fabric_installer()
    if not installer_path:
        return

    try:
        command = ["java", "-jar", installer_path, "client", "-dir", minecraft_dir, "-mcversion", "1.21.1"]
        subprocess.run(command, check=True)
        messagebox.showinfo("Succes", f"Fabric succesvol geïnstalleerd voor {launcher}!")
        if launcher == "Minecraft":
            ask_for_vulcano_client()
            show_minecraft_instructions()
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Fout", f"Er is een fout opgetreden bij het installeren van Fabric: {e}")
    finally:
        if os.path.exists(installer_path):
            os.remove(installer_path)

def install_vulcanoclient():
    def detect_os():
        os_name = platform.system()
        print(f"Besturingssysteem gedetecteerd: {os_name}")
        return os_name

    def get_minecraft_directory(launcher):
        os_name = detect_os()
        print(f"Zoeken naar de Minecraft-directory voor launcher: {launcher} op {os_name}")

        if launcher == "Minecraft":
            if os_name == "Windows":
                return os.path.expandvars(r"%APPDATA%\\.minecraft")
            elif os_name == "Darwin":  
                return os.path.expanduser("~/Library/Application Support/minecraft")
            elif os_name == "Linux":
                return os.path.expanduser("~/.minecraft")
        elif launcher == "TLauncher":
            if os_name == "Windows":
                return os.path.expandvars(r"%APPDATA%\\.minecraft")
            elif os_name == "Darwin":
                return os.path.expanduser("~/Library/Application Support/.minecraft")
            elif os_name == "Linux":
                return os.path.expanduser("~/.minecraft")

        print("Minecraft directory niet gevonden.")
        return None

    def download_fabric_installer():
        try:
            installer_path = os.path.join(os.getcwd(), "fabric-installer.jar")
            print(f"Downloaden van Fabric-installer van {FABRIC_INSTALLER_URL} naar {installer_path}")
            urllib.request.urlretrieve(FABRIC_INSTALLER_URL, installer_path)
            print("Fabric-installer succesvol gedownload.")
            return installer_path
        except Exception as e:
            print(f"Fout bij downloaden van de Fabric-installer: {e}")
            messagebox.showerror("Fout", f"Kon de Fabric-installer niet downloaden: {e}")
            return None

    def download_images():
        for key, url in IMAGE_URLS.items():
            local_path = os.path.join(os.getcwd(), f"{key}.png")
            print(f"Proberen afbeelding {key} te downloaden van {url}...")
            
            if not os.path.exists(local_path):
                try:
                    print(f"Afbeelding {key} niet gevonden, downloaden...")
                    urllib.request.urlretrieve(url, local_path)
                    IMAGE_URLS[key] = local_path 
                    print(f"Afbeelding {key} succesvol gedownload en opgeslagen.")
                except Exception as e:
                    print(f"Afbeelding {key} kon niet worden gedownload: {e}")
            else:
                IMAGE_URLS[key] = local_path 
                print(f"Afbeelding {key} is al lokaal aanwezig.")

    def show_tlauncher_instructions():
        print("TLauncher instructies worden weergegeven...")
        instructions_window = Toplevel()
        instructions_window.title("Instructies voor TLauncher")
        instructions_window.geometry("820x600")

        canvas = Canvas(instructions_window)
        scrollbar = Scrollbar(instructions_window, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def on_mouse_wheel(event):
            print(f"Mouse wheel scrolled, event: {event}")
            if event.num == 5 or event.delta < 0:
                canvas.yview_scroll(1, "units")
            elif event.num == 4 or event.delta > 0:
                canvas.yview_scroll(-1, "units")

        canvas.bind_all("<MouseWheel>", on_mouse_wheel)
        canvas.bind_all("<Button-4>", on_mouse_wheel) 
        canvas.bind_all("<Button-5>", on_mouse_wheel)  

        tk.Label(scrollable_frame, text="Volg de onderstaande stappen om Fabric te installeren in TLauncher:", wraplength=400, justify="left", font=("Arial", 20)).pack(pady=10)

        steps = [
            ("1. Open TLauncher\n", None),
            ("2. Geef je nickname in\n", IMAGE_URLS.get("step2")),
            ("3. Selecteer bij versies Fabric 1.21.1\n", IMAGE_URLS.get("step3")),
            ("4. Klik op spelen\n", IMAGE_URLS.get("step4")),
            ("5. Veel plezier\n", None)
        ]

        for step in steps:
            step_text, image_file = step
            tk.Label(scrollable_frame, text=step_text, wraplength=400, justify="left", font=("Arial", 20)).pack(pady=5)
            if image_file:
                try:
                    pil_image = Image.open(image_file)
                    img_width, img_height = pil_image.size
                    scale_factor = min(800/img_width, 600/img_height)
                    new_width = int(img_width * scale_factor)
                    new_height = int(img_height * scale_factor)
                    
                    pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    img = ImageTk.PhotoImage(pil_image)
                    
                    img_label = Label(scrollable_frame, image=img)
                    img_label.image = img
                    img_label.pack(pady=5)
                    img_label.pack(anchor="center")
                except Exception as e:
                    print(f"Fout bij het laden van de afbeelding {image_file}: {e}")
                    tk.Label(scrollable_frame, text=f"Afbeelding kon niet worden geladen: {image_file}", font=("Arial", 20)).pack(pady=5)

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

        ttk.Button(scrollable_frame, text="Sluiten", command=instructions_window.destroy, style="TButton").pack(pady=10)

    def ask_for_vulcano_client():
        print("Vragen of VulcanoClient al geïnstalleerd is...")
        response = messagebox.askyesno("VulcanoClient Installatie", "Heb je VulcanoClient al geïnstalleerd?")
        if response: 
            print("VulcanoClient is al geïnstalleerd.")
            
        else:
            print("VulcanoClient is nog niet geïnstalleerd.")
            response2 = messagebox.askyesno("Installeren", "Wil je VulcanoClient nu installeren?")
            if response2: 
                print("Start installatie van VulcanoClient...")
                install_vulcano_client() 
            else:
                print("VulcanoClient wordt later geïnstalleerd.")
                messagebox.showinfo("Informatie", "Je kunt VulcanoClient later installeren om verder te gaan.")

    def install_vulcano_client():
        CURRENT_PATH = os.getcwd()
        print(f"Installeer VulcanoClient, huidige pad: {CURRENT_PATH}")
        
        if platform.system() == "Darwin": 
            MINECRAFT_PATH = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "minecraft")
        elif platform.system() == "Linux": 
            MINECRAFT_PATH = os.path.join(os.path.expanduser("~"), ".minecraft")
        elif platform.system() == "Windows": 
            MINECRAFT_PATH = os.path.join(os.getenv('APPDATA'), '.minecraft')
        else:
            print("Dit besturingssysteem wordt niet ondersteund.")
            return

        print(f"Installatiepad: {MINECRAFT_PATH}")
        
        if not os.path.exists(MINECRAFT_PATH):
            print("Minecraft directory bestaat niet. Creëer de map...")
            os.makedirs(MINECRAFT_PATH)
        
        def delete_old_files():
            to_delete = [
                os.path.join(MINECRAFT_PATH, "config"),
                os.path.join(MINECRAFT_PATH, "data"),
                os.path.join(MINECRAFT_PATH, "mods"),
                os.path.join(MINECRAFT_PATH, "options.txt"),
                os.path.join(MINECRAFT_PATH, "optionsof.txt"),
                os.path.join(MINECRAFT_PATH, "servers.dat")
            ]
            for item in to_delete:
                try:
                    if os.path.isdir(item):
                        shutil.rmtree(item)
                        print(f"Verwijderd map: {item}")
                    elif os.path.isfile(item):
                        os.remove(item)
                        print(f"Verwijderd bestand: {item}")
                except Exception as e:
                    print(f"Fout bij verwijderen van {item}: {e}")

        def download_file(url, destination):
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()
                with open(destination, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                print(f"Bestand gedownload van {url} naar {destination}")
                return True
            except requests.exceptions.RequestException as e:
                print(f"Fout bij downloaden van {url}: {e}")
                return False

        def extract_zip(zip_path, extract_to):
            try:
                print(f"Uitpakken van {zip_path} naar {extract_to}...")
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_to)
                os.remove(zip_path) 
                print(f"Uitpakken voltooid en zip-bestand verwijderd.")
                return True
            except zipfile.BadZipFile as e:
                print(f"Fout bij uitpakken van {zip_path}: {e}")
                return False

        client_zip_path = os.path.join(CURRENT_PATH, "vulcanoclient.zip")
        if download_file(URL_CLIENT, client_zip_path):
            extract_zip(client_zip_path, MINECRAFT_PATH)
            print("VulcanoClient is succesvol geïnstalleerd!")
            messagebox.showinfo("VulcanoClient Installatie", "VulcanoClient is succesvol geïnstalleerd!")
        else:
            print("Er is een fout opgetreden bij het installeren van VulcanoClient.")
            messagebox.showerror("Fout", "Er is een fout opgetreden bij het installeren van VulcanoClient.")

    ask_for_vulcano_client()

def load_image(image_source):
    try:
        if image_source.startswith("http"):
            response = requests.get(image_source)
            response.raise_for_status()
            image_data = BytesIO(response.content)
            return PhotoImage(data=image_data.read())
        else:
            return PhotoImage(file=image_source)
    except Exception as e:
        print(f"Fout bij het laden van de afbeelding: {e}")
        return None
    
def delete_images_on_close(root):
    dir_current = os.getcwd()
    img_del1 = os.path.join(dir_current, "example_image.png")
    img_del2 = os.path.join(dir_current, "step2.png")
    img_del3 = os.path.join(dir_current, "step3.png")
    img_del4 = os.path.join(dir_current, "step4.png")
    img_del5 = os.path.join(dir_current, "step2_mc.png")
    img_del6 = os.path.join(dir_current, "step3_mc.png")
    img_del7 = os.path.join(dir_current, "step1_lunar.png")
    img_del8 = os.path.join(dir_current, "step2_lunar.png")
    img_del9 = os.path.join(dir_current, "step3_lunar.png")
    img_del10 = os.path.join(dir_current, "step4_lunar.png")
    img_del11 = os.path.join(dir_current, "step5_lunar.png")
    img_del12 = os.path.join(dir_current, "step6_lunar.png")
    img_del13 = os.path.join(dir_current, "step7_lunar.png")
    
    os.remove(img_del1)
    os.remove(img_del2)
    os.remove(img_del3)
    os.remove(img_del4)
    os.remove(img_del5)
    os.remove(img_del6)
    os.remove(img_del7)
    os.remove(img_del8)
    os.remove(img_del9)
    os.remove(img_del10)
    os.remove(img_del11)
    os.remove(img_del12)
    os.remove(img_del13)
    
    root.quit()
    
def disable_close():
    delete_images_on_close(root)

def vulcanoclient_1_21_1_lunar_installer():
    try:
        progress_window, progress_bar, label, console = create_progress_window("VulcanoClient Installatie")
        
        def log_message(message):
            print(message)
            if console:
                update_progress(progress_bar, label, progress_bar['value'], None, 
                              console, message)

        update_progress(progress_bar, label, 10, "Mappen aanmaken...", 
                       console, "Start met aanmaken van benodigde mappen...")
        
        lunar_path = os.path.expanduser("~\\.lunarclient")
        lunar_profiles_path = os.path.join(lunar_path, "profiles")
        lunar_profiles_lunar_path = os.path.join(lunar_profiles_path, "lunar")
        lunar_profiles_lunar_1_21_path = os.path.join(lunar_profiles_lunar_path, "1.21")
        lunar_profiles_lunar_1_21_mods_path = os.path.join(lunar_profiles_lunar_1_21_path, "mods")
        lunar_profiles_lunar_1_21_mods_fabric_1_21_1_path = os.path.join(lunar_profiles_lunar_1_21_mods_path, "fabric-1.21.1")
        lunar_settings_path = os.path.join(lunar_path, "settings")
        lunar_settings_game_path = os.path.join(lunar_settings_path, "game")

        if not os.path.exists(lunar_path):
            os.makedirs(lunar_path)
            log_message(f"De map '{lunar_path}' is aangemaakt.")
        else:
            log_message(f"De map '{lunar_path}' bestaat al.")

        if not os.path.exists(lunar_profiles_path):
            os.makedirs(lunar_profiles_path)
            log_message(f"De map '{lunar_profiles_path}' is aangemaakt.")
        else:
            log_message(f"De map '{lunar_profiles_path}' bestaat al.")

        if not os.path.exists(lunar_profiles_lunar_path):
            os.makedirs(lunar_profiles_lunar_path)
            log_message(f"De map '{lunar_profiles_lunar_path}' is aangemaakt.")
        else:
            log_message(f"De map '{lunar_profiles_lunar_path}' bestaat al.")

        if not os.path.exists(lunar_profiles_lunar_1_21_path):
            os.makedirs(lunar_profiles_lunar_1_21_path)
            log_message(f"De map '{lunar_profiles_lunar_1_21_path}' is aangemaakt.")
        else:
            log_message(f"De map '{lunar_profiles_lunar_1_21_path}' bestaat al.")

        if not os.path.exists(lunar_profiles_lunar_1_21_mods_path):
            os.makedirs(lunar_profiles_lunar_1_21_mods_path)
            log_message(f"De map '{lunar_profiles_lunar_1_21_mods_path}' is aangemaakt.")
        else:
            log_message(f"De map '{lunar_profiles_lunar_1_21_mods_path}' bestaat al.")

        if not os.path.exists(lunar_profiles_lunar_1_21_mods_fabric_1_21_1_path):
            os.makedirs(lunar_profiles_lunar_1_21_mods_fabric_1_21_1_path)
            log_message(f"De map '{lunar_profiles_lunar_1_21_mods_fabric_1_21_1_path}' is aangemaakt.")
        else:
            log_message(f"De map '{lunar_profiles_lunar_1_21_mods_fabric_1_21_1_path}' bestaat al.")

        if not os.path.exists(lunar_settings_path):
            os.makedirs(lunar_settings_path)
            log_message(f"De map '{lunar_settings_path}' is aangemaakt.")
        else:
            log_message(f"De map '{lunar_settings_path}' bestaat al.")

        if not os.path.exists(lunar_settings_game_path):
            os.makedirs(lunar_settings_game_path)
            log_message(f"De map '{lunar_settings_game_path}' is aangemaakt.")
        else:
            log_message(f"De map '{lunar_settings_game_path}' bestaat al.")

        lunar_del1 = os.path.join(lunar_settings_game_path, "features.json")
        lunar_del2 = os.path.join(lunar_settings_game_path, "global_options.json")
        lunar_del3 = os.path.join(lunar_settings_game_path, "language.json")
        lunar_del4 = os.path.join(lunar_settings_game_path, "muted_users.json")
        lunar_del5 = os.path.join(lunar_settings_game_path, "main_menu_theme_manager.json")
        lunar_del6 = os.path.join(lunar_settings_game_path, "version")
        lunar_del7 = os.path.join(lunar_settings_game_path, "Default")
        lunar_del8 = lunar_profiles_lunar_1_21_mods_fabric_1_21_1_path

        for file_path in [lunar_del1, lunar_del2, lunar_del3, lunar_del4, lunar_del5, lunar_del6]:
            if os.path.exists(file_path):
                os.remove(file_path)
                log_message(f"Bestand '{file_path}' is verwijderd.")
            else:
                log_message(f"Bestand '{file_path}' bestaat niet.")

        for dir_path in [lunar_del7, lunar_del8]:
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
                log_message(f"Map '{dir_path}' is verwijderd.")
            else:
                log_message(f"Map '{dir_path}' bestaat niet.")

        zip_url = lunar_vulcanoclient_url
        zip_filename = "vulcanoclient_lunar.zip"
        zip_path = os.path.join(os.getcwd(), zip_filename)

        log_message("Bezig met downloaden van VulcanClient.zip...")
        response = requests.get(zip_url)
        with open(zip_path, 'wb') as f:
            f.write(response.content)
        log_message("Download voltooid!")

        log_message("Bezig met uitpakken...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(lunar_path)
        log_message("Uitpakken voltooid!")

        temp_extract_path = lunar_path
        fabric_source = os.path.join(temp_extract_path, "fabric-1.21.1")
        game_source = os.path.join(temp_extract_path, "game")

        if os.path.exists(fabric_source):
            shutil.copytree(fabric_source, lunar_profiles_lunar_1_21_mods_fabric_1_21_1_path, dirs_exist_ok=True)
            log_message("fabric-1.21.1 map is verplaatst")

        if os.path.exists(game_source):
            for item in os.listdir(game_source):
                source_item = os.path.join(game_source, item)
                dest_item = os.path.join(lunar_settings_game_path, item)
                if os.path.isfile(source_item):
                    shutil.copy2(source_item, dest_item)
                elif os.path.isdir(source_item):
                    shutil.copytree(source_item, dest_item, dirs_exist_ok=True)
            log_message("Game bestanden zijn verplaatst")

        os.remove(zip_path)
        if os.path.exists(fabric_source):
            shutil.rmtree(fabric_source)
        if os.path.exists(game_source):
            shutil.rmtree(game_source)
        log_message("Tijdelijke bestanden zijn opgeruimd")

        update_progress(progress_bar, label, 100, "Installatie voltooid!", 
                       console, "Installatie succesvol afgerond!")
        time.sleep(2)
        progress_window.destroy()
        
    except Exception as e:
        if 'progress_window' in locals():
            progress_window.destroy()
        messagebox.showerror("Fout", f"Er is een fout opgetreden: {str(e)}")


def install_winget_as_admin():
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def install_winget():
        try:
            progress_window, progress_bar, label, console = create_progress_window("Winget Installatie")
            update_progress(progress_bar, label, 0, "Start Winget installatie...", 
                          console, "Start installatie proces van Winget...")

            command = 'irm asheroto.com/winget | iex'
            
            powershell_command = [
                'powershell.exe',
                '-NoProfile',
                '-ExecutionPolicy', 'Bypass',
                '-Command', command
            ]
            
            update_progress(progress_bar, label, 20, "Winget installatie wordt gestart...", 
                          console, "Winget installatie wordt gestart...")
            
            process = subprocess.Popen(
                powershell_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            progress = 20
            while True:
                output = process.stdout.readline()
                error = process.stderr.readline()
                
                if output:
                    progress += 5
                    if progress > 90:
                        progress = 90
                    update_progress(progress_bar, label, progress, "Bezig met installeren...", 
                                  console, output.strip())
                if error:
                    update_progress(progress_bar, label, progress, "Waarschuwing ontvangen", 
                                  console, f"Waarschuwing: {error.strip()}")
                    
                if output == '' and error == '' and process.poll() is not None:
                    break
            
            if process.returncode == 0:
                update_progress(progress_bar, label, 100, "Winget is succesvol geïnstalleerd!", 
                              console, "Winget installatie succesvol afgerond!")
            else:
                update_progress(progress_bar, label, 100, "Er is een fout opgetreden", 
                              console, "Er is een fout opgetreden tijdens de installatie.")
            
            time.sleep(2)
            progress_window.destroy()
                
        except Exception as e:
            if 'progress_window' in locals():
                update_progress(progress_bar, label, 100, "Er is een fout opgetreden!", 
                              console, f"Fout: {str(e)}")
                time.sleep(2)
                progress_window.destroy()
            messagebox.showerror("Fout", f"Er is een fout opgetreden: {str(e)}")

    if not is_admin():
        messagebox.showerror("Fout", "Dit script moet als administrator worden uitgevoerd.")
        return
    else:
        install_winget()


def install_lunar():
    os_name = platform.system()
    
    if os_name == "Windows":
        subprocess.run(['winget', 'install', '--id=Moonsworth.LunarClient', '-e'], 
                      check=True, 
                      creationflags=subprocess.CREATE_NO_WINDOW)
    
    elif os_name == "Darwin":
        subprocess.run(['brew', 'install', '--cask', 'lunar-client'], check=True)
    
    elif os_name == "Linux":
        subprocess.run(['sudo', 'add-apt-repository', 'ppa:lunarclient/lunarclient'], check=True)
        subprocess.run(['sudo', 'apt-get', 'update'], check=True)
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'lunarclient'], check=True)

def lunar_installer():
    progress_window, progress_bar, label, console = create_progress_window("Lunar Client Setup")
    try:
        update_progress(progress_bar, label, 0, "Start installatie proces...", 
                       console, "Start Lunar Client installatie proces...")
        
        update_progress(progress_bar, label, 20, "Controleren van Winget...", 
                       console, "Controleren of Winget is geïnstalleerd...")
        install_winget_as_admin()
        
        update_progress(progress_bar, label, 50, "Installeren van Lunar Client...", 
                       console, "Start Lunar Client installatie...")
        install_lunar()
        
        update_progress(progress_bar, label, 100, "Installatie voltooid!", 
                       console, "Lunar Client installatie proces voltooid!")
        time.sleep(2)
        progress_window.destroy()
        
    except Exception as e:
        update_progress(progress_bar, label, 100, "Er is een fout opgetreden!", 
                       console, f"Fout: {str(e)}")
        time.sleep(2)
        progress_window.destroy()
        messagebox.showerror("Fout", f"Er is een fout opgetreden: {str(e)}")

def lunar_prima():
    print("prima")

def lunar_client():
    response = messagebox.askyesno("Lunar Client Installatie", "Heb je Lunar Client al geïnstalleerd?")
    if response:
        lunar_prima()
        response2 = messagebox.askyesno("VulcanoClient Installatie", "Heb je VulcanoClient voor Lunar Client al geïnstalleerd?")
        if response2:
            lunar_prima()
            show_lunar_instructions()
        else:
            kill_lunar_client()
            vulcanoclient_1_21_1_lunar_installer()
            show_lunar_instructions()
    else:
        kill_lunar_client()
        lunar_installer()
        response2 = messagebox.askyesno("VulcanoClient Installatie", "Heb je VulcanoClient voor Lunar Client al geïnstalleerd?")
        if response2:
            lunar_prima()
            show_lunar_instructions()
        else:
            kill_lunar_client()
            vulcanoclient_1_21_1_lunar_installer()
            show_lunar_instructions()

def create_gui():
    infinite_progress_window = InfiniteProgressWindow()

    if platform.system() == "Windows":
        infinite_progress_window.start()
        download_images()
        infinite_progress_window.stop()
        time.sleep(2)
    else:
        download_images()

    global root
    root = tk.Tk()
    root.title("VulcanoClient Installer")

    window_width = 600
    window_height = 600

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_position = (screen_width // 2) - (window_width // 2)
    y_position = screen_height - window_height - 100

    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

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

    tk.Label(root, text="Selecteer je launcher:", font=("Arial", 20)).pack(pady=10)

    image_source = IMAGE_URLS.get("example_image")
    if image_source:
        img = load_image(image_source)
        if img:
            image_label = tk.Label(root, image=img)
            image_label.image = img 
            image_label.pack(pady=10)

    minecraft_button = ttk.Button(root, text="Minecraft", command=lambda: install_fabric("Minecraft"))
    minecraft_button.pack(pady=5)

    tlauncher_button = ttk.Button(root, text="TLauncher", command=lambda: install_fabric("TLauncher"))
    tlauncher_button.pack(pady=5)

    lunar_button = ttk.Button(root, text="Lunar Client", command=lunar_client)
    lunar_button.pack(pady=5)

    close_button = ttk.Button(root, text="Afsluiten", command=lambda: delete_images_on_close(root))
    close_button.pack(pady=10)

    root.protocol("WM_DELETE_WINDOW", disable_close)

    root.mainloop()


if __name__ == "__main__":
    if platform.system() == "Darwin":
        messagebox.showinfo("Niet ondersteund", "You are using mac? fr? just don't be a poor apple fan and just use windows. you can use this program when you have windows")
        sys.exit()
    create_gui()