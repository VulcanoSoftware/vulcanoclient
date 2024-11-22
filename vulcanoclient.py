import os
import requests
import subprocess
import platform
import zipfile
import shutil
import sys
import ctypes

# URLs voor downloads
URL_WIN = "https://github.com/VulcanoSoftware/vulcanoclient/raw/refs/heads/main/TLauncher-Installer-1.5.4.exe"
URL_MAC_LINUX = "https://github.com/VulcanoSoftware/vulcanoclient/raw/refs/heads/main/TLauncher.jar"
URL_CLIENT = "https://github.com/VulcanoSoftware/vulcanoclient/releases/download/1.1/vulcanoclient.zip"
JAVA_URL_WIN = "https://www.dropbox.com/scl/fi/76bxeokec52ogubia5953/OpenJDK21U-jdk_x64_windows_hotspot_21.0.5_11-1.msi?rlkey=cf9vfdwqu9j4jebhxw7a3emx1&st=q0zh2t3j&dl=1"
JAVA_URL_MAC = "https://www.dropbox.com/scl/fi/bq5hk1h8wzapmfcyl0oyw/OpenJDK21U-jdk_x64_mac_hotspot_21.0.5_11.pkg?rlkey=9cq1s36qv9fjvf1hse748zxil&st=yunz104m&dl=1"
FABRIC_URL = "https://github.com/VulcanoSoftware/vulcanoclient/raw/refs/heads/main/fabric-installer-1.0.1.jar"

# Het huidige pad bepalen
CURRENT_PATH = os.getcwd()

# Automatisch het pad naar de .minecraft map bepalen
if platform.system() == "Darwin":  # macOS
    MINECRAFT_PATH = os.path.join(os.path.expanduser("~"), "Library", "Application Support", "minecraft")
    OS_TYPE = "mac"
elif platform.system() == "Linux":  # Linux
    MINECRAFT_PATH = os.path.join(os.path.expanduser("~"), ".minecraft")
    OS_TYPE = "linux"
elif platform.system() == "Windows":  # Windows
    MINECRAFT_PATH = os.path.join(os.getenv('APPDATA'), '.minecraft')
    OS_TYPE = "windows"
else:
    print("Dit besturingssysteem wordt niet ondersteund.")
    sys.exit()

# Controleer of de .minecraft map al bestaat, maak deze aan als dat niet het geval is
if not os.path.exists(MINECRAFT_PATH):
    print(f"De map {MINECRAFT_PATH} bestaat niet. De map wordt nu aangemaakt...")
    os.makedirs(MINECRAFT_PATH)
else:
    print(f"De map {MINECRAFT_PATH} bestaat al.")

print(f"Het .minecraft pad is: {MINECRAFT_PATH}")

# Functie om te controleren of Java is geïnstalleerd
def check_java():
    try:
        subprocess.run(["java", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("Java is al geïnstalleerd.")
        return True
    except subprocess.CalledProcessError:
        print("Java lijkt niet correct te zijn geïnstalleerd.")
        return False
    except FileNotFoundError:
        print("Java is niet geïnstalleerd.")
        return False

# Functie om Java te installeren
def install_java():
    if OS_TYPE == "windows":
        java_installer_path = os.path.join(CURRENT_PATH, "openjdk-windows-installer.msi")
        if download_file(JAVA_URL_WIN, java_installer_path):
            try:
                subprocess.run([java_installer_path, "/quiet", "/norestart"], check=True)
                print("Java 21 is succesvol geïnstalleerd op Windows.")
            except subprocess.CalledProcessError as e:
                print(f"Fout bij het installeren van Java op Windows: {e}")
            finally:
                os.remove(java_installer_path)
    elif OS_TYPE == "mac":
        java_installer_path = os.path.join(CURRENT_PATH, "openjdk-macos-installer.pkg")
        if download_file(JAVA_URL_MAC, java_installer_path):
            try:
                subprocess.run(["sudo", "installer", "-pkg", java_installer_path, "-target", "/"], check=True)
                print("Java 21 is succesvol geïnstalleerd op macOS.")
            except subprocess.CalledProcessError as e:
                print(f"Fout bij het installeren van Java op macOS: {e}")
            finally:
                os.remove(java_installer_path)
    elif OS_TYPE == "linux":
        print("Linux gedetecteerd. Java 21 wordt nu geïnstalleerd...")
        try:
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "-y", "openjdk-21-jdk"], check=True)
            print("Java 21 is succesvol geïnstalleerd op Linux.")
        except subprocess.CalledProcessError as e:
            print(f"Fout bij het installeren van Java op Linux: {e}")
    else:
        print("Geen installatie-instructies beschikbaar voor jouw besturingssysteem.")

    print("Herstart het script nadat Java is geïnstalleerd.")
    # Na installatie, controleer opnieuw of Java werkt
    if not check_java():
        print("Java is niet goed geïnstalleerd. Het script kan niet verder gaan.")
        sys.exit()

    sys.exit()


