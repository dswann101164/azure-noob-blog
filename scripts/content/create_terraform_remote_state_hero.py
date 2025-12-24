"""
Generate hero image for Terraform Remote State blog post
Creates 1200x630px image with "chaos to order" theme
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Image specifications
WIDTH = 1200
HEIGHT = 630

# Colors
AZURE_BLUE = '#0078D4'
AZURE_DARK_BLUE = '#003D7A'
TERRAFORM_PURPLE = '#844FBA'
CHAOS_RED = '#D13438'
SUCCESS_GREEN = '#107C10'
WHITE = '#FFFFFF'
LIGHT_GRAY = '#F3F2F1'

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
    """Add text with drop shadow for better readability"""
    x, y = position
    # Draw shadow
    draw.text((x + 3, y + 3), text, font=font, fill=shadow_color)
    # Draw main text
    draw.text(position, text, font=font, fill=fill_color)

def create_hero_image():
    """Create the hero image for Terraform Remote State post"""
    # Create gradient background (Azure blue)
    img = create_gradient_background(WIDTH, HEIGHT, hex_to_rgb(AZURE_DARK_BLUE), hex_to_rgb(AZURE_BLUE))
    draw = ImageDraw.Draw(img)
    
    # Load fonts
    try:
        title_font = ImageFont.truetype("arial.ttf", 72)
        subtitle_font = ImageFont.truetype("arial.ttf", 36)
        label_font = ImageFont.truetype("arialbd.ttf", 28)
        emoji_font = ImageFont.truetype("seguiemj.ttf", 80)  # Windows emoji font
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
        emoji_font = ImageFont.load_default()
    
    # Add "Azure Noob" branding in top left
    draw.text((40, 40), "Azure Noob", font=label_font, fill=WHITE)
    
    # Add decorative line
    draw.rectangle([(40, 85), (300, 92)], fill=hex_to_rgb(TERRAFORM_PURPLE))
    
    # Split the image into Before/After sections visually
    center_x = WIDTH // 2
    
    # Draw vertical divider line
    draw.rectangle([(center_x - 3, 120), (center_x + 3, HEIGHT - 80)], fill=WHITE)
    
    # LEFT SIDE: CHAOS (Before)
    chaos_x = center_x // 2
    
    # "BEFORE" label
    add_text_with_shadow(draw, "BEFORE", (60, 140), label_font, hex_to_rgb(CHAOS_RED))
    
    # Chaos elements (emoji-style representation)
    try:
        draw.text((chaos_x - 40, 220), "💥", font=emoji_font, fill=WHITE)
        draw.text((chaos_x - 80, 320), "💻", font=emoji_font, fill=WHITE)
        draw.text((chaos_x, 320), "⚠️", font=emoji_font, fill=WHITE)
        draw.text((chaos_x - 40, 420), "🔥", font=emoji_font, fill=WHITE)
    except:
        # Fallback text if emoji font doesn't work
        draw.text((80, 240), "State Conflicts", font=subtitle_font, fill=hex_to_rgb(CHAOS_RED))
        draw.text((80, 300), "Lost Files", font=subtitle_font, fill=hex_to_rgb(CHAOS_RED))
        draw.text((80, 360), "2 AM Pages", font=subtitle_font, fill=hex_to_rgb(CHAOS_RED))
        draw.text((80, 420), "No Backups", font=subtitle_font, fill=hex_to_rgb(CHAOS_RED))
    
    # RIGHT SIDE: ORDER (After)
    order_x = center_x + (center_x // 2)
    
    # "AFTER" label
    add_text_with_shadow(draw, "AFTER", (center_x + 60, 140), label_font, hex_to_rgb(SUCCESS_GREEN))
    
    # Order elements
    try:
        draw.text((order_x - 40, 220), "☁️", font=emoji_font, fill=WHITE)
        draw.text((order_x - 80, 320), "🔒", font=emoji_font, fill=WHITE)
        draw.text((order_x, 320), "✅", font=emoji_font, fill=WHITE)
        draw.text((order_x - 40, 420), "😴", font=emoji_font, fill=WHITE)
    except:
        # Fallback text
        draw.text((center_x + 60, 240), "Remote State", font=subtitle_font, fill=hex_to_rgb(SUCCESS_GREEN))
        draw.text((center_x + 60, 300), "State Locking", font=subtitle_font, fill=hex_to_rgb(SUCCESS_GREEN))
        draw.text((center_x + 60, 360), "Auto Backups", font=subtitle_font, fill=hex_to_rgb(SUCCESS_GREEN))
        draw.text((center_x + 60, 420), "Sleep Better", font=subtitle_font, fill=hex_to_rgb(SUCCESS_GREEN))
    
    # Main title at bottom
    title_text = "Terraform Remote State"
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    text_width = bbox[2] - bbox[0]
    title_x = (WIDTH - text_width) // 2
    title_y = HEIGHT - 120
    
    # Add shadow and title
    add_text_with_shadow(draw, title_text, (title_x, title_y), title_font, WHITE)
    
    # Subtitle
    subtitle_text = "30 Minutes to Zero State Disasters"
    bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
    subtitle_width = bbox[2] - bbox[0]
    subtitle_x = (WIDTH - subtitle_width) // 2
    subtitle_y = title_y + 80
    draw.text((subtitle_x, subtitle_y), subtitle_text, font=subtitle_font, fill=LIGHT_GRAY)
    
    # Save image
    output_dir = "static/images/hero"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "terraform-remote-state.png")
    img.save(output_path, 'PNG', quality=95)
    print(f"✓ Created: {output_path}")
    return output_path

if __name__ == "__main__":
    print("Generating hero image for Terraform Remote State post...")
    create_hero_image()
    print("\n✓ Hero image created successfully!")
    print("\nNext steps:")
    print("1. Review: static/images/hero/terraform-remote-state.png")
    print("2. Test locally: python app.py")
    print("3. Deploy: python freeze.py && git add . && git commit -m 'Add Terraform Remote State post' && git push")
