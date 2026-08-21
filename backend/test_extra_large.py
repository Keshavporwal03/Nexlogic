import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

def make_white_transparent(img):
    if not img: return None
    img = img.convert('RGBA')
    data = img.getdata()
    new_data = []
    for item in data:
        if item[0] > 235 and item[1] > 235 and item[2] > 235:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    img.putdata(new_data)
    return img

tpl_path = 'app/static/user_exact_template.png'
raw_tpl = Image.open(tpl_path).convert('RGBA')
target_w = 1400
target_h = int(raw_tpl.height * (target_w / raw_tpl.width))
img = raw_tpl.resize((target_w, target_h), Image.Resampling.LANCZOS)
w, h = img.size
draw = ImageDraw.Draw(img)

# Exact background color
bg_fill = img.getpixel((int(w * 0.50), int(h * 0.15)))

# 1. Clean logo area ONLY (top 172px, x=0 to x=545)
draw.rectangle([0, 0, 545, 172], fill=bg_fill)
draw.rectangle([480, 160, 535, 215], fill=bg_fill)
draw.rectangle([460, 460, 520, 485], fill=bg_fill)

for r in range(7):
    for c in range(5):
        draw.ellipse([24 + c * 14, 22 + r * 14, 28 + c * 14, 26 + r * 14], fill='#CBD5E1')

logo_path = 'app/static/company-logo.png'
c_logo = Image.open(logo_path)
bbox = c_logo.getbbox()
if bbox: c_logo = c_logo.crop(bbox)
c_logo = make_white_transparent(c_logo)
c_logo.thumbnail((440, 125), Image.Resampling.LANCZOS)
img.paste(c_logo, (55, 32), c_logo)

# 2. Clean middle job card region (from x=475 to x=1030, y=170 to y=655)
draw.rectangle([475, 170, 1030, 655], fill=bg_fill)

# 3. Clean left subtitle area completely (from x=20 to x=475, y=400 to y=575)
draw.rectangle([20, 400, 475, 575], fill=bg_fill)

font_dir = 'app/static/fonts'
icons_dir = 'app/static/icons'

# Extra Large, Prominent Typography for Job Content
font_job_title = ImageFont.truetype(os.path.join(font_dir, 'Montserrat-Bold.ttf'), 21)
font_job_label = ImageFont.truetype(os.path.join(font_dir, 'Montserrat-Bold.ttf'), 16)
font_job_val = ImageFont.truetype(os.path.join(font_dir, 'Montserrat-Regular.ttf'), 16)
font_job_sub = ImageFont.truetype(os.path.join(font_dir, 'Montserrat-Regular.ttf'), 13)

font_tagline = ImageFont.truetype(os.path.join(font_dir, 'Montserrat-Bold.ttf'), 15)
font_h2 = ImageFont.truetype(os.path.join(font_dir, 'Montserrat-Bold.ttf'), 17)
font_bold = ImageFont.truetype(os.path.join(font_dir, 'Montserrat-Bold.ttf'), 14)
font_bold_xs = ImageFont.truetype(os.path.join(font_dir, 'Montserrat-Bold.ttf'), 10)

# Left Subtitle (Well-spaced across 4 lines)
tagline_txt = 'Exciting opportunities for experienced cybersecurity professionals to join our prestigious projects in Vijayawada.'
wrapped_tag = textwrap.fill(tagline_txt, width=36)
ty = 412
for line in wrapped_tag.split('\n')[:4]:
    draw.text((45, ty), line, fill='#374151', font=font_tagline)
    ty += 22

# Middle Column (Centered at x=490, gives 540px width with no overlap)
col2_x = 490

# --- ROLE 1 ---
cs_ic = Image.open(os.path.join(icons_dir, 'clipboard_lines.png')).convert('RGBA')
cs_ic.thumbnail((60, 60))
img.paste(cs_ic, (col2_x, 184), cs_ic)

draw.text((col2_x + 74, 184), '1. PROJECT MANAGER –', fill='#18181B', font=font_job_title)
draw.text((col2_x + 98, 214), 'CYBER AUDIT – GRC SPECIALIST', fill='#18181B', font=font_job_title)

