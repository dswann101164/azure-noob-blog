from PIL import Image, ImageDraw, ImageFont
import os

# Image dimensions
width = 1200
height = 630

# Create base image with gradient background
img = Image.new('RGB', (width, height), '#0F172A')
draw = ImageDraw.Draw(img)

# Create gradient effect
for i in range(height):
    # Gradient from dark blue to slightly lighter blue
    r = int(15 + (i / height) * 10)
    g = int(23 + (i / height) * 15)
    b = int(42 + (i / height) * 20)
    draw.rectangle([(0, i), (width, i+1)], fill=(r, g, b))

# Try to load fonts, fallback to default if not available
try:
    title_font = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 72)
    subtitle_font = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 36)
    small_font = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 28)
except:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    small_font = ImageFont.load_default()

# Main title - centered with tool names
title_lines = [
    "Portal • CLI • PowerShell",
    "Bicep • Terraform"
]

y_offset = 120
for line in title_lines:
    bbox = draw.textbbox((0, 0), line, font=title_font)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    
    # Draw text shadow
    draw.text((x+3, y_offset+3), line, font=title_font, fill='#000000')
    # Draw main text with Azure blue
    draw.text((x, y_offset), line, font=title_font, fill='#0078D4')
    y_offset += 90

# Subtitle
subtitle = "Which One Should a Noob Learn First?"
bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
text_width = bbox[2] - bbox[0]
x = (width - text_width) // 2
y_offset += 40

# Draw subtitle shadow
draw.text((x+2, y_offset+2), subtitle, font=subtitle_font, fill='#000000')
# Draw subtitle with white
draw.text((x, y_offset), subtitle, font=subtitle_font, fill='#FFFFFF')

# Bottom text with recommendation
y_offset += 100
recommendation = "START: Portal → CLI → Bicep OR Terraform"
bbox = draw.textbbox((0, 0), recommendation, font=small_font)
text_width = bbox[2] - bbox[0]
x = (width - text_width) // 2

# Draw rectangle background for bottom text
padding = 20
draw.rectangle(
    [(x - padding, y_offset - padding), 
     (x + text_width + padding, y_offset + 40 + padding)], 
    fill='#0078D4'
)

# Draw recommendation text
draw.text((x, y_offset), recommendation, font=small_font, fill='#FFFFFF')

# Bottom branding
branding = "azure-noob.com"
bbox = draw.textbbox((0, 0), branding, font=small_font)
text_width = bbox[2] - bbox[0]
x = (width - text_width) // 2
y_offset = height - 60

draw.text((x, y_offset), branding, font=small_font, fill='#64748B')

# Add decorative elements - tool icons representation
# Portal icon (browser window)
draw.rectangle([(100, 280), (200, 350)], outline='#0078D4', width=3)
draw.rectangle([(100, 280), (200, 305)], fill='#0078D4')

# CLI icon (terminal)
draw.rectangle([(900, 280), (1050, 350)], outline='#10B981', width=3)
draw.line([(920, 310), (940, 325), (920, 340)], fill='#10B981', width=3)
draw.text((960, 305), ">_", font=subtitle_font, fill='#10B981')

# Code icon (IaC representation)
draw.rectangle([(480, 500), (720, 580)], outline='#F59E0B', width=3)
draw.text((500, 515), "{  }", font=title_font, fill='#F59E0B')

# Ensure output directory exists
output_dir = "C:\\Users\\dswann\\Documents\\GitHub\\azure-noob-blog\\static\\images\\hero"
os.makedirs(output_dir, exist_ok=True)

# Save the image
output_path = os.path.join(output_dir, "azure-tool-selection-noobs.png")
img.save(output_path, 'PNG', optimize=True)

print(f"Hero image created successfully: {output_path}")
print(f"Image size: {width}x{height}")
