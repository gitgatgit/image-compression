def generate_avatar(text, color, size=500, output="avatar.png", font_path=None, scale=0.52):
    # 1. Render at 2x for smooth edges (Super-sampling)
    render_size = size * 2 
    image = Image.new('RGB', (render_size, render_size), color)
    draw = ImageDraw.Draw(image)

    # 2. Font Scaling (Google uses ~0.52 for that specific 'N' look)
    font_size = int(render_size * scale)
    font = get_font(font_size, font_path)

    # 3. Precision Centering
    # We calculate based on the 'cap-height' to avoid it looking "sunken"
    left, top, right, bottom = draw.textbbox((0, 0), text.upper(), font=font)
    text_width = right - left
    text_height = bottom - top
    
    # Mathematical center minus the font's internal offset
    x = (render_size - text_width) // 2 - left
    y = (render_size - text_height) // 2 - top

    draw.text((x, y), text.upper(), fill="white", font=font)

    # 4. Circle Mask
    mask = Image.new('L', (render_size, render_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, render_size, render_size), fill=255)
    
    output_image = Image.new('RGBA', (render_size, render_size), (0, 0, 0, 0))
    output_image.paste(image, (0, 0), mask=mask)

    # 5. Downscale to final size
    output_image = output_image.resize((size, size), resample=Image.Resampling.LANCZOS)
    output_image.save(output)
    print(f"Success! Match complete.")
