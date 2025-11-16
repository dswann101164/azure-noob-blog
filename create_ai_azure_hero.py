"""
Generate hero image for AI replacing Azure admins blog post
Creates 1200x630px image showing the skills gap
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Image specifications
WIDTH = 1200
HEIGHT = 630

# Colors
AZURE_BLUE = '#0078D4'
AZURE_DARK_BLUE = '#003D7A'
AI_PURPLE = '#7B2CBF'
WHITE = '#FFFFFF'
LIGHT_GRAY = '#F3F2F1'
WARNING_ORANGE = '#FF6B35'

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_gradient_background(width, height, color1, color2):
    """Create a gradient background from color1 to color2"""
    base = Image.new('RGB', (width, height), color1)
    top = Image.new('RGB', (width, height), color2)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        for x in range(width):
            mask_data.append(int(255 * (y / height)))
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

def add_text_with_shadow(draw, text, position, font, fill_color, shadow_color=(0, 0, 0, 128)):
    """Add text with drop shadow"""
    x, y = position
    draw.text((x + 3, y + 3), text, font=font, fill=shadow_color)
    draw.text(position, text, font=font, fill=fill_color)

def create_hero_image():
    """Create hero image showing skills gap"""
    # Create gradient background
    img = create_gradient_background(WIDTH, HEIGHT, hex_to_rgb(AZURE_DARK_BLUE), hex_to_rgb(AZURE_BLUE))
    draw = ImageDraw.Draw(img)
    
    # Load fonts
    try:
        title_font = ImageFont.truetype("arial.ttf", 68)
        subtitle_font = ImageFont.truetype("arial.ttf", 32)
        label_font = ImageFont.truetype("arialbd.ttf", 26)
        big_font = ImageFont.truetype("arialbd.ttf", 90)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
        big_font = ImageFont.load_default()
    
    # Add "Azure Noob" branding
    draw.text((40, 40), "Azure Noob", font=label_font, fill=WHITE)
    
    # Add decorative line
    draw.rectangle([(40, 85), (300, 92)], fill=hex_to_rgb(AI_PURPLE))
    
    # Split image: LEFT = What's taught, RIGHT = What's needed
    center_x = WIDTH // 2
    
    # Draw vertical divider
    draw.rectangle([(center_x - 2, 120), (center_x + 2, HEIGHT - 80)], fill=WHITE)
    
    # LEFT SIDE: What's Being Taught
    left_x = 80
    draw.text((left_x, 140), "TAUGHT:", font=label_font, fill=WHITE)
    
    skills_y = 200
    skills_list = [
        "PowerShell",
        "Networking", 
        "Security",
        "VMs"
    ]
    
    for skill in skills_list:
        draw.text((left_x, skills_y), f"✓ {skill}", font=subtitle_font, fill=LIGHT_GRAY)
        skills_y += 50
    
    # Missing skill with warning
    draw.text((left_x, skills_y + 30), "✗ AI Capability", font=subtitle_font, fill=hex_to_rgb(WARNING_ORANGE))
    
    # RIGHT SIDE: What Companies Need
    right_x = center_x + 80
    draw.text((right_x, 140), "NEEDED:", font=label_font, fill=WHITE)
    
    needs_y = 200
    draw.text((right_x, needs_y), "Azure +", font=subtitle_font, fill=LIGHT_GRAY)
    draw.text((right_x, needs_y + 80), "AI Skills", font=big_font, fill=WHITE)
    
    # Add emphasis
    draw.text((right_x, needs_y + 200), "= New Job", font=subtitle_font, fill=LIGHT_GRAY)
    
    # Main title at bottom
    title_text = "The Skills Gap"
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    text_width = bbox[2] - bbox[0]
    title_x = (WIDTH - text_width) // 2
    title_y = HEIGHT - 120
    
    add_text_with_shadow(draw, title_text, (title_x, title_y), title_font, WHITE)
    
    # Subtitle
    subtitle_text = "Nobody Is Teaching Azure + AI"
    bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
    subtitle_width = bbox[2] - bbox[0]
    subtitle_x = (WIDTH - subtitle_width) // 2
    subtitle_y = title_y + 75
    draw.text((subtitle_x, subtitle_y), subtitle_text, font=subtitle_font, fill=LIGHT_GRAY)
    
    # Save image
    output_dir = "static/images/hero"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "ai-replacing-azure-admins.png")
    img.save(output_path, 'PNG', quality=95)
    print(f"✓ Created: {output_path}")
    return output_path

if __name__ == "__main__":
    print("Generating hero image for AI + Azure skills gap post...")
    create_hero_image()
    print("\n✓ Hero image created!")
    print("\nNext step: python freeze.py")
