import os
import sys
import time

def typewriter_effect(text, speed=0.001, color='\033[92m'):
    """Efecto de escritura rápida para Termux (Verde Android)"""
    for char in text:
        sys.stdout.write(color + char + '\033[0m')
        sys.stdout.flush()
        time.sleep(speed)
    print()

def clear_screen():
    """Limpia la terminal de Termux"""
    os.system('clear')

def show_banner():
    """Banner de AXNDER-MOBILE optimizado para pantallas pequeñas"""
    GREEN = '\033[92m'
    RESET = '\033[0m'
    
    # Versión del banner con ancho ajustado para móviles
    banner = f"""
{GREEN}    █████╗ ██╗  ██╗███╗   ██╗██████╗ ███████╗██████╗ 
   ██╔══██╗╚██╗██╔╝████╗  ██║██╔══██╗██╔════╝██╔══██╗
   ███████║ ╚███╔╝ ██╔██╗ ██║██║  ██║█████╗  ██████╔╝
   ██╔══██║ ██╔██╗ ██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗
   ██║  ██║██╔╝ ██╗██║ ╚████║██████╔╝███████╗██║  ██║
   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝{RESET}"""
    
    typewriter_effect(banner, 0.0005)
    typewriter_effect(" > PROTOCOLO RNIBO INICIALIZADO (MOBILE)...")
    typewriter_effect(" > ENTORNO AXNDER-TERMUX: ONLINE")
    print(f"{GREEN}" + "—"*52 + f"{RESET}")