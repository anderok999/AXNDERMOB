from PIL import Image, ImageDraw, ImageFont
import os

def create_terminal_message(text):
    # Resolución 720p para máxima compatibilidad
    width, height = 1280, 720 
    image = Image.new('RGB', (width, height), color='black')
    draw = ImageDraw.Draw(image)
    
    # --- LA SOLUCIÓN AQUÍ ---
    # Nombre exacto del archivo que subiste a GitHub
    font_filename = "Courier_New.ttf"
    
    # Buscamos la fuente en la misma carpeta donde está este script (.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(current_dir, font_filename)
    
    # Definimos el tamaño gigante (ahora sí se aplicará)
    font_size = 150 if len(text) < 12 else 85

    font = None
    try:
        if os.path.exists(font_path):
            # Si el archivo existe en la carpeta, lo cargamos con el tamaño masivo
            font = ImageFont.truetype(font_path, font_size)
        else:
            # Si no está (por si alguien no bajó la fuente), buscamos en Android como respaldo
            print(f"[!] Archivo {font_filename} no detectado. Buscando respaldo...")
            fallback_paths = [
                "/system/fonts/Roboto-Bold.ttf",
                "/system/fonts/DroidSans-Bold.ttf"
            ]
            for p in fallback_paths:
                if os.path.exists(p):
                    font = ImageFont.truetype(p, font_size)
                    break
    except Exception as e:
        print(f"[-] Error cargando fuente TTF: {e}")

    # Si todo lo anterior falla, usamos la fuente por defecto (se verá pequeña, pero el programa no crashea)
    if font is None:
        font = ImageFont.load_default()

    # Cálculo de centrado (esto asegura que el texto quede en medio de la TV)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    # Dibujamos en verde neón (Color Matrix)
    draw.text(((width - tw) // 2, (height - th) // 2), text, fill=(0, 255, 0), font=font)
    
    # Guardamos la imagen
    path = os.path.abspath("ghost_msg.png")
    image.save(path, "PNG", optimize=True)
    return path