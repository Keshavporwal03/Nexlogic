import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

tpl = Image.open('app/static/reference_template.png').convert('RGBA')
w, h = 1400, 940
img = tpl.resize((w, h), Image.Resampling.LANCZOS)
draw = ImageDraw.Draw(img)

# Clear middle job card region with exact matching color (241, 242, 242)
bg_fill = (241, 242, 242, 255)
# Middle card box
draw.rectangle([int(w * 0.38), int(h * 0.19), int(w * 0.71), int(h * 0.69)], fill=bg_fill)

# Left subtitle box
draw.rectangle([int(w * 0.04), int(h * 0.46), int(w * 0.36), int(h * 0.57)], fill=bg_fill)

# Footer contact boxes
draw.rectangle([int(w * 0.10), int(h * 0.93), int(w * 0.32), int(h * 0.98)], fill=(24, 24, 27, 255))
draw.rectangle([int(w * 0.42), int(h * 0.93), int(w * 0.62), int(h * 0.98)], fill=(24, 24, 27, 255))

font_dir = 'app/static/fonts'
font_title = ImageFont.truetype(os.path.join(font_dir, 'Montserrat-Bold.ttf'), 20)
font_bold = ImageFont.truetype(os.path.join(font_dir, 'Montserrat-Bold.ttf'), 14)
font_bold_sm = ImageFont.truetype(os.path.join(font_dir, 'Montserrat-Bold.ttf'), 12)
font_reg_sm = ImageFont.truetype(os.path.join(font_dir, 'Montserrat-Regular.ttf'), 12)
font_tagline = ImageFont.truetype(os.path.join(font_dir, 'Montserrat-Bold.ttf'), 17)
font_foot = ImageFont.truetype(os.path.join(font_dir, 'Montserrat-Bold.ttf'), 20)

# Left Subtitle
tagline = 'Exciting opportunities for experienced cybersecurity professionals to join our prestigious AP SOC Project.'
wrapped = textwrap.fill(tagline, width=32)
ty = int(h * 0.47)
for line in wrapped.split('\n'):
    draw.text((int(w * 0.04), ty), line, fill='#374151', font=font_tagline)
    ty += 24

# Middle Role 1
col2_x = int(w * 0.39)
icons_dir = 'app/static/icons'
cs_ic = Image.open(os.path.join(icons_dir, 'clipboard_lines.png')).convert('RGBA')
cs_ic.thumbnail((50, 50))
img.paste(cs_ic, (col2_x, int(h * 0.20)), cs_ic)

draw.text((col2_x + 60, int(h * 0.20)), '1. PROJECT MANAGER –', fill='#18181B', font=font_title)
draw.text((col2_x + 80, int(h * 0.23)), 'CYBER AUDIT – GRC SPECIALIST', fill='#18181B', font=font_title)

by = int(h * 0.27)
draw.text((col2_x + 60, by), '• Experience:', fill='#111827', font=font_bold_sm)
draw.text((col2_x + 160, by), '10+ Years', fill='#4B5563', font=font_reg_sm)
by += 24

draw.text((col2_x + 60, by), '• Qualification:', fill='#111827', font=font_bold_sm)
draw.text((col2_x + 170, by), 'B.Tech / M.Tech', fill='#4B5563', font=font_reg_sm)
by += 18
draw.text((col2_x + 70, by), '(Electronics, Computer Science, Electrical, Cybersecurity)', fill='#6B7280', font=font_reg_sm)
by += 24

draw.text((col2_x + 60, by), '• Certifications:', fill='#111827', font=font_bold_sm)
draw.text((col2_x + 175, by), 'CISA / CISSP / CISM', fill='#4B5563', font=font_reg_sm)

# Middle Role 2
by2 = int(h * 0.44)
ml_ic = Image.open(os.path.join(icons_dir, 'monitor_lock.png')).convert('RGBA')
ml_ic.thumbnail((50, 50))
img.paste(ml_ic, (col2_x, by2), ml_ic)

draw.text((col2_x + 60, by2 + 2), '2. SOC MANAGER', fill='#18181B', font=font_title)
by = by2 + 34

draw.text((col2_x + 60, by), '• Experience:', fill='#111827', font=font_bold_sm)
draw.text((col2_x + 160, by), '10+ Years', fill='#4B5563', font=font_reg_sm)
by += 24

draw.text((col2_x + 60, by), '• Qualification:', fill='#111827', font=font_bold_sm)
draw.text((col2_x + 170, by), "Bachelor's / Master's", fill='#4B5563', font=font_reg_sm)
by += 18
draw.text((col2_x + 70, by), '(Computer Science, IT, Cybersecurity or related field)', fill='#6B7280', font=font_reg_sm)
by += 24

draw.text((col2_x + 60, by), '• Certifications (Preferred):', fill='#111827', font=font_bold_sm)
by += 18
draw.text((col2_x + 70, by), 'GCIA / GCFA / GCIH / GCFE / CEH / ECIH / Security+ / CySA+', fill='#4B5563', font=font_reg_sm)
by += 18
draw.text((col2_x + 70, by), 'Vendor Certifications (CrowdStrike, Splunk, QRadar, etc.)', fill='#6B7280', font=font_reg_sm)

# Footer links
draw.text((int(w * 0.105), int(h * 0.935)), 'www.nexlogic.co.in', fill='#8E9F76', font=font_foot)
draw.text((int(w * 0.425), int(h * 0.935)), 'hr@naxlogic.com', fill='#8E9F76', font=font_foot)

os.makedirs('generated_previews', exist_ok=True)
img.save('generated_previews/test_hybrid.png')
print('Hybrid banner saved successfully!')
