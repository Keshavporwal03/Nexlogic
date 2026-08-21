import os
import textwrap
import urllib.request
import hashlib
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# Curated high-res Unsplash photo IDs for Indian & Global city landmarks / themes
CURATED_LOCATION_PHOTOS = {
    "bhopal": "photo-1506744038136-46273834b3fb",
    "vijayawada": "photo-1506744038136-46273834b3fb",
    "kanpur": "photo-1548013146-72479768bada",
    "noida": "photo-1486406146926-c627a92ad1ab",
    "indore": "photo-1519501025264-65ba15a82390",
    "indor": "photo-1519501025264-65ba15a82390",
    "delhi": "photo-1587474260584-136574528ed5",
    "bengaluru": "photo-1596176530529-78163a4f7af2",
    "bangalore": "photo-1596176530529-78163a4f7af2",
    "lucknow": "photo-1548013146-72479768bada",
    "manipur": "photo-1590050752117-238cb0fb12b1",
    "office": "photo-1486406146926-c627a92ad1ab",
    "chair": "photo-1486406146926-c627a92ad1ab",
    "tech": "photo-1526374965328-7f61d4dc18c5",
    "default": "photo-1486406146926-c627a92ad1ab"
}

FALLBACK_CITY_POOL = [
    "photo-1486406146926-c627a92ad1ab",
    "photo-1506744038136-46273834b3fb",
    "photo-1519501025264-65ba15a82390",
    "photo-1512453979798-5ea266f8880c",
    "photo-1599661046289-e31897846e41",
    "photo-1570168007204-dfb528c6958f"
]

def resolve_location_photo_id(loc_name: str, index: int = 0) -> str:
    """Match a location string to a curated city landmark Unsplash photo."""
    if not loc_name:
        return FALLBACK_CITY_POOL[index % len(FALLBACK_CITY_POOL)]
    clean_loc = loc_name.lower().strip()
    for key, pid in CURATED_LOCATION_PHOTOS.items():
        if key in clean_loc:
            return pid
    h = int(hashlib.md5(clean_loc.encode()).hexdigest(), 16) + index
    return FALLBACK_CITY_POOL[h % len(FALLBACK_CITY_POOL)]

def fetch_unsplash_image(photo_id: str, w: int, h: int) -> Image.Image:
    """Fetch and center-crop an Unsplash photo with procedural fallback."""
    url = f"https://images.unsplash.com/{photo_id}?auto=format&fit=crop&w={w}&q=85"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=6) as response:
            img = Image.open(BytesIO(response.read())).convert("RGBA")
            img_ratio = img.width / img.height
            req_ratio = w / h
            if img_ratio > req_ratio:
                new_w = int(img.height * req_ratio)
                left = (img.width - new_w) // 2
                img = img.crop((left, 0, left + new_w, img.height))
            else:
                new_h = int(img.width / req_ratio)
                top = (img.height - new_h) // 2
                img = img.crop((0, top, img.width, top + new_h))
            img = img.resize((w, h), Image.Resampling.LANCZOS)
            return img
    except Exception as e:
        print(f"Unsplash fetch fallback triggered for {photo_id}: {e}")
        fallback = Image.new("RGBA", (w, h), "#0F291E")
        f_draw = ImageDraw.Draw(fallback)
        for i in range(h):
            alpha = int(40 + (i / h) * 60)
            f_draw.line([(0, i), (w, i)], fill=(20, 58, 38, alpha))
        return fallback

def make_white_transparent(img):
    """Make white or near-white background transparent."""
    if not img:
        return None
    img = img.convert("RGBA")
    data = img.getdata()
    new_data = []
    for item in data:
        if item[0] > 235 and item[1] > 235 and item[2] > 235:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    img.putdata(new_data)
    return img