# Functie om bestanden te downloaden
def download_file(url, destination):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(destination, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Bestand gedownload naar: {destination}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Fout bij het downloaden van {url}: {e}")
        return False

# Functie om bestanden uit te pakken
def extract_zip(zip_path, extract_to):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"Bestand succesvol uitgepakt naar: {extract_to}")
        os.remove(zip_path)
        return True
    except zipfile.BadZipFile as e:
        print(f"Fout bij het uitpakken van {zip_path}: {e}")
        return False

# Functie om oude bestanden te verwijderen
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
                print(f"Map verwijderd: {item}")
            elif os.path.isfile(item):
                os.remove(item)
                print(f"Bestand verwijderd: {item}")
        except Exception as e:
            print(f"Fout bij verwijderen van {item}: {e}")

# Hoofdwhile-lus
while True:
    cracked = input("Heb je Minecraft gekocht? (Y/N) ").strip().lower()

    if cracked == "y":
        print("Je hebt premium Minecraft.")
        mc_dl = input("Heb je Minecraft al gedownload? (Y/N) ").strip().lower()
        if mc_dl == "y":
            fabric_installed = input("Is Fabric al geïnstalleerd? (Y/N) ").strip().lower()
            if fabric_installed == "n":
                print("Fabric wordt nu geïnstalleerd...")
                fabric_installer_path = os.path.join(CURRENT_PATH, "fabric-installer.jar")
                
                # Download Fabric Installer
                if download_file(FABRIC_URL, fabric_installer_path):
                    try:
                        # Fabric installeren op Windows, macOS en Linux met de juiste versie
                        print("=======================================")
                        print("volg onderstaande instructies: ")
                        print("selecteer bij de minecraft versie 1.21.1")
                        print("selecteer bij loader versie 0.16.2")
                        print("zorg ervoor dat 'create profile' aangevinkt is")
                        print("klik op install")
                        print("=======================================")
                        subprocess.run(["java", "-jar", fabric_installer_path, "--installClient", "--minecraftVersion", "1.21.1", "--fabricLoader", "0.16.2"], check=True)
                        input("druk op enter als je klaar bent met deze stap ... ")
                    except subprocess.CalledProcessError as e:
                        print(f"Fout bij het installeren van Fabric: {e}")
                    finally:
                        os.remove(fabric_installer_path)
                else:
                    print("Download van Fabric Installer is mislukt. Probeer opnieuw.")
            elif fabric_installed == "y":
                print("Fabric is al geïnstalleerd. Start je Minecraft-launcher om te spelen!")
                break
            else:
                print("Ongeldige invoer. Start het script opnieuw.")
        elif mc_dl == "n":
            print("Download Minecraft via https://minecraft.net en probeer opnieuw.")
            input("druk op enter als je klaar bent met deze stap ... ")
        else:
            print("Ongeldige invoer. Start het script opnieuw.")

    elif cracked == "n":
        print("Je hebt een cracked Minecraft-account.")
        minecraft_dl = input("Wil je Minecraft downloaden? (Y/N) ").strip().lower()
        if minecraft_dl == "y":
            print("Minecraft wordt nu gedownload...")
            if OS_TYPE == "windows":
                download_file(URL_WIN, "TLauncher-Installer-1.5.4.exe")
                subprocess.run(["TLauncher-Installer-1.5.4.exe", "/S"], check=True)
                input("druk op enter als je klaar bent met deze stap ... ")
            elif OS_TYPE == "mac" or OS_TYPE == "linux":
                download_file(URL_MAC_LINUX, "TLauncher.jar")
                input("druk op enter als je klaar bent met deze stap ... ")

            print("Minecraft downloaden...")
            download_file(URL_CLIENT, "vulcanoclient.zip")
            extract_zip("vulcanoclient.zip", MINECRAFT_PATH)
            input("druk op enter als je klaar bent met deze stap ... ")

            break
        elif minecraft_dl == "n":
            print("Zonder Minecraft kan dit script niet verder. Het script wordt afgesloten.")
            sys.exit()
        else:
            print("Ongeldige invoer. Start het script opnieuw.")
