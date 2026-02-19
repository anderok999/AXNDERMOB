import os
import subprocess
import time

class AxnderEngine:
    def __init__(self):
        self.found_devices = []

    def _purge(self):
        """Limpia procesos para evitar bloqueos en la red de Android."""
        try:
            os.system('pkill -f nanodlna > /dev/null 2>&1')
            time.sleep(0.5)
        except:
            pass

    def scan_network(self):
        from nanodlna import devices
        print("\033[92m[*] RASTREANDO NODOS (RNIBO AGRESSIVE SCANN)...\033[0m")
        
        # Escaneo de 12 segundos para dar tiempo a las TVs lentas
        raw_devs = devices.get_devices(timeout=12)
        self.found_devices = []

        for d in raw_devs:
            # Extraemos datos básicos del objeto o diccionario
            name = getattr(d, 'friendly_name', 'Smart TV')
            loc = getattr(d, 'location', '')
            ip = getattr(d, 'ip', '0.0.0.0')

            # REPARACIÓN DE IP: Si la IP es 0.0.0.0, la sacamos del URL de 'location'
            if (ip == '0.0.0.0' or ip == '') and '//' in loc:
                try:
                    ip = loc.split('//')[1].split(':')[0]
                except:
                    ip = "Unknown"

            self.found_devices.append({
                'friendly_name': name,
                'location': loc,
                'ip': ip
            })
        
        return self.found_devices

    def inject_direct(self, device_index, target_file):
        try:
            target = self.found_devices[device_index]
            loc = target['location']
            self._purge()
            
            # --no-stdin es vital para que Termux no se cuelgue
            cmd = f'nanodlna play "{target_file}" --device "{loc}" --no-stdin'
            subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception as e:
            print(f"[-] Error de inyección: {e}")
            return False

    def inject_sequence(self, device_index, target_file):
        target = self.found_devices[device_index]
        loc = target['location']
        self._purge()
        
        # Fase 1: Intro
        subprocess.Popen(f'nanodlna play "intro_axnder.mp4" --device "{loc}" --no-stdin', shell=True)
        time.sleep(7)
        self._purge()
        # Fase 2: Payload
        subprocess.Popen(f'nanodlna play "{target_file}" --device "{loc}" --no-stdin', shell=True)
        return True

    def stop_all(self, device_index):
        target = self.found_devices[device_index]
        loc = target['location']
        subprocess.run(f'nanodlna stop --device "{loc}"', shell=True)
        self._purge()