by = 258
draw.text((col2_x + 74, by), '• Experience:', fill='#111827', font=font_job_label)
draw.text((col2_x + 200, by), '10+ Years in Cyber Audit & GRC', fill='#374151', font=font_job_val)
by += 29

draw.text((col2_x + 74, by), '• Qualification:', fill='#111827', font=font_job_label)
draw.text((col2_x + 210, by), 'B.Tech / M.Tech / MCA / Master\'s', fill='#374151', font=font_job_val)
by += 21
draw.text((col2_x + 88, by), '(Electronics, Computer Science, Electrical, Cybersecurity)', fill='#6B7280', font=font_job_sub)
by += 29

draw.text((col2_x + 74, by), '• Key Skills:', fill='#111827', font=font_job_label)
draw.text((col2_x + 185, by), 'CISA, CISSP, CISM, ISO 27001, GRC', fill='#374151', font=font_job_val)
by += 42

# --- ROLE 2 ---
ml_ic = Image.open(os.path.join(icons_dir, 'monitor_lock.png')).convert('RGBA')
ml_ic.thumbnail((60, 60))
img.paste(ml_ic, (col2_x, by), ml_ic)

draw.text((col2_x + 74, by + 4), '2. SOC MANAGER', fill='#18181B', font=font_job_title)
by += 36

draw.text((col2_x + 74, by), '• Experience:', fill='#111827', font=font_job_label)
draw.text((col2_x + 200, by), '10+ Years in SOC Operations', fill='#374151', font=font_job_val)
by += 29

draw.text((col2_x + 74, by), '• Qualification:', fill='#111827', font=font_job_label)
draw.text((col2_x + 210, by), 'Bachelor\'s / Master\'s (IT / Cyber)', fill='#374151', font=font_job_val)
by += 29

draw.text((col2_x + 74, by), '• Certifications:', fill='#111827', font=font_job_label)
draw.text((col2_x + 215, by), 'GCIA / GCFA / CEH / Security+ / CySA+', fill='#374151', font=font_job_val)
by += 21
draw.text((col2_x + 88, by), '(CrowdStrike, Splunk, SIEM & Threat Hunting)', fill='#6B7280', font=font_job_sub)

# Redraw Dark Footer Bar
tier2_y = int(h * 0.883)
draw.rectangle([0, tier2_y, w, h], fill='#18181B')

draw.ellipse([45, tier2_y + 24, 90, tier2_y + 69], fill='#55634D')
gw = Image.open(os.path.join(icons_dir, 'globe_white.png')).convert('RGBA')
gw.thumbnail((24, 24))
img.paste(gw, (56, tier2_y + 35), gw)

draw.text((105, tier2_y + 22), 'VISIT OUR PORTAL', fill='#9CA3AF', font=font_bold_xs)
draw.text((105, tier2_y + 40), 'www.nexlogic.co.in', fill='#A3B18A', font=font_h2)

draw.line([(450, tier2_y + 16), (450, h - 16)], fill='#374151', width=1)

draw.ellipse([480, tier2_y + 24, 525, tier2_y + 69], fill='#55634D')
mw = Image.open(os.path.join(icons_dir, 'mail_white.png')).convert('RGBA')
mw.thumbnail((22, 22))
img.paste(mw, (492, tier2_y + 36), mw)

draw.text((540, tier2_y + 22), 'SEND YOUR RESUME', fill='#9CA3AF', font=font_bold_xs)
draw.text((540, tier2_y + 40), 'hr@naxlogic.com', fill='#A3B18A', font=font_h2)

draw.line([(890, tier2_y + 16), (890, h - 16)], fill='#374151', width=1)
draw.text((920, tier2_y + 36), 'NEXLOGIC — INNOVATING CONNECTIONS.', fill='#E5E7EB', font=font_bold)

os.makedirs('generated_previews', exist_ok=True)
img.save('generated_previews/test_flawless_final.png')
print('Saved test_flawless_final.png successfully!')
