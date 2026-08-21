import os
import math
from PIL import Image, ImageDraw

icons_dir = os.path.join(os.path.dirname(__file__), "app", "static", "icons")
os.makedirs(icons_dir, exist_ok=True)

def create_icon_canvas(size=120):
    return Image.new("RGBA", (size, size), (0, 0, 0, 0))

def save_icon(img, name):
    img.save(os.path.join(icons_dir, name))

# 1. Rocket
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.polygon([(60, 15), (75, 45), (85, 75), (60, 65), (35, 75), (45, 45)], fill="#1E293B")
draw.polygon([(35, 70), (20, 85), (35, 80)], fill="#E58E26") # Left fin
draw.polygon([(85, 70), (100, 85), (85, 80)], fill="#E58E26") # Right fin
draw.ellipse([(52, 38), (68, 54)], fill="#60A5FA") # Window
draw.polygon([(50, 70), (60, 105), (70, 70)], fill="#EF4444") # Flame
save_icon(img, "rocket.png")

# 2. Shield (Security)
def gen_shield(color, name):
    img = create_icon_canvas()
    draw = ImageDraw.Draw(img)
    draw.polygon([(60, 15), (95, 28), (95, 65), (60, 105), (25, 65), (25, 28)], fill=color)
    draw.polygon([(60, 25), (85, 35), (85, 62), (60, 95), (35, 62), (35, 35)], fill="white")
    draw.polygon([(60, 32), (78, 40), (78, 60), (60, 85), (42, 60), (42, 40)], fill=color)
    save_icon(img, name)
gen_shield("#0C4A2B", "shield_green.png")
gen_shield("#1E3A5F", "shield_blue.png")
gen_shield("#C88A2E", "shield_gold.png")

# 3. Courthouse / Governance
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.polygon([(60, 20), (20, 45), (100, 45)], fill="#1F1F1F")
draw.rectangle([25, 45, 95, 52], fill="#1F1F1F")
for c in range(4):
    bx = 32 + c * 18
    draw.rectangle([bx, 52, bx + 8, 85], fill="#1F1F1F")
draw.rectangle([20, 85, 100, 95], fill="#1F1F1F")
save_icon(img, "courthouse.png")

# 4. Users / People
def gen_users(color, name):
    img = create_icon_canvas()
    draw = ImageDraw.Draw(img)
    draw.ellipse([45, 20, 75, 50], fill=color) # Center head
    draw.ellipse([25, 30, 47, 52], fill=color) # Left head
    draw.ellipse([73, 30, 95, 52], fill=color) # Right head
    draw.pieslice([35, 48, 85, 98], 180, 360, fill=color) # Center body
    draw.pieslice([15, 55, 55, 95], 180, 360, fill=color) # Left body
    draw.pieslice([65, 55, 105, 95], 180, 360, fill=color) # Right body
    save_icon(img, name)
gen_users("#1F1F1F", "users.png")
gen_users("white", "users_white.png")
gen_users("#C88A2E", "users_gold.png")
gen_users("#0C4A2B", "users_green.png")

# 5. Chart Up / Trend
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.rectangle([25, 70, 37, 95], fill="#1F1F1F")
draw.rectangle([45, 55, 57, 95], fill="#1F1F1F")
draw.rectangle([65, 40, 77, 95], fill="#1F1F1F")
draw.rectangle([85, 25, 97, 95], fill="#1F1F1F")
draw.polygon([(25, 55), (60, 30), (80, 40), (95, 15), (105, 25), (85, 48), (60, 38), (30, 62)], fill="#E58E26")
save_icon(img, "chart_up.png")

# 6. AI Chip
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.rectangle([30, 30, 90, 90], fill="#0C4A2B")
draw.rectangle([40, 40, 80, 80], fill="white")
draw.text((45, 48), "AI", fill="#0C4A2B")
for i in range(3):
    pos = 42 + i * 16
    draw.line([(pos, 15), (pos, 30)], fill="#0C4A2B", width=4)
    draw.line([(pos, 90), (pos, 105)], fill="#0C4A2B", width=4)
    draw.line([(15, pos), (30, pos)], fill="#0C4A2B", width=4)
    draw.line([(90, pos), (105, pos)], fill="#0C4A2B", width=4)
save_icon(img, "ai_chip.png")

# 7. Cloud Network
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.ellipse([30, 45, 60, 75], fill="#0C4A2B")
draw.ellipse([50, 30, 85, 65], fill="#0C4A2B")
draw.ellipse([70, 45, 95, 75], fill="#0C4A2B")
draw.rectangle([42, 55, 85, 75], fill="#0C4A2B")
draw.line([(60, 75), (60, 95)], fill="#0C4A2B", width=4)
draw.line([(40, 95), (80, 95)], fill="#0C4A2B", width=4)
save_icon(img, "cloud_network.png")

