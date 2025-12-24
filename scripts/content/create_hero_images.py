"""
Generate hero images for Terraform + Azure DevOps CI/CD blog series
Creates 1200x630px images with Azure blue gradient backgrounds and text overlays
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

# Image specifications
WIDTH = 1200
HEIGHT = 630

# Azure color palette
AZURE_BLUE = '#0078D4'
AZURE_DARK_BLUE = '#003D7A'
TERRAFORM_PURPLE = '#844FBA'
WHITE = '#FFFFFF'
LIGHT_GRAY = '#F3F2F1'

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

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def add_text_with_outline(draw, text, position, font, fill_color, outline_color, outline_width=2):
    """Add text with outline for better readability"""
    x, y = position
    # Draw outline
    for adj_x in range(-outline_width, outline_width + 1):
        for adj_y in range(-outline_width, outline_width + 1):
            draw.text((x + adj_x, y + adj_y), text, font=font, fill=outline_color)
    # Draw main text
    draw.text(position, text, font=font, fill=fill_color)

def create_hero_image(title, subtitle, filename, accent_color=TERRAFORM_PURPLE):
    """Create a hero image with title and subtitle"""
    # Create gradient background
    img = create_gradient_background(WIDTH, HEIGHT, hex_to_rgb(AZURE_DARK_BLUE), hex_to_rgb(AZURE_BLUE))
    
    # Add a subtle pattern overlay
    overlay = Image.new('RGBA', (WIDTH, HEIGHT), (255, 255, 255, 10))
    draw_overlay = ImageDraw.Draw(overlay)
    for i in range(0, WIDTH, 40):
        draw_overlay.line([(i, 0), (i + HEIGHT, HEIGHT)], fill=(255, 255, 255, 20), width=1)
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    
    draw = ImageDraw.Draw(img)
    
    # Try to load fonts, fall back to default if not available
    try:
        title_font = ImageFont.truetype("arial.ttf", 60)
        subtitle_font = ImageFont.truetype("arial.ttf", 32)
        label_font = ImageFont.truetype("arialbd.ttf", 24)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
    
    # Add "Azure Noob" branding in top left
    draw.text((40, 40), "Azure Noob", font=label_font, fill=WHITE)
    
    # Add decorative line with accent color
    draw.rectangle([(40, 90), (400, 95)], fill=hex_to_rgb(accent_color))
    
    # Add title (centered vertically)
    title_y = HEIGHT // 2 - 80
    
    # Word wrap title if needed
    words = title.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=title_font)
        if bbox[2] - bbox[0] < WIDTH - 100:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    
    # Draw title lines
    y_offset = title_y
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (WIDTH - text_width) // 2
        add_text_with_outline(draw, line, (x, y_offset), title_font, WHITE, hex_to_rgb(AZURE_DARK_BLUE), 3)
        y_offset += 70
    
    # Add subtitle
    if subtitle:
        bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        subtitle_width = bbox[2] - bbox[0]
        subtitle_x = (WIDTH - subtitle_width) // 2
        subtitle_y = y_offset + 20
        draw.text((subtitle_x, subtitle_y), subtitle, font=subtitle_font, fill=LIGHT_GRAY)
    
    # Add Terraform logo placeholder (colored rectangle)
    logo_size = 60
    logo_x = WIDTH - logo_size - 40
    logo_y = HEIGHT - logo_size - 40
    draw.rectangle([(logo_x, logo_y), (logo_x + logo_size, logo_y + logo_size)], 
                   fill=hex_to_rgb(TERRAFORM_PURPLE), outline=WHITE, width=2)
    
    # Save image
    output_dir = "static/images/hero"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    img.save(output_path, 'PNG', quality=95)
    print(f"✓ Created: {output_path}")
    return output_path

def main():
    """Generate all hero images for the blog series"""
    print("Generating hero images for Terraform + Azure DevOps CI/CD series...")
    print()
    
    images = [
        {
            "title": "Enterprise Terraform CI/CD",
            "subtitle": "Complete 6-Part Series",
            "filename": "terraform-devops-series-index.png"
        },
        {
            "title": "Part 1: Prerequisites",
            "subtitle": "Foundation & Architecture",
            "filename": "terraform-devops-part1.png"
        },
        {
            "title": "Part 2: Build Pipelines",
            "subtitle": "Status Checks & Plan Creation",
            "filename": "terraform-devops-part2.png"
        },
        {
            "title": "Part 3: Release Pipeline",
            "subtitle": "Deployment & Approval Gates",
            "filename": "terraform-devops-part3.png"
        },
        {
            "title": "Part 4: Branch Policies",
            "subtitle": "GitOps Enforcement",
            "filename": "terraform-devops-part4.png"
        },
        {
            "title": "Part 5: Production Setup",
            "subtitle": "Multi-Environment Best Practices",
            "filename": "terraform-devops-part5.png"
        },
        {
            "title": "Part 6: Troubleshooting",
            "subtitle": "Real Production Issues & Solutions",
            "filename": "terraform-devops-part6.png"
        }
    ]
    
    for img_config in images:
        create_hero_image(
            title=img_config["title"],
            subtitle=img_config["subtitle"],
            filename=img_config["filename"]
        )
    
    print()
    print(f"✓ All {len(images)} hero images created successfully!")
    print(f"✓ Location: static/images/hero/")
    print()
    print("Next steps:")
    print("1. Review the generated images")
    print("2. Run: python freeze.py")
    print("3. Commit and push:")
    print("   git add static/images/hero posts")
    print("   git commit -m 'Add hero images for Terraform CI/CD series'")
    print("   git push origin main")

if __name__ == "__main__":
    main()