def create_job_banner(jobs, company_colors: dict) -> BytesIO:
    """
    Generate authoritative recruitment banners:
    - Single-Job: Exact 1:1 master reproduction of the user's reference banner with dynamic role data.
    - Multi-Job: PDF Page 17 3-Role Power Grid.
    """
    if isinstance(jobs, dict):
        jobs = [jobs]
    elif not isinstance(jobs, list):
        jobs = []
        
    width = 1400
    is_single_job = len(jobs) <= 1
    
    font_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "fonts")
    try:
        font_huge = ImageFont.truetype(os.path.join(font_dir, "Montserrat-Bold.ttf"), 78)
        font_huge_hiring = ImageFont.truetype(os.path.join(font_dir, "Montserrat-Bold.ttf"), 88)
        font_h1 = ImageFont.truetype(os.path.join(font_dir, "Montserrat-Bold.ttf"), 28)
        font_h2 = ImageFont.truetype(os.path.join(font_dir, "Montserrat-Bold.ttf"), 22)
        font_title_banner = ImageFont.truetype(os.path.join(font_dir, "Montserrat-Bold.ttf"), 20)
        font_bold = ImageFont.truetype(os.path.join(font_dir, "Montserrat-Bold.ttf"), 16)
        font_bold_sm = ImageFont.truetype(os.path.join(font_dir, "Montserrat-Bold.ttf"), 14)
        font_bold_xs = ImageFont.truetype(os.path.join(font_dir, "Montserrat-Bold.ttf"), 12)
        font_regular = ImageFont.truetype(os.path.join(font_dir, "Montserrat-Regular.ttf"), 15)
        font_regular_sm = ImageFont.truetype(os.path.join(font_dir, "Montserrat-Regular.ttf"), 13)
        font_tagline = ImageFont.truetype(os.path.join(font_dir, "Montserrat-Bold.ttf"), 18)
        font_foot = ImageFont.truetype(os.path.join(font_dir, "Montserrat-Bold.ttf"), 22)
    except IOError:
        font_huge = font_huge_hiring = font_h1 = font_h2 = font_title_banner = font_bold = font_bold_sm = font_bold_xs = font_tagline = font_foot = ImageFont.load_default()
        font_regular = font_regular_sm = ImageFont.load_default()


    icons_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "icons")
    def load_icon(name):
        icon_path = os.path.join(icons_dir, f"{name}.png")
        try:
            return Image.open(icon_path).convert("RGBA")
        except:
            return None

    apply_link = company_colors.get("apply_link") or "https://egovtalent.com/jobs"
    contact_email = company_colors.get("contact_email") or "hr@naxlogic.com"
    website = company_colors.get("website") or "www.nexlogic.co.in"

    # =========================================================================
    # 1. SINGLE JOB BANNER (Exact 100% Match to User Master Reference Banner)
    # =========================================================================
    if is_single_job:
        job = jobs[0] if jobs else {}
        j_title = (job.get("title") or "PROJECT MANAGER – CYBER AUDIT – GRC SPECIALIST").upper()
        j_loc = job.get("location") or "Noida, Uttar Pradesh"
        j_exp = job.get("experience") or "10+ Years"
        j_mode = job.get("work_mode") or "100% On-site"
        j_openings = job.get("number_of_openings") or job.get("openings") or job.get("vacancies") or 1
        j_skills = job.get("skills") or []

        
        tpl_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "user_exact_template.png")
        if os.path.exists(tpl_path):
            raw_tpl = Image.open(tpl_path).convert("RGBA")
            target_w = 1400
            target_h = int(raw_tpl.height * (target_w / raw_tpl.width))
            img = raw_tpl.resize((target_w, target_h), Image.Resampling.LANCZOS)
        else:
            target_w, target_h = 1400, 928
            img = Image.new("RGBA", (target_w, target_h), "#F8F6F0")
            
        draw = ImageDraw.Draw(img)
        w, h = img.size
         # 1. Clean Logo Area & Paste Official Company Logo
        bg_fill = img.getpixel((int(w * 0.50), int(h * 0.15))) if img else (250, 246, 243, 255)
        draw.rectangle([0, 0, 545, 172], fill=bg_fill)
        draw.rectangle([480, 160, 535, 215], fill=bg_fill)
        draw.rectangle([460, 460, 520, 485], fill=bg_fill)

        for r in range(7):
            for c in range(5):
                draw.ellipse([24 + c * 14, 22 + r * 14, 28 + c * 14, 26 + r * 14], fill="#CBD5E1")

        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "company-logo.png")
        if os.path.exists(logo_path):
            try:
                c_logo = Image.open(logo_path)
                bbox = c_logo.getbbox()
                if bbox:
                    c_logo = c_logo.crop(bbox)
                c_logo = make_white_transparent(c_logo)
                c_logo.thumbnail((440, 125), Image.Resampling.LANCZOS)
                img.paste(c_logo, (55, 32), c_logo)
            except Exception as e:
                print(f"Company logo load error: {e}")

        # 2. Dynamic Middle Section & Left Subtitle (Scaled Up Larger Font Sizes)
        font_job_title = ImageFont.truetype(os.path.join(font_dir, "Montserrat-Bold.ttf"), 24)
        font_job_label = ImageFont.truetype(os.path.join(font_dir, "Montserrat-Bold.ttf"), 18)
        font_job_val = ImageFont.truetype(os.path.join(font_dir, "Montserrat-Regular.ttf"), 17)
        font_job_sub = ImageFont.truetype(os.path.join(font_dir, "Montserrat-Regular.ttf"), 15)


        # Clean Middle Job Card Area (from x=475 to x=1030, y=170 to y=655)
        draw.rectangle([475, 170, 1030, 655], fill=bg_fill)
        
        # Clean Left Subtitle Area (from x=20 to x=475, y=430 to y=575) - Y starts at 430 to prevent clipping "HIRING!" bottom!
        draw.rectangle([20, 430, 475, 575], fill=bg_fill)

        # Left Subtitle
        if "cyber" in j_title.lower() or "security" in j_title.lower() or "audit" in j_title.lower():
            tagline_txt = f"Exciting opportunities for experienced cybersecurity professionals to join our prestigious projects in {j_loc}."
        elif "software" in j_title.lower() or "engineer" in j_title.lower() or "developer" in j_title.lower():
            tagline_txt = f"Exciting opportunities for experienced software engineering professionals to join our prestigious digital platforms in {j_loc}."
        else:
            tagline_txt = f"Exciting opportunities for experienced professionals to join our prestigious digital governance projects in {j_loc}."
            
        wrapped_tag = textwrap.fill(tagline_txt, width=38)
        ty = 435
        for line in wrapped_tag.split('\n')[:4]:
            draw.text((45, ty), line, fill="#374151", font=font_tagline)
            ty += 22
            
        # Middle Section (Role 1 & Role 2 with Extra Large Prominent Typography)
        col2_x = 490
        
        # Role 1
        cs_ic = load_icon("clipboard_lines") or load_icon("clipboard_shield")
        if cs_ic:
            cs_ic.thumbnail((60, 60))
            img.paste(cs_ic, (col2_x, 184), cs_ic)
            
        r1_title = j_title
        if "–" in r1_title or "-" in r1_title:
            parts = r1_title.replace("–", "-").split("-", 1)
            draw.text((col2_x + 74, 184), f"1. {parts[0].strip()} –", fill="#18181B", font=font_job_title)
            draw.text((col2_x + 98, 214), parts[1].strip(), fill="#18181B", font=font_job_title)
            by = 258
        else:
            draw.text((col2_x + 74, 186), f"1. {r1_title[:30]}", fill="#18181B", font=font_job_title)
            by = 236
            
        draw.text((col2_x + 74, by), "• Experience:", fill="#111827", font=font_job_label)
        draw.text((col2_x + 200, by), j_exp, fill="#374151", font=font_job_val)
        by += 28
        
        j_qual = job.get("education_requirements")
        if j_qual:
            qual_str = " / ".join(j_qual) if isinstance(j_qual, list) else str(j_qual)
            draw.text((col2_x + 74, by), "• Qualification:", fill="#111827", font=font_job_label)
            wrapped_qual = textwrap.fill(qual_str, width=34)
            for line in wrapped_qual.split('\n'):
                draw.text((col2_x + 210, by), line, fill="#374151", font=font_job_val)
                by += 20
            by += 8
        
        if j_skills:
            draw.text((col2_x + 74, by), "• Key Skills:", fill="#111827", font=font_job_label)
            skills_str = ", ".join(j_skills[:5]) if isinstance(j_skills, list) else str(j_skills)
            wrapped_sk = textwrap.fill(skills_str, width=34)
            sk_lines = wrapped_sk.split('\n')
            
            draw.text((col2_x + 185, by), sk_lines[0], fill="#374151", font=font_job_val)
            by += 22
            for sk_l in sk_lines[1:3]:
                draw.text((col2_x + 185, by), sk_l, fill="#374151", font=font_job_val)
                by += 20
                
        j_certs = job.get("preferred_certifications")
        if j_certs:
            draw.text((col2_x + 74, by), "• Certifications:", fill="#111827", font=font_job_label)
            certs_str = ", ".join(j_certs[:4]) if isinstance(j_certs, list) else str(j_certs)
            wrapped_certs = textwrap.fill(certs_str, width=32)
            cert_lines = wrapped_certs.split('\n')
            
            draw.text((col2_x + 225, by), cert_lines[0], fill="#374151", font=font_job_val)
            by += 22
            for cert_l in cert_lines[1:3]:
                draw.text((col2_x + 225, by), cert_l, fill="#374151", font=font_job_val)
                by += 20

        # Section 2: Display Job 2 if 2+ jobs exist, otherwise display Key Responsibilities & Governance for the single job
        if len(jobs) >= 2:
            r2_job = jobs[1]
            r2_title = f"2. {(r2_job.get('title') or 'ASSOCIATE ROLE').upper()[:32]}"
            r2_exp = (r2_job.get("experience") or "5+ Years").strip()
            r2_qual_list = r2_job.get("education_requirements")
            r2_qual = " / ".join(r2_qual_list) if isinstance(r2_qual_list, list) else (str(r2_qual_list) if r2_qual_list else "")
            
            r2_skills = r2_job.get("skills")
            if r2_skills:
                r2_skills_label = "• Key Skills:"
                r2_skills_val = ", ".join(r2_skills[:4]) if isinstance(r2_skills, list) else str(r2_skills)
            else:
                r2_skills_label = ""
                r2_skills_val = ""
        else:
            r2_title = "2. KEY RESPONSIBILITIES & GOVERNANCE"
            r2_exp = f"{j_mode} • Location: {j_loc}"
            openings_text = f"{j_openings} Active Opening" if int(j_openings) == 1 else f"{j_openings} Active Openings"
            r2_qual = f"{openings_text} • Immediate Joiners Preferred"
            
            j_resp = job.get("key_responsibilities")
            if j_resp:
                r2_skills_label = "• Key Responsibilities:"
                r2_skills_val = ", ".join(j_resp[:4]) if isinstance(j_resp, list) else str(j_resp)
            else:
                r2_skills_label = ""
                r2_skills_val = ""


        # Section 2 Rendering
        by += 15 # Add extra spacing before Section 2
        ml_ic = load_icon("monitor_lock") or load_icon("clipboard_shield")
        if ml_ic:
            ml_ic.thumbnail((60, 60))
            img.paste(ml_ic, (col2_x, by), ml_ic)
            
        # Title might be long, let's wrap it just in case
        wrapped_r2 = textwrap.fill(r2_title, width=35)
        for line in wrapped_r2.split('\n'):
            draw.text((col2_x + 74, by + 4), line, fill="#18181B", font=font_job_title)
            by += 28
        by += 10
        
        if len(jobs) >= 2:
            draw.text((col2_x + 74, by), "• Experience:", fill="#111827", font=font_job_label)
            draw.text((col2_x + 200, by), r2_exp, fill="#374151", font=font_job_val)
            by += 28
            
            if r2_qual:
                draw.text((col2_x + 74, by), "• Qualification:", fill="#111827", font=font_job_label)
                draw.text((col2_x + 210, by), r2_qual, fill="#374151", font=font_job_val)
                by += 28
            
            if r2_skills_label and r2_skills_val:
                draw.text((col2_x + 74, by), r2_skills_label, fill="#111827", font=font_job_label)
                draw.text((col2_x + 185, by), r2_skills_val[:45], fill="#374151", font=font_job_val)
        else:
            draw.text((col2_x + 74, by), "• Deployment:", fill="#111827", font=font_job_label)
            wrapped_dep = textwrap.fill(r2_exp, width=32)
            for line in wrapped_dep.split('\n'):
                draw.text((col2_x + 215, by), line, fill="#374151", font=font_job_val)
                by += 22
            by += 6
            
            draw.text((col2_x + 74, by), "• Openings:", fill="#111827", font=font_job_label)
            wrapped_qual = textwrap.fill(r2_qual, width=34)
            for line in wrapped_qual.split('\n'):
                draw.text((col2_x + 200, by), line, fill="#374151", font=font_job_val)
                by += 22
            by += 6
            
            if r2_skills_label and r2_skills_val:
                draw.text((col2_x + 74, by), r2_skills_label, fill="#111827", font=font_job_label)
                if "Responsibilities" in r2_skills_label:
                    by += 24
                    wrapped_skills = textwrap.fill(r2_skills_val, width=45)
                    for line in wrapped_skills.split('\n'):
                        draw.text((col2_x + 95, by), line, fill="#374151", font=font_job_val)
                        by += 22
                else:
                    wrapped_skills = textwrap.fill(r2_skills_val, width=34)
                    for line in wrapped_skills.split('\n'):
                        draw.text((col2_x + 215, by), line, fill="#374151", font=font_job_val)
                        by += 22





        # Single-Job Footer Bar (Dynamic Apply Link from job profile)
        tier2_y = int(h * 0.883)
        draw.rectangle([0, tier2_y, w, h], fill="#18181B")
        
        # Apply Online / Visit Portal
        draw.ellipse([45, tier2_y + 24, 90, tier2_y + 69], fill="#55634D")
        gw = load_icon("globe_white")
        if gw:
            gw.thumbnail((24, 24))
            img.paste(gw, (56, tier2_y + 35), gw)
            
        custom_apply_link = (job.get("apply_link") or company_colors.get("apply_link") or website or "www.eGovTalent.com").strip()
        clean_apply_display = custom_apply_link.replace("https://", "").replace("http://", "").rstrip("/")
        if len(clean_apply_display) > 28:
            clean_apply_display = clean_apply_display[:26] + "..."

        draw.text((105, tier2_y + 22), "APPLY ONLINE AT", fill="#9CA3AF", font=font_bold_xs)
        draw.text((105, tier2_y + 40), clean_apply_display, fill="#A3B18A", font=font_h2)
        
        draw.line([(450, tier2_y + 16), (450, h - 16)], fill="#374151", width=1)
        
        # Send Your Resume
        draw.ellipse([480, tier2_y + 24, 525, tier2_y + 69], fill="#55634D")
        mw = load_icon("mail_white")

        if mw:
            mw.thumbnail((22, 22))
            img.paste(mw, (492, tier2_y + 36), mw)
            
        draw.text((540, tier2_y + 22), "SEND YOUR RESUME", fill="#9CA3AF", font=font_bold_xs)
        draw.text((540, tier2_y + 40), contact_email, fill="#A3B18A", font=font_h2)
        
        draw.line([(890, tier2_y + 16), (890, h - 16)], fill="#374151", width=1)
        
        # Tagline
        draw.text((920, tier2_y + 36), "NEXLOGIC — INNOVATING CONNECTIONS.", fill="#E5E7EB", font=font_bold)

    else:
        display_jobs = jobs[:3]
        num_cards = len(display_jobs)
        
        # 1. Base Canvas Creation
        target_w, target_h = 1400, 940
        img = Image.new("RGBA", (target_w, target_h), "#F2F0EA")  # Off-white/cream background
        draw = ImageDraw.Draw(img)
        w, h = img.size
        
        # 2. Header (Top Left)
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "company-logo.png")
        if not os.path.exists(logo_path):
            logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "nexlogic_logo.png")
            
        if os.path.exists(logo_path):
            try:
                logo_img = Image.open(logo_path).convert("RGBA")
                # Remove white background from logo
                datas = logo_img.getdata()
                newData = []
                for item in datas:
                    if item[0] > 240 and item[1] > 240 and item[2] > 240:
                        newData.append((255, 255, 255, 0))
                    else:
                        newData.append(item)
                logo_img.putdata(newData)
                
                logo_img.thumbnail((400, 120), Image.Resampling.LANCZOS) # Made logo even larger
                img.paste(logo_img, (40, 20), logo_img)
            except Exception:
                pass
                
        # Vertical divider line
        draw.line([(360, 30), (360, 100)], fill="#374151", width=2)
        
        # eGov Talent placeholder Text
        draw.text((380, 35), "Your Gateway to", fill="#4B5563", font=font_bold)
        draw.text((380, 55), "e-Governance Careers", fill="#111827", font=font_h2)
        
        # "WE ARE HIRING!" Text
        f_we_are = ImageFont.truetype(os.path.join(font_dir, "Montserrat-Bold.ttf"), 54) if os.path.exists(os.path.join(font_dir, "Montserrat-Bold.ttf")) else font_huge
        f_hiring = ImageFont.truetype(os.path.join(font_dir, "Montserrat-Bold.ttf"), 110) if os.path.exists(os.path.join(font_dir, "Montserrat-Bold.ttf")) else font_huge
        
        draw.text((40, 140), "WE ARE", fill="#2D241C", font=f_we_are)
        draw.text((40, 190), "HIRING!", fill="#5E4D3E", font=f_hiring) # Warm Sepia brown
        
        # Subtitle Pill
        draw.rounded_rectangle([40, 330, 480, 370], radius=18, fill="#3E3228") # Dark brown
        draw.text((65, 340), "Great Opportunities for IT Professionals", fill="white", font=font_title_banner)
        
        draw.text((40, 390), "— Exciting roles in e-Governance & Digital Transformation Domain —", fill="#5E4D3E", font=font_bold)
        
        # 3. Image & Curved Graphics (Top Right)
        draw.ellipse([800, -250, 1600, 550], fill="#5E4D3E") # Outer sepia
        draw.ellipse([825, -225, 1600, 525], fill="#3E3228") # Inner dark brown
        
        # Create a mask for the image to fit perfectly inside the third ellipse
        mask = Image.new("L", img.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse([835, -215, 1600, 515], fill=255)
        
        # Use new city image
        ref_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "city_hero.png")
        if os.path.exists(ref_path):
            try:
                ref_img = Image.open(ref_path).convert("RGBA")
                # Resize so width is 800 to cover the mask
                ref_img = ref_img.resize((800, int(ref_img.height * (800/ref_img.width))), Image.Resampling.LANCZOS)
                
                temp_img = Image.new("RGBA", img.size)
                temp_img.paste(ref_img, (830, -50))
                
                # Paste the masked image!
                img.paste(temp_img, (0, 0), mask)
            except Exception:
                pass
                
        # "Join Us" Badge - Moved next to HIRING!
        circ_x = 510
        circ_y = 130
        draw.ellipse([circ_x, circ_y, circ_x+160, circ_y+160], fill="#5E4D3E")
        draw.text((circ_x + 35, circ_y + 55), "JOIN US &\nBUILD\nIMPACTFUL\nSOLUTIONS", fill="white", font=font_bold, align="center")
        
        # 4. Dynamic Job Profile Cards
        cols = [
            {"x": 40, "header_bg": "#3E3228"},   # Dark Brown
            {"x": 490, "header_bg": "#5E4D3E"},  # Sepia Brown
            {"x": 940, "header_bg": "#7A6A58"}   # Warm Grey/Beige
        ]
        
        card_w = 420
        card_y = 430
        card_h = 370 
        
        for idx, j_item in enumerate(display_jobs):
            col = cols[idx]
            cx = col["x"]
            
            # Card Base
            draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + card_h], radius=12, fill="#FFFFFF", outline="#E5E7EB", width=2)
            
            # Header
            draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + 70], radius=12, fill=col["header_bg"])
            draw.rectangle([cx, card_y + 35, cx + card_w, card_y + 70], fill=col["header_bg"]) # square bottom
            
            # Icon
            c_icon = load_icon("users_white") if idx == 0 else (load_icon("building_white") if idx == 1 else load_icon("clipboard_lines"))
            if c_icon:
                c_icon.thumbnail((45, 45))
                img.paste(c_icon, (cx + 15, card_y + 12), c_icon)
                
            # Title
            t_title = j_item.get("title", "SPECIALIST").upper()
            wrapped_t = textwrap.fill(f"{idx+1}. {t_title}", width=25)
            ty = card_y + 15
            for line in wrapped_t.split('\n')[:2]:
                draw.text((cx + 70, ty), line, fill="white", font=font_title_banner)
                ty += 22
                
            # Content
            by = card_y + 85
            
            # Experience
            j_exp = j_item.get("experience")
            if j_exp:
                draw.text((cx + 20, by), "• Experience:", fill="#111827", font=font_title_banner)
                draw.text((cx + 175, by + 4), j_exp, fill="#4B5563", font=font_bold)
                by += 32
                
            # Location
            j_loc = j_item.get("location")
            if j_loc:
                draw.text((cx + 20, by), "• Location:", fill="#111827", font=font_title_banner)
                draw.text((cx + 175, by + 4), j_loc, fill="#4B5563", font=font_bold)
                by += 32
                
            # Qualification
            j_qual = j_item.get("education_requirements")
            if j_qual:
                draw.text((cx + 20, by), "• Qualification:", fill="#111827", font=font_title_banner)
                qual_str = ", ".join(j_qual) if isinstance(j_qual, list) else str(j_qual)
                draw.text((cx + 175, by + 4), textwrap.shorten(qual_str, width=25), fill="#4B5563", font=font_bold)
                by += 32
            
            # Responsibilities
            j_resp = j_item.get("key_responsibilities")
            if j_resp:
                draw.text((cx + 20, by), "• Responsibilities:", fill="#111827", font=font_title_banner)
                b_str = " ".join(j_resp) if isinstance(j_resp, list) else str(j_resp)
                wrapped_b = textwrap.fill(b_str, width=42)
                by += 26
                for line in wrapped_b.split('\n')[:4]:
                    draw.text((cx + 35, by), line, fill="#4B5563", font=font_regular)
                    by += 22
                by += 10
            
            # Skills
            skills = j_item.get("skills")
            if skills:
                draw.text((cx + 20, by), "• Skills:", fill="#111827", font=font_title_banner)
                sk_str = ", ".join(skills) if isinstance(skills, list) else str(skills)
                wrapped_sk = textwrap.fill(sk_str, width=42)
                by += 26
                for line in wrapped_sk.split('\n')[:2]:
                    draw.text((cx + 35, by), line, fill="#4B5563", font=font_regular)
                    by += 22
                by += 10
            
            # Certifications
            j_cert = j_item.get("preferred_certifications")
            if j_cert and by < (card_y + card_h - 90):
                draw.text((cx + 20, by), "• Certifications:", fill="#111827", font=font_title_banner)
                cert_str = ", ".join(j_cert) if isinstance(j_cert, list) else str(j_cert)
                wrapped_c = textwrap.fill(cert_str, width=42)
                by += 26
                for line in wrapped_c.split('\n')[:2]:
                    draw.text((cx + 35, by), line, fill="#4B5563", font=font_regular)
                    by += 22
                by += 10
                
            # Apply Now Box (bottom)
            btn_y = card_y + card_h - 50
            draw.rounded_rectangle([cx, btn_y, cx + card_w, card_y + card_h], radius=12, fill=col["header_bg"])
            draw.rectangle([cx, btn_y, cx + card_w, btn_y + 15], fill=col["header_bg"]) # square top
            
            aw = load_icon("globe_white")
            if aw:
                aw.thumbnail((24, 24))
                img.paste(aw, (cx + 15, btn_y + 13), aw)
                
            draw.text((cx + 45, btn_y + 16), "APPLY NOW", fill="white", font=font_bold)
            
            clean_app_link = apply_link if len(apply_link) < 32 else apply_link[:30] + "..."
            draw.text((cx + 160, btn_y + 16), clean_app_link, fill="#D1D5DB", font=font_bold_sm)
            
        # 5. Footer Layout
        # Divider line
        draw.line([(40, 830), (1360, 830)], fill="#D1D5DB", width=2)
        
        # Email Box
        m_ic = load_icon("mail_white")
        draw.ellipse([50, 840, 100, 890], fill="#5E4D3E")
        if m_ic:
            m_ic.thumbnail((26, 26))
            img.paste(m_ic, (62, 852), m_ic)
            
        draw.text((115, 845), "SEND YOUR CV TO", fill="#6B7280", font=font_bold_sm)
        draw.text((115, 865), contact_email, fill="#111827", font=font_h2)
        
        # Divider
        draw.line([(450, 840), (450, 890)], fill="#D1D5DB", width=2)
        
        # Trust Users Icon
        u_ic = load_icon("users_green")
        if u_ic:
            u_ic.thumbnail((45, 45))
            img.paste(u_ic, (470, 845), u_ic)
            
        draw.text((530, 840), "IDEAL CANDIDATES:", fill="#6B7280", font=font_bold_sm)
        draw.text((530, 860), "Professionals with experience in e-Governance, Healthcare,\nInsurance, Business Analytics, IT Consulting & Digital Transformation.", fill="#4B5563", font=font_regular_sm)
        
        # Domain text & Logo
        draw.text((1000, 845), "SHAPE THE FUTURE OF\nDIGITAL INDIA WITH US!", fill="#111827", font=font_bold)
        
        # Bottom Strip
        draw.rectangle([0, 920, target_w, target_h], fill="#2D241C")

    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr
