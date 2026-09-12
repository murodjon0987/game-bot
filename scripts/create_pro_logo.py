import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_circular_gaming_logo(output_path="murodjon_logo.jpg"):
    # 1024x1024 ultra-high resolution
    size = 1024
    img = Image.new("RGBA", (size, size), (11, 14, 23, 255))
    draw = ImageDraw.Draw(img)

    # 1. Radial Dark Cosmic Background
    center = size // 2
    for r in range(center, 0, -2):
        factor = r / center
        # Gradient from deep dark navy #090B14 to glowing midnight cyan-indigo #131A30
        red = int(10 + (1 - factor) * 15)
        green = int(14 + (1 - factor) * 28)
        blue = int(26 + (1 - factor) * 50)
        draw.ellipse([center - r, center - r, center + r, center + r], fill=(red, green, blue, 255))

    # 2. Outer Glowing Neon Ring (Cyan / Magenta)
    ring_radius = 460
    # Glow layers
    for glow in range(25, 0, -2):
        alpha = int((1 - glow / 25) * 80)
        draw.ellipse(
            [center - ring_radius - glow, center - ring_radius - glow, 
             center + ring_radius + glow, center + ring_radius + glow],
            outline=(0, 229, 255, alpha),
            width=3
        )
    # Sharp Core Ring
    draw.ellipse(
        [center - ring_radius, center - ring_radius, center + ring_radius, center + ring_radius],
        outline=(0, 240, 255, 255),
        width=8
    )
    # Secondary Gold Accent Ring
    draw.ellipse(
        [center - ring_radius + 15, center - ring_radius + 15, center + ring_radius - 15, center + ring_radius - 15],
        outline=(255, 185, 0, 180),
        width=3
    )

    # 3. Geometric Tech Circuit Accent Lines
    for angle_deg in range(0, 360, 30):
        rad = math.radians(angle_deg)
        x1 = center + int((ring_radius - 40) * math.cos(rad))
        y1 = center + int((ring_radius - 40) * math.sin(rad))
        x2 = center + int((ring_radius - 20) * math.cos(rad))
        y2 = center + int((ring_radius - 20) * math.sin(rad))
        draw.line([(x1, y1), (x2, y2)], fill=(0, 240, 255, 200), width=4)

    # 4. Central Shield / Crest Base
    crest_pts = [
        (center - 240, center - 200),
        (center + 240, center - 200),
        (center + 210, center + 100),
        (center, center + 270),
        (center - 210, center + 100)
    ]
    # Crest Shadow & Glow
    draw.polygon(crest_pts, fill=(16, 22, 38, 255), outline=(0, 229, 255, 255))
    # Inner metallic bevel crest
    inner_crest = [
        (center - 220, center - 180),
        (center + 220, center - 180),
        (center + 190, center + 85),
        (center, center + 245),
        (center - 190, center + 85)
    ]
    draw.polygon(inner_crest, fill=(22, 30, 52, 255), outline=(255, 190, 0, 220))

    # 5. Glowing 3D "M" Monogram with Golden Crown
    # Draw Golden Crown at top of Crest
    crown_y = center - 170
    crown_pts = [
        (center - 90, crown_y),
        (center - 120, crown_y - 65),
        (center - 40, crown_y - 35),
        (center, crown_y - 85),
        (center + 40, crown_y - 35),
        (center + 120, crown_y - 65),
        (center + 90, crown_y)
    ]
    draw.polygon(crown_pts, fill=(255, 195, 0, 255), outline=(255, 240, 150, 255))
    # Crown jewels
    draw.ellipse([center - 125, crown_y - 75, center - 115, crown_y - 65], fill=(0, 240, 255, 255))
    draw.ellipse([center - 7, crown_y - 95, center + 7, crown_y - 81], fill=(0, 240, 255, 255))
    draw.ellipse([center + 115, crown_y - 75, center + 125, crown_y - 65], fill=(0, 240, 255, 255))

    # 6. Sleek Modern Gamepad Body (Cyber Controller)
    pad_y = center - 30
    pad_box = [center - 180, pad_y - 90, center + 180, pad_y + 90]
    draw.rounded_rectangle(pad_box, radius=55, fill=(12, 17, 30, 255), outline=(0, 229, 255, 255), width=6)
    
    # Controller Grips
    draw.polygon([(center - 170, pad_y + 40), (center - 190, pad_y + 140), (center - 110, pad_y + 125), (center - 110, pad_y + 50)], fill=(15, 22, 38, 255), outline=(0, 229, 255, 255))
    draw.polygon([(center + 170, pad_y + 40), (center + 190, pad_y + 140), (center + 110, pad_y + 125), (center + 110, pad_y + 50)], fill=(15, 22, 38, 255), outline=(0, 229, 255, 255))

    # D-Pad (Left)
    d_x, d_y = center - 100, pad_y
    draw.rectangle([d_x - 12, d_y - 35, d_x + 12, d_y + 35], fill=(0, 240, 255, 255))
    draw.rectangle([d_x - 35, d_y - 12, d_x + 35, d_y + 12], fill=(0, 240, 255, 255))

    # Action Buttons (Right: ABXY)
    b_x, b_y = center + 100, pad_y
    btn_colors = [(255, 75, 75), (75, 255, 120), (75, 160, 255), (255, 215, 0)]
    coords = [(b_x, b_y - 25), (b_x + 25, b_y), (b_x, b_y + 25), (b_x - 25, b_y)]
    for (cx, cy), col in zip(coords, btn_colors):
        draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=col)

    # Glowing Center Power Button (Neon Cyan)
    draw.ellipse([center - 28, pad_y - 28, center + 28, pad_y + 28], fill=(0, 240, 255, 255), outline=(255, 255, 255, 255), width=3)

    # 7. Big Sculpted 3D "M" Emblem
    m_y = center + 70
    m_pts = [
        (center - 130, m_y + 80),
        (center - 130, m_y - 10),
        (center - 70, m_y - 10),
        (center, m_y + 55),
        (center + 70, m_y - 10),
        (center + 130, m_y - 10),
        (center + 130, m_y + 80),
        (center + 90, m_y + 80),
        (center + 90, m_y + 25),
        (center, m_y + 95),
        (center - 90, m_y + 25),
        (center - 90, m_y + 80),
    ]
    # M Shadow/Glow
    draw.polygon(m_pts, fill=(255, 185, 0, 255), outline=(255, 240, 150, 255))

    # 8. Ribbon Banner with "MURODJON GAME BOT"
    banner_y = center + 270
    banner_w = 410
    banner_h = 76
    banner_rect = [center - banner_w, banner_y, center + banner_w, banner_y + banner_h]
    # Banner background
    draw.rounded_rectangle(banner_rect, radius=20, fill=(7, 10, 18, 255), outline=(0, 240, 255, 255), width=5)
    
    # Banner Text using default or clean font
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 46)
        font_sub = ImageFont.truetype("arialbd.ttf", 26)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    title_text = "MURODJON GAME BOT"
    sub_text = "OFFICIAL TELEGRAM BOT"

    # Text measurement & centering
    t_bbox = draw.textbbox((0, 0), title_text, font=font_title)
    t_w = t_bbox[2] - t_bbox[0]
    draw.text((center - t_w // 2, banner_y + 12), title_text, font=font_title, fill=(255, 255, 255, 255))

    # Small VIP badge under banner
    badge_rect = [center - 130, banner_y + banner_h + 8, center + 130, banner_y + banner_h + 46]
    draw.rounded_rectangle(badge_rect, radius=12, fill=(255, 185, 0, 255), outline=(255, 240, 150, 255), width=2)
    s_bbox = draw.textbbox((0, 0), "VIP EDITION", font=font_sub)
    s_w = s_bbox[2] - s_bbox[0]
    draw.text((center - s_w // 2, banner_y + banner_h + 12), "VIP EDITION", font=font_sub, fill=(10, 10, 15, 255))

    # Final RGB conversion
    rgb_img = img.convert("RGB")
    rgb_img.save(output_path, quality=98)
    print(f"Professional circular logo created: {output_path}")

if __name__ == "__main__":
    create_circular_gaming_logo("murodjon_logo.jpg")
    create_circular_gaming_logo("murodjon_pro_logo.jpg")
