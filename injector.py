import os
import subprocess
import time

class AxnderEngine:
    def __init__(self):
        self.found_devices = []

    def _purge(self):
        """Limpia procesos de nanodlna para liberar memoria en Android."""
        try:
            subprocess.run(['pkill', '-f', 'nanodlna'], capture_output=True)
        except:
            pass

    def scan_network(self):
        from nanodlna import devices
        # Timeout más largo porque el Wi-Fi de los móviles suele tardar más en resolver
        self.found_devices = devices.get_devices(timeout=10)
        return self.found_devices

    def inject_sequence(self, device_index, target_file):
        target = self.found_devices[device_index]
        location = getattr(target, 'location', '')
        self._purge()
        try:
            # Fase 1
            subprocess.Popen(f'nanodlna play "intro_axnder.mp4" --device "{location}"', shell=True)
            time.sleep(7)
            self._purge()
            # Fase 2
            subprocess.Popen(f'nanodlna play "{target_file}" --device "{location}"', shell=True)
            return True
        except: return False

    def inject_direct(self, device_index, target_file):
        target = self.found_devices[device_index]
        location = getattr(target, 'location', '')
        self._purge()
        subprocess.Popen(f'nanodlna play "{target_file}" --device "{location}"', shell=True)
        return True

    def stop_all(self, device_index):
        target = self.found_devices[device_index]
        location = getattr(target, 'location', '')
        subprocess.run(f'nanodlna stop --device "{location}"', shell=True)