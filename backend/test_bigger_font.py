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

# Clean logo area
bg_fill = img.getpixel((int(w * 0.50), int(h * 0.15)))
draw.rectangle([0, 0, 560, 190], fill=bg_fill)

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

# Clean middle job card region (large box to expand)
draw.rectangle([int(w * 0.370), int(h * 0.180), int(w * 0.720), int(h * 0.720)], fill=bg_fill)

# Clean left subtitle
draw.rectangle([int(w * 0.035), int(h * 0.465), int(w * 0.360), int(h * 0.585)], fill=bg_fill)

font_dir = 'app/static/fonts'
icons_dir = 'app/static/icons'

font_job_title = ImageFont.truetype(os.path.join(font_dir, 'Montserrat-Bold.ttf'), 20)
font_job_label = ImageFont.truetype(os.path.join(font_dir, 'Montserrat-Bold.ttf'), 14)
font_job_val = ImageFont.truetype(os.path.join(font_dir, 'Montserrat-Regular.ttf'), 14)
font_job_sub = ImageFont.truetype(os.path.join(font_dir, 'Montserrat-Regular.ttf'), 12)
font_tagline = ImageFont.truetype(os.path.join(font_dir, 'Montserrat-Bold.ttf'), 16)
font_h2 = ImageFont.truetype(os.path.join(font_dir, 'Montserrat-Bold.ttf'), 17)
font_bold = ImageFont.truetype(os.path.join(font_dir, 'Montserrat-Bold.ttf'), 14)
font_bold_xs = ImageFont.truetype(os.path.join(font_dir, 'Montserrat-Bold.ttf'), 10)

# Left Subtitle
tagline_txt = 'Exciting opportunities for experienced technology professionals to join our prestigious projects in Noida, UP.'
wrapped_tag = textwrap.fill(tagline_txt, width=32)
ty = int(h * 0.472)
for line in wrapped_tag.split('\n')[:4]:
    draw.text((int(w * 0.040), ty), line, fill='#374151', font=font_tagline)
    ty += 23

# Middle Column (Bigger, Spaced Out, and Filling Space Nicely)
col2_x = int(w * 0.375)

# --- ROLE 1 ---
cs_ic = Image.open(os.path.join(icons_dir, 'clipboard_lines.png')).convert('RGBA')
cs_ic.thumbnail((54, 54))
img.paste(cs_ic, (col2_x, int(h * 0.195)), cs_ic)

draw.text((col2_x + 66, int(h * 0.198)), '1. ASSOCIATE SOFTWARE ENGINEER', fill='#18181B', font=font_job_title)

by = int(h * 0.250)
draw.text((col2_x + 66, by), '• Experience:', fill='#111827', font=font_job_label)
draw.text((col2_x + 175, by), '0-2 Years in relevant domain', fill='#374151', font=font_job_val)
by += 26

draw.text((col2_x + 66, by), '• Qualification:', fill='#111827', font=font_job_label)
draw.text((col2_x + 185, by), 'B.Tech / B.E. / MCA / M.Tech / MBA / CA', fill='#374151', font=font_job_val)
by += 18
draw.text((col2_x + 78, by), '(Computer Science, IT, Electronics, or relevant discipline)', fill='#6B7280', font=font_job_sub)
by += 26

draw.text((col2_x + 66, by), '• Key Skills:', fill='#111827', font=font_job_label)
draw.text((col2_x + 160, by), 'JavaScript, React.js, Node.js, Express.js, SQL', fill='#374151', font=font_job_val)
by += 40

# --- ROLE 2 ---
ml_ic = Image.open(os.path.join(icons_dir, 'monitor_lock.png')).convert('RGBA')
ml_ic.thumbnail((54, 54))
img.paste(ml_ic, (col2_x, by), ml_ic)

draw.text((col2_x + 66, by + 4), '2. SOC MANAGER', fill='#18181B', font=font_job_title)
by += 34

draw.text((col2_x + 66, by), '• Experience:', fill='#111827', font=font_job_label)
draw.text((col2_x + 175, by), '10+ Years in SOC / Cybersecurity', fill='#374151', font=font_job_val)
by += 26

draw.text((col2_x + 66, by), '• Qualification:', fill='#111827', font=font_job_label)
draw.text((col2_x + 185, by), "Bachelor's / Master's (IT / Cyber Security)", fill='#374151', font=font_job_val)
by += 26

draw.text((col2_x + 66, by), '• Certifications (Preferred):', fill='#111827', font=font_job_label)
by += 20
draw.text((col2_x + 78, by), 'GCIA / GCFA / GCIH / CEH / ECIH / Security+ / CySA+', fill='#374151', font=font_job_val)
by += 18
draw.text((col2_x + 78, by), '(CrowdStrike, Splunk, QRadar, SIEM & Threat Hunting)', fill='#6B7280', font=font_job_sub)

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
img.save('generated_previews/test_bigger_font2.png')
print('Saved test_bigger_font2.png successfully!')
