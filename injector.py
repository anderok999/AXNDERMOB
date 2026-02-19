import os
import subprocess
import time

class AxnderEngine:
    def __init__(self):
        self.found_devices = []

    def _purge(self):
        """Limpia procesos para evitar bloqueos en la memoria de Android."""
        try:
            subprocess.run(['pkill', '-f', 'nanodlna'], capture_output=True)
        except:
            pass

    def scan_network(self):
        """Escaneo profundo. Nota: Requiere GPS activado en el móvil."""
        from nanodlna import devices
        print("\033[93m[*] RASTREANDO NODOS EN RED LOCAL...\033[0m")
        # Aumentamos a 12 segundos porque el Wi-Fi móvil es más inestable
        self.found_devices = devices.get_devices(timeout=12)
        return self.found_devices

    def inject_direct(self, device_index, target_file):
        """Inyecta media directamente al nodo seleccionado."""
        try:
            target = self.found_devices[device_index]
            location = getattr(target, 'location', '')
            self._purge()
            
            # Ejecución limpia para Termux
            cmd = f'nanodlna play "{target_file}" --device "{location}"'
            subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception as e:
            print(f"[-] Error de inyección: {e}")
            return False

    def inject_sequence(self, device_index, target_file):
        """Inyecta Intro de seguridad + Payload final."""
        target = self.found_devices[device_index]
        location = getattr(target, 'location', '')
        intro = "intro_axnder.mp4"
        
        if not os.path.exists(intro):
            print(f"[-] No se encontró {intro}, saltando a payload...")
            return self.inject_direct(device_index, target_file)

        self._purge()
        subprocess.Popen(f'nanodlna play "{intro}" --device "{location}"', shell=True)
        time.sleep(7) # Duración de la intro
        self._purge()
        subprocess.Popen(f'nanodlna play "{target_file}" --device "{location}"', shell=True)
        return True

    def stop_all(self, device_index):
        """Corta la comunicación con el nodo."""
        target = self.found_devices[device_index]
        location = getattr(target, 'location', '')
        subprocess.run(f'nanodlna stop --device "{location}"', shell=True)
        self._purge()