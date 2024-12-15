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

FABRIC_INSTALLER_URL = "https://github.com/VulcanoSoftware/vulcanoclient/raw/refs/heads/main/fabric-installer-0.11.2.jar"

URL_CLIENT = "https://github.com/VulcanoSoftware/vulcanoclient/releases/download/1.2/vulcanoclient.zip"

IMAGE_URLS = {
    "step2": "https://www.dropbox.com/scl/fi/dqqdkg9szyunwpqm0jalv/step2.png?rlkey=0gkoxa2tcvsh1np6uo6lspu5r&st=2t5rirs5&dl=1",
    "step3": "https://www.dropbox.com/scl/fi/31yvorfga25deggv19c8n/step3.png?rlkey=71c3nc5mnk59otnmzx5f2flpp&st=4torqxn8&dl=1",
    "step4": "https://www.dropbox.com/scl/fi/4cobagvk6v2gjj6p00hxu/step4.png?rlkey=34lx0wntdcb4jc1u2ldqnern8&st=ku5rp7dr&dl=1",
    "step2_mc": "https://www.dropbox.com/scl/fi/aa7yrqozvf5rj0p249ppx/step2_mc.png?rlkey=re6l7ctybklev8ibk0hvyzncy&st=03dscwik&dl=1",
    "step3_mc": "https://www.dropbox.com/scl/fi/2dlgpejy71fxj1rhri7pl/step3_mc.png?rlkey=y3xrc1k35vtob794r2tgtkta0&st=jzjyp79l&dl=1",
    "example_image": "https://www.dropbox.com/scl/fi/157ujxatwxkztlni2eog4/8d22d753007f68c48eea910386b79ab3.png?rlkey=bkspxpwq57t1ngzd7m72qm3gk&st=b5qeindq&dl=1"
}

def java_install():
    def is_choco_installed():
        try:
            subprocess.run(['choco', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            return False

    def install_choco():
        try:
            subprocess.run(
                ['powershell', '-Command', 
                'Set-ExecutionPolicy Bypass -Scope Process -Force; '
                '[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12; '
                'iex ((New-Object System.Net.WebClient).DownloadString("https://community.chocolatey.org/install.ps1"))'],
                check=True
            )
            print("Chocolatey is succesvol geïnstalleerd.")
        except subprocess.CalledProcessError as e:
            print(f"Fout bij het installeren van Chocolatey: {e}")
            sys.exit(1)

    def is_java_installed():
        try:
            java_path = subprocess.run(['which', 'java'], stdout=subprocess.PIPE, stderr=subprocess.PIPE) if platform.system() != 'Windows' else subprocess.run(['where', 'java'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return java_path.returncode == 0
        except Exception as e:
            print(f"Fout bij het controleren van Java-installatie: {e}")
            return False

    def install_java_windows():
        try:
            subprocess.run(['choco', 'install', 'openjdk', '--version=21', '-y'], check=True)
            print("Java 21 is succesvol geïnstalleerd op Windows.")
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
                print("Het script wordt niet uitgevoerd als administrator op Windows.")
        
        elif platform.system() in ['Linux', 'Darwin']:
            if os.geteuid() == 0:
                print("Het script wordt uitgevoerd als root op Linux/macOS.")
            else:
                print("Het script wordt niet uitgevoerd als root op Linux/macOS.")
        
        if not is_java_installed():
            print("Java 21 is nog niet geïnstalleerd.")

            if os_platform == 'Windows':
                if not is_choco_installed():
                    print("Chocolatey is nog niet geïnstalleerd. Dit zal nu gebeuren...")
                    install_choco()
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
        main()
        
java_install()

def detect_os():
    return platform.system()


def get_minecraft_directory(launcher):
    os_name = detect_os()

    if launcher == "Minecraft":
        if os_name == "Windows":
            return os.path.expandvars(r"%APPDATA%\\.minecraft")
        elif os_name == "Darwin": 
            return os.path.expanduser("~/Library/Application Support/minecraft")
        elif os_name == "Linux":
            return os.path.expanduser("~/.minecraft")
    elif launcher == "TLauncher":
        if os_name == "Windows":
            return os.path.expandvars(r"%APPDATA%\\.tlauncher\\.minecraft")
        elif os_name == "Darwin":
            return os.path.expanduser("~/Library/Application Support/tlauncher/.minecraft")
        elif os_name == "Linux":
            return os.path.expanduser("~/.tlauncher/.minecraft")

    return None

def download_fabric_installer():
    try:
        installer_path = os.path.join(os.getcwd(), "fabric-installer.jar")
        urllib.request.urlretrieve(FABRIC_INSTALLER_URL, installer_path)
        return installer_path
    except Exception as e:
        messagebox.showerror("Fout", f"Kon de Fabric-installer niet downloaden: {e}")
        return None

def download_images():
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
                img = PhotoImage(file=image_file)  
                img = img.subsample(2, 2)  
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
                img = PhotoImage(file=image_file)  
                img = img.subsample(2, 2)  
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

def install_fabric(launcher):
    if launcher == "TLauncher":
        ask_for_vulcano_client() 
        show_tlauncher_instructions()
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
                return os.path.expandvars(r"%APPDATA%\\.tlauncher\\.minecraft")
            elif os_name == "Darwin":
                return os.path.expanduser("~/Library/Application Support/tlauncher/.minecraft")
            elif os_name == "Linux":
                return os.path.expanduser("~/.tlauncher/.minecraft")

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
                    img = PhotoImage(file=image_file)
                    img = img.subsample(2, 2) 
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
    
    os.remove(img_del1)
    os.remove(img_del2)
    os.remove(img_del3)
    os.remove(img_del4)
    os.remove(img_del5)
    os.remove(img_del6)
    
    root.quit()
    
def disable_close():
    pass

def create_gui():
    download_images()

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

    close_button = ttk.Button(root, text="Afsluiten", command=lambda: delete_images_on_close(root))
    close_button.pack(pady=10)

    root.protocol("WM_DELETE_WINDOW", disable_close)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
