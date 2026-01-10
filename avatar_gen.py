import os
import argparse
from PIL import Image, ImageDraw, ImageFont

def get_font(font_size, font_path=None):
    if font_path and os.path.exists(font_path):
        return ImageFont.truetype(font_path, font_size)
    
    fonts_to_try = [
        "arial.ttf", "Arial.ttf", "DejaVuSans.ttf", 
        "LiberationSans-Regular.ttf", "Verdana.ttf"
    ]
    
    for font in fonts_to_try:
        try:
            return ImageFont.truetype(font, font_size)
        except IOError:
            continue
            
    return ImageFont.load_default()

def generate_avatar(text, color, size=500, output="avatar.png", font_path=None, scale=0.52):
    render_size = size * 2 
    image = Image.new('RGB', (render_size, render_size), color)
    draw = ImageDraw.Draw(image)

    font_size = int(render_size * scale)
    font = get_font(font_size, font_path)

    bbox = draw.textbbox((0, 0), text.upper(), font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (render_size - text_width) // 2 - bbox[0]
    y = (render_size - text_height) // 2 - bbox[1]

    draw.text((x, y), text.upper(), fill="white", font=font)

    mask = Image.new('L', (render_size, render_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, render_size, render_size), fill=255)
    
    output_image = Image.new('RGBA', (render_size, render_size), (0, 0, 0, 0))
    output_image.paste(image, (0, 0), mask=mask)

    output_image = output_image.resize((size, size), resample=Image.Resampling.LANCZOS)
    output_image.save(output)
    print(f"Success! Saved avatar to: {output}")

# --- UPDATED MAIN FOR CLI ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Google-style initial avatar.")
    
    # Positional arguments
    parser.add_argument("text", help="The character(s) to display in the avatar")
    parser.add_argument("color", help="The background color (Hex or name, e.g., '#1A2421')")
    
    # Optional arguments
    parser.add_argument("--out", default="avatar.png", help="The output filename (default: avatar.png)")
    parser.add_argument("--size", type=int, default=500, help="Final image size in pixels")
    parser.add_argument("--scale", type=float, default=0.52, help="Font scale factor")

    args = parser.parse_args()

    # Call the function using the CLI arguments
    generate_avatar(
        text=args.text, 
        color=args.color, 
        output=args.out, 
        size=args.size, 
        scale=args.scale
    )