# 8. Testing File / QA
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.rectangle([30, 20, 85, 100], fill="#C88A2E")
draw.rectangle([36, 26, 79, 94], fill="white")
draw.line([(44, 40), (70, 40)], fill="#C88A2E", width=4)
draw.line([(44, 55), (70, 55)], fill="#C88A2E", width=4)
draw.line([(44, 70), (70, 70)], fill="#C88A2E", width=4)
save_icon(img, "qa_file.png")

# 9. Pen / Copywriter
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.polygon([(85, 20), (95, 30), (45, 80), (35, 70)], fill="#C88A2E")
draw.polygon([(45, 80), (35, 70), (25, 95)], fill="#1F1F1F")
save_icon(img, "pen.png")

# 10. Legal Scales
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.line([(60, 20), (60, 95)], fill="#1E3A5F", width=6)
draw.line([(25, 35), (95, 35)], fill="#1E3A5F", width=6)
draw.polygon([(20, 65), (45, 65), (32, 75)], fill="#1E3A5F")
draw.line([(32, 35), (20, 65)], fill="#1E3A5F", width=3)
draw.line([(32, 35), (45, 65)], fill="#1E3A5F", width=3)
draw.polygon([(75, 65), (100, 65), (87, 75)], fill="#1E3A5F")
draw.line([(87, 35), (75, 65)], fill="#1E3A5F", width=3)
draw.line([(87, 35), (100, 65)], fill="#1E3A5F", width=3)
draw.rectangle([45, 90, 75, 100], fill="#1E3A5F")
save_icon(img, "legal_scales.png")

# 11. Clipboard / Procurement
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.rectangle([30, 25, 90, 95], fill="#1E3A5F")
draw.rectangle([36, 31, 84, 89], fill="white")
draw.rectangle([48, 15, 72, 28], fill="#E58E26")
draw.line([(44, 45), (76, 45)], fill="#1E3A5F", width=3)
draw.line([(44, 60), (76, 60)], fill="#1E3A5F", width=3)
draw.line([(44, 75), (76, 75)], fill="#1E3A5F", width=3)
save_icon(img, "procurement.png")

# 12. IoT Tower
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.polygon([(60, 20), (35, 95), (45, 95), (60, 45), (75, 95), (85, 95)], fill="#1E3A5F")
draw.ellipse([52, 12, 68, 28], fill="#E58E26")
draw.arc([40, 5, 80, 45], 200, 340, fill="#E58E26", width=3)
draw.arc([30, -5, 90, 55], 200, 340, fill="#E58E26", width=3)
save_icon(img, "iot_tower.png")

# 13. Security Lock
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.arc([40, 20, 80, 60], 180, 360, fill="#1E3A5F", width=8)
draw.rectangle([32, 45, 88, 92], fill="#1E3A5F")
draw.ellipse([54, 60, 66, 72], fill="white")
draw.polygon([(57, 70), (63, 70), (65, 82), (55, 82)], fill="white")
save_icon(img, "security_lock.png")

# 14. Globe Portal (Gold / Blue)
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.ellipse([15, 15, 105, 105], outline="#E58E26", width=6)
draw.ellipse([38, 15, 82, 105], outline="#E58E26", width=5)
draw.line([15, 60, 105, 60], fill="#E58E26", width=5)
save_icon(img, "globe_portal.png")

# 21. Megaphone (White)
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.polygon([(35, 45), (75, 25), (75, 85), (35, 65)], fill="white") # Cone
draw.rectangle([25, 45, 35, 65], fill="white") # Back piece
draw.polygon([(45, 65), (55, 65), (50, 95), (42, 95)], fill="white") # Handle
draw.ellipse([70, 25, 80, 85], fill="white") # Front rim
# Sound waves
draw.arc([85, 35, 100, 75], -60, 60, fill="white", width=4)
draw.arc([95, 25, 115, 85], -60, 60, fill="white", width=4)
save_icon(img, "megaphone_white.png")

# 22. Gear (White)
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
for a in range(0, 360, 45):
    rad = math.radians(a)
    cx = 60 + int(38 * math.cos(rad))
    cy = 60 + int(38 * math.sin(rad))
    draw.rectangle([cx - 8, cy - 8, cx + 8, cy + 8], fill="white")
draw.ellipse([25, 25, 95, 95], fill="white")
draw.ellipse([45, 45, 75, 75], fill="#6B7280") # Center hole
save_icon(img, "gear_white.png")

