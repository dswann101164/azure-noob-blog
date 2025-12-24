from PIL import Image, ImageDraw, ImageFont

# Create image
width, height = 1200, 630
img = Image.new('RGB', (width, height), color='#0F172A')
draw = ImageDraw.Draw(img)

# Try to load a font, fallback to default if not available
try:
    title_font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 60)
    subtitle_font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 36)
    label_font = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 32)
    desc_font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 24)
except:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    label_font = ImageFont.load_default()
    desc_font = ImageFont.load_default()

# Title at top
title = 'The Three AI Operations Roles'
title_bbox = draw.textbbox((0, 0), title, font=title_font)
title_width = title_bbox[2] - title_bbox[0]
draw.text(((width - title_width) / 2, 40), title, fill='#F1F5F9', font=title_font)

subtitle = "That Don't Exist Yet"
subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
draw.text(((width - subtitle_width) / 2, 120), subtitle, fill='#94A3B8', font=subtitle_font)

# Three role boxes
box_width = 320
box_height = 300
box_spacing = 40
start_x = (width - (box_width * 3 + box_spacing * 2)) / 2
start_y = 200

roles = [
    {'title': 'AI Admin', 'color': '#3B82F6', 'items': ['Make Tools Work', 'Train Teams', 'Build Workflows']},
    {'title': 'AI Security', 'color': '#EF4444', 'items': ['Monitor Usage', 'Prevent Risks', 'Enforce Policy']},
    {'title': 'AI Analyst', 'color': '#10B981', 'items': ['Measure ROI', 'Find Patterns', 'Report Value']}
]

for i, role in enumerate(roles):
    x = start_x + (box_width + box_spacing) * i
    y = start_y
    draw.rectangle([x, y, x + box_width, y + box_height], fill='#1E293B', outline=role['color'], width=3)
    draw.rectangle([x, y, x + box_width, y + 8], fill=role['color'])
    title_text = role['title']
    title_bbox = draw.textbbox((0, 0), title_text, font=label_font)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text((x + (box_width - title_w) / 2, y + 30), title_text, fill='#F1F5F9', font=label_font)
    item_y = y + 90
    for item in role['items']:
        item_bbox = draw.textbbox((0, 0), f'• {item}', font=desc_font)
        item_w = item_bbox[2] - item_bbox[0]
        draw.text((x + (box_width - item_w) / 2, item_y), f'• {item}', fill='#94A3B8', font=desc_font)
        item_y += 50

# Bottom text
bottom_text = '12-24 Month Window to Position Yourself'
bottom_bbox = draw.textbbox((0, 0), bottom_text, font=subtitle_font)
bottom_width = bottom_bbox[2] - bottom_bbox[0]
draw.text(((width - bottom_width) / 2, height - 80), bottom_text, fill='#F59E0B', font=subtitle_font)

# Save
img.save('C:/Users/dswann/Documents/GitHub/azure-noob-blog/static/images/hero/three-ai-roles.png')
print('Hero image created successfully at: static/images/hero/three-ai-roles.png')
