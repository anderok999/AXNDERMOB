from PIL import Image, ImageDraw, ImageFont
import os

def create_terminal_message(text):
    # En TVs el aspect ratio suele ser 16:9
    width, height = 1280, 720 
    image = Image.new('RGB', (width, height), color='black')
    draw = ImageDraw.Draw(image)
    
    # Rutas exclusivas de Android
    font_paths = [
        "/system/fonts/Roboto-Bold.ttf",
        "/system/fonts/DroidSans.ttf",
        "/system/fonts/NotoSans-Bold.ttf"
    ]

    font_path = next((p for p in font_paths if os.path.exists(p)), None)
    
    try:
        font = ImageFont.truetype(font_path, 100) if font_path else ImageFont.load_default()
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((width - tw) // 2, (height - th) // 2), text, fill=(0, 255, 0), font=font)
    
    path = os.path.abspath("ghost_msg.png")
    image.save(path)
    return path