# 23. Handshake
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.polygon([(20, 50), (45, 35), (60, 50), (35, 65)], fill="#1E293B")
draw.polygon([(100, 50), (75, 35), (60, 50), (85, 65)], fill="#0C4A2B")
draw.ellipse([50, 42, 70, 62], fill="#C88A2E")
draw.line([(35, 65), (50, 80)], fill="#1E293B", width=6)
draw.line([(85, 65), (70, 80)], fill="#0C4A2B", width=6)
save_icon(img, "handshake.png")

# 24. Calculator
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.rounded_rectangle([30, 20, 90, 100], radius=8, fill="#1E293B")
draw.rectangle([40, 30, 80, 45], fill="#93C5FD") # Screen
for r in range(3):
    for c in range(3):
        bx = 42 + c * 14
        by = 54 + r * 14
        draw.rectangle([bx, by, bx + 10, by + 10], fill="white")
save_icon(img, "calc.png")

# 25. Monitor / Portal
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.rounded_rectangle([25, 25, 95, 75], radius=6, fill="#1E293B")
draw.rectangle([32, 32, 88, 68], fill="#93C5FD") # Screen
draw.rectangle([54, 75, 66, 92], fill="#1E293B") # Stand
draw.rectangle([40, 92, 80, 98], fill="#1E293B") # Base
save_icon(img, "monitor.png")

# 26. Check Circle (Green)
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.ellipse([20, 20, 100, 100], fill="#0C4A2B")
draw.line([(38, 60), (52, 74), (82, 44)], fill="white", width=8)
save_icon(img, "check_circle.png")

# 27. White Qualification Grad & Briefcase
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.polygon([(60, 25), (100, 45), (60, 65), (20, 45)], fill="white")
draw.rectangle([40, 60, 80, 80], fill="white")
draw.line([(95, 45), (95, 80)], fill="white", width=4)
save_icon(img, "grad_white.png")

img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.rounded_rectangle([25, 40, 95, 95], radius=6, fill="white")
draw.rounded_rectangle([45, 25, 75, 45], radius=4, outline="white", width=4)
draw.line([(25, 65), (95, 65)], fill="#0C4A2B", width=4)
save_icon(img, "briefcase_white.png")

img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.polygon([(60, 20), (20, 45), (100, 45)], fill="white")
draw.rectangle([25, 45, 95, 52], fill="white")
for c in range(4):
    bx = 32 + c * 18
    draw.rectangle([bx, 52, bx + 8, 85], fill="white")
draw.rectangle([20, 85, 100, 95], fill="white")
save_icon(img, "courthouse_white.png")

print("All icons successfully generated!")

# 15. Pointer Cursor
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.polygon([(30, 20), (30, 90), (52, 70), (75, 100), (88, 90), (65, 60), (90, 60)], fill="#1F1F1F")
draw.polygon([(35, 28), (35, 80), (50, 65), (70, 92), (78, 87), (58, 60), (80, 60)], fill="white")
save_icon(img, "pointer_cursor.png")

# 16. Clock Round
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.ellipse([15, 15, 105, 105], fill="#0C4A2B")
draw.ellipse([22, 22, 98, 98], fill="#112A1B")
draw.line([(60, 60), (60, 32)], fill="#E5A93C", width=6)
draw.line([(60, 60), (80, 60)], fill="#E5A93C", width=6)
save_icon(img, "clock_round.png")

# 17. Target / Bullseye (Gold)
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.ellipse([15, 15, 105, 105], outline="#E5A93C", width=6)
draw.ellipse([35, 35, 85, 85], outline="#E5A93C", width=6)
draw.ellipse([50, 50, 70, 70], fill="#E5A93C")
save_icon(img, "target_gold.png")

# 18. Grad Cap (Gold)
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.polygon([(60, 25), (15, 48), (60, 70), (105, 48)], fill="#E5A93C")
draw.polygon([(35, 60), (35, 82), (60, 95), (85, 82), (85, 60), (60, 70)], fill="#E5A93C")
draw.line([(95, 52), (95, 85)], fill="#E5A93C", width=4)
save_icon(img, "grad_gold.png")

# 19. Currency / Rupee (Gold)
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.ellipse([15, 15, 105, 105], outline="#E5A93C", width=6)
# Rupee symbol
draw.line([(40, 36), (80, 36)], fill="#E5A93C", width=6)
draw.line([(40, 48), (75, 48)], fill="#E5A93C", width=5)
draw.arc([(35, 36), (75, 75)], 270, 90, fill="#E5A93C", width=6)
draw.line([(52, 68), (80, 92)], fill="#E5A93C", width=6)
save_icon(img, "rupee_gold.png")

