from branding import show_banner, clear_screen, typewriter_effect
from injector import AxnderEngine
from ghost_writer import create_terminal_message
from voice_engine import generate_voice_msg
import time
import os
import sys

def loading_animation(duration=3):
    chars = "/—\|"
    for i in range(duration * 10):
        sys.stdout.write(f"\r\033[92m[*] ENVIANDO PAYLOAD {chars[i % len(chars)]}\033[0m")
        sys.stdout.flush()
        time.sleep(0.1)
    print("\n")

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    clear_screen()
    show_banner()
    
    engine = AxnderEngine()
    typewriter_effect("\033[92m[*] PROTOCOLO AXNDER-MOBILE ACTIVO\033[0m")
    
    devs = engine.scan_network()
    if not devs:
        print("\033[91m[-] NINGÚN NODO ENCONTRADO. ACTIVA GPS Y REINTENTA.\033[0m")
        return

    print("\n ID | OBJETIVO             | IP")
    print("-" * 45)
    for idx, d in enumerate(devs):
        name = getattr(d, 'friendly_name', 'Smart TV')
        ip = getattr(d, 'ip', '0.0.0.0')
        print(f" {idx:<2} | {name[:18]:<19} | {ip}")
    print("-" * 45)

    try:
        target_id = int(input("\n[?] ID DEL OBJETIVO: "))
        while True:
            print("\n\033[92m[1] INTRO+FILE [2] TEXTO [3] VOZ+TEXTO [4] STOP [5] SALIR\033[0m")
            opc = input("AXNDER >> ")

            if opc == "1":
                f = input("[?] ARCHIVO: ")
                if engine.inject_sequence(target_id, f): loading_animation()
            
            elif opc == "2":
                m = input("[?] MENSAJE: ")
                path = create_terminal_message(m)
                if engine.inject_direct(target_id, path): loading_animation(2)

            elif opc == "3":
                m = input("[?] MENSAJE VOZ: ")
                img = create_terminal_message(m)
                audio = generate_voice_msg(m)
                engine.inject_direct(target_id, img)
                loading_animation(2)
                time.sleep(1)
                engine.inject_direct(target_id, audio)

            elif opc == "4":
                engine.stop_all(target_id)
                print("[!] Nodo purgado.")

            elif opc == "5": break
    except Exception as e:
        print(f"[-] ERROR: {e}")

if __name__ == "__main__":
    main()