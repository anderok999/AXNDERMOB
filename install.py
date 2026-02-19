import os
import subprocess
import sys
import time

def run_cmd(cmd):
    try:
        subprocess.check_call(cmd, shell=True)
    except Exception as e:
        print(f"\033[91m[!] Error ejecutando {cmd}: {e}\033[0m")

def setup_axnder():
    print("\033[96m" + "="*40)
    print("      AXNDER-MOBILE INSTALLER")
    print("="*40 + "\033[0m")

    # 1. Verificar si es Termux
    if os.path.exists("/data/data/com.termux"):
        print("[*] Entorno Termux detectado.")
        # Actualizar e instalar dependencias de sistema
        run_cmd("pkg update -y && pkg upgrade -y")
        run_cmd("pkg install python pillow libjpeg-turbo -y")
        
        # 2. Permisos de almacenamiento
        print("[*] Solicitando permisos de almacenamiento...")
        run_cmd("termux-setup-storage")
        print("\033[93m[!] POR FAVOR, ACEPTA EL POP-UP DE PERMISOS EN TU PANTALLA.\033[0m")
        time.sleep(3)
    else:
        print("[!] No se detectó Termux. Asegúrate de estar en Android.")

    # 3. Instalar librerías de Python
    print("[*] Instalando dependencias de Python...")
    run_cmd(f"{sys.executable} -m pip install --upgrade pip")
    run_cmd(f"{sys.executable} -m pip install nanodlna gtts pillow")

    # 4. Crear estructura de carpetas
    if not os.path.exists("payloads"):
        os.makedirs("payloads")
        print("[+] Carpeta /payloads creada.")

    print("\n\033[92m[V] INSTALACIÓN COMPLETADA.\033[0m")
    print("\033[92m[>] Para iniciar usa: python main.py\033[0m")
    print("\033[93m[!] IMPORTANTE: Activa el GPS antes de escanear.\033[0m\n")

if __name__ == "__main__":
    setup_axnder()