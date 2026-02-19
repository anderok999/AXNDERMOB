import os
import subprocess
import time

class AxnderEngine:
    def __init__(self):
        self.found_devices = []

    def _purge(self):
        """Limpia procesos previos para que la red no se sature."""
        try:
            subprocess.run(['pkill', '-f', 'nanodlna'], capture_output=True)
            time.sleep(0.3)
        except:
            pass

    def scan_network(self):
        from nanodlna import devices
        print("\033[92m[*] RASTREANDO NODOS (VERIFICA GPS ON)...\033[0m")
        self.found_devices = devices.get_devices(timeout=10)
        return self.found_devices

    def inject_direct(self, device_index, target_file):
        try:
            target = self.found_devices[device_index]
            location = getattr(target, 'location', '')
            self._purge()
            
            # --no-stdin evita que el proceso se quede esperando en Termux
            cmd = f'nanodlna play "{target_file}" --device "{location}" --no-stdin'
            subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception as e:
            print(f"[-] Error: {e}")
            return False

    def inject_sequence(self, device_index, target_file):
        target = self.found_devices[device_index]
        location = getattr(target, 'location', '')
        intro = "intro_axnder.mp4"
        
        self._purge()
        # Inyectar Intro
        subprocess.Popen(f'nanodlna play "{intro}" --device "{location}" --no-stdin', shell=True)
        time.sleep(7) 
        self._purge()
        # Inyectar Payload
        subprocess.Popen(f'nanodlna play "{target_file}" --device "{location}" --no-stdin', shell=True)
        return True

    def stop_all(self, device_index):
        target = self.found_devices[device_index]
        location = getattr(target, 'location', '')
        subprocess.run(f'nanodlna stop --device "{location}"', shell=True)
        self._purge()