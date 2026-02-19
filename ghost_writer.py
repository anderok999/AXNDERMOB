from PIL import Image, ImageDraw, ImageFont
import os

def create_terminal_message(text):
    # Resolución nativa de Smart TV para evitar el efecto "miniatura"
    width, height = 1920, 1080 
    image = Image.new('RGB', (width, height), color='black')
    draw = ImageDraw.Draw(image)
    
    # Fuentes del sistema Android
    font_paths = [
        "/system/fonts/Roboto-Bold.ttf",
        "/system/fonts/DroidSansMono.ttf",
        "/system/fonts/NotoSans-Bold.ttf"
    ]

    font_path = next((p for p in font_paths if os.path.exists(p)), None)
    
    # Tamaño de fuente dinámico: si el texto es corto, es GIGANTE
    font_size = 250 if len(text) < 10 else 180
    if len(text) > 20: font_size = 120

    try:
        font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()
    except:
        font = ImageFont.load_default()

    # Centrado absoluto
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((width - tw) // 2, (height - th) // 2), text, fill=(0, 255, 0), font=font)
    
    # Guardado optimizado para transmisión rápida por red
    path = os.path.abspath("ghost_msg.png")
    image.save(path, "PNG", optimize=True)
    return path