# 20. Briefcase (Gold)
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.ellipse([15, 15, 105, 105], outline="#E5A93C", width=6)
draw.rectangle([32, 45, 88, 85], fill="#E5A93C")
draw.rectangle([48, 32, 72, 45], outline="#E5A93C", width=5)
save_icon(img, "briefcase_gold.png")

# Mail White
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.rectangle([20, 35, 100, 85], fill="#0C4A2B", outline="white", width=4)
draw.polygon([(20, 35), (60, 65), (100, 35)], fill="#0C4A2B", outline="white", width=4)
save_icon(img, "mail_white.png")

# Clock Round
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.ellipse([10, 10, 110, 110], fill="#0C4A2B", outline="#E5A93C", width=4)
draw.ellipse([18, 18, 102, 102], fill="#062E1A")
draw.line([(60, 60), (60, 28)], fill="#F59E0B", width=6)
draw.line([(60, 60), (84, 60)], fill="#F59E0B", width=6)
draw.ellipse([54, 54, 66, 66], fill="#F59E0B")
save_icon(img, "clock_round.png")

# India Map Silhouette Graphic with Glowing Pins
def create_india_map(w=260, h=260):
    img = Image.new("RGBA", (w, h), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    
    # Stylized India polygonal outline
    points = [
        (130, 20), (145, 35), (160, 45), (170, 60), (155, 75), (180, 85), 
        (210, 80), (235, 95), (245, 110), (225, 125), (200, 120), (185, 135),
        (175, 160), (165, 185), (150, 215), (135, 245), (125, 235), (115, 200),
        (95, 175), (75, 160), (60, 140), (45, 125), (55, 105), (85, 95),
        (80, 75), (95, 55), (115, 35)
    ]
    # Draw map body
    draw.polygon(points, fill="#D1D5DB", outline="#94A3B8")
    
    # Location pins
    pin_locations = [
        (95, 110),  # West / Bhopal
        (140, 95),  # North / Delhi
        (160, 115), # Lucknow
        (145, 170), # South / Vijayawada
        (225, 105)  # East / Manipur
    ]
    
    for px, py in pin_locations:
        # Glow circle
        draw.ellipse([px-12, py-12, px+12, py+12], fill=(245, 158, 11, 100))
        # Marker pin
        draw.ellipse([px-7, py-14, px+7, py], fill="#D97706")
        draw.polygon([(px-7, py-7), (px+7, py-7), (px, py+5)], fill="#D97706")
        draw.ellipse([px-2, py-11, px+2, py-7], fill="white")
        
    save_icon(img, "india_map.png")

# Monitor Lock (Role 2 Icon)
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.rounded_rectangle([15, 15, 105, 105], radius=14, fill="#55634D")
draw.rounded_rectangle([25, 25, 95, 78], radius=6, outline="white", width=4)
draw.rectangle([54, 78, 66, 92], fill="white")
draw.rectangle([40, 92, 80, 98], fill="white")
# Lock in center
draw.rounded_rectangle([48, 46, 72, 68], radius=4, fill="white")
draw.arc([52, 34, 68, 52], 180, 0, fill="white", width=4)
save_icon(img, "monitor_lock.png")

# Clipboard Icon (Role 1 Icon)
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.rounded_rectangle([15, 15, 105, 105], radius=14, fill="#55634D")
draw.rounded_rectangle([30, 24, 90, 96], radius=6, outline="white", width=4)
draw.rounded_rectangle([44, 16, 76, 28], radius=3, fill="white")
# Lines & Check
draw.line([(40, 42), (80, 42)], fill="white", width=3)
draw.line([(40, 56), (80, 56)], fill="white", width=3)
draw.line([(40, 70), (80, 70)], fill="white", width=3)
draw.line([(40, 84), (65, 84)], fill="white", width=3)
save_icon(img, "clipboard_lines.png")

# Bell Outline for Stay Tuned
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.ellipse([10, 10, 110, 110], outline="white", width=5)
draw.polygon([(60, 26), (36, 72), (84, 72)], fill="white")
draw.rectangle([32, 72, 88, 78], fill="white")
draw.ellipse([52, 78, 68, 90], fill="white")
draw.ellipse([56, 18, 64, 26], fill="white")
save_icon(img, "bell_outline.png")

# Clipboard Shield
img = create_icon_canvas()
draw = ImageDraw.Draw(img)
draw.rounded_rectangle([25, 20, 95, 100], radius=8, fill="#55634D")
draw.rectangle([42, 12, 78, 25], fill="#1F2937")
draw.polygon([(60, 45), (80, 55), (80, 75), (60, 90), (40, 75), (40, 55)], fill="white")
draw.line([(48, 65), (56, 73), (72, 57)], fill="#55634D", width=4)
save_icon(img, "clipboard_shield.png")

create_india_map()
print("Icons updated successfully!")

