from branding import show_banner, clear_screen, typewriter_effect
from injector import AxnderEngine
from ghost_writer import create_terminal_message
from voice_engine import generate_voice_msg
import time
import os

def main():
    # En Termux es vital asegurarse de estar en el directorio correcto
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    clear_screen()
    show_banner()
    
    engine = AxnderEngine()
    typewriter_effect("\033[92m[*] AXNDER-MOBILE: INICIANDO ESCANEO LOCAL...\033[0m")
    
    # Verificación de Ubicación (Crucial en Android)
    print("\033[93m[!] RECUERDA: El GPS/Ubicación debe estar ON para detectar nodos.\033[0m")
    
    try:
        devs = engine.scan_network()
    except Exception as e:
        print(f"\033[91m[-] ERROR DE RED TERMUX: {e}\033[0m")
        return
    
    if not devs:
        print("\033[91m[-] NO SE DETECTARON NODOS. REINTENTA CON GPS ACTIVADO.\033[0m")
        return

    print("\n ID | NODO DETECTADO             | IP")
    print(" " + "-"*50)
    for idx, d in enumerate(devs):
        name = getattr(d, 'friendly_name', 'Smart TV')
        ip = getattr(d, 'ip', '0.0.0.0')
        print(f" {idx:<2} | {name[:20]:<21} | {ip}")
    print(" " + "-"*50)

    try:
        target_id = int(input("\n[?] SELECCIONA ID: "))
        
        while True:
            print("\n\033[92m--- PANEL AXNDER ANDROID ---\033[0m")
            print(" 1. PAYLOAD COMPLETO (INTRO + FILE)")
            print(" 2. GHOST WRITE (TEXTO)")
            print(" 3. GHOST VOICE (VOZ + TEXTO)")
            print(" 4. DETENER TODO")
            print(" 5. SALIR")
            
            opc = input("\nAXNDER-MBL >> ")

            if opc == "1":
                file_path = input("[?] PAYLOAD (ej: video.mp4): ")
                engine.inject_sequence(target_id, file_path)
            
            elif opc == "2":
                msg = input("[?] MENSAJE: ")
                img = create_terminal_message(msg)
                engine.inject_direct(target_id, img)

            elif opc == "3":
                msg = input("[?] MENSAJE VOZ: ")
                img = create_terminal_message(msg)
                audio = generate_voice_msg(msg)
                engine.inject_direct(target_id, img)
                time.sleep(2)
                engine.inject_direct(target_id, audio)

            elif opc == "4":
                engine.stop_all(target_id)
            
            elif opc == "5":
                break
    except:
        print("\n[-] Sesión cerrada.")

if __name__ == "__main__":
    main()