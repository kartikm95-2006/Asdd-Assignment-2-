from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 480
img = Image.new("RGB", (W, H), "#0b1320")
draw = ImageDraw.Draw(img)

try:
    font_title = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 28)
    font_sub = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 16)
    font_box_title = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 20)
    font_box_desc = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 14)
    font_box_tag = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 12)
except:
    font_title = font_sub = font_box_title = font_box_desc = font_box_tag = ImageFont.load_default()

# Header
draw.text((40, 30), "Automated CI/CD Pipeline Architecture (GitHub Actions & Docker)", fill="#f8fafc", font=font_title)
draw.text((40, 70), "Project: TaskTrack DevOps Portal | Student: Kartik Mahindrakar (Roll No: 99)", fill="#94a3b8", font=font_sub)

# Draw 3 Pipeline Stage Boxes
stages = [
    {
        "stage": "STAGE 1",
        "title": "Build Stage",
        "icon": "[ BUILD ]",
        "color": "#3b82f6",
        "bg": "#1e293b",
        "items": [
            "- Checkout repository",
            "- Setup Python 3.12 environment",
            "- Compile & validate syntax",
            "- Build Docker container image",
            "- Tag: tasktrack-app:latest"
        ],
        "status": "PASS: Image Compiled"
    },
    {
        "stage": "STAGE 2",
        "title": "Test Stage",
        "icon": "[ TEST ]",
        "color": "#10b981",
        "bg": "#1e293b",
        "items": [
            "- Run Pytest suite (8/8 pass)",
            "- Validate REST API endpoints",
            "- Spin up container in test mode",
            "- Query live /health endpoint",
            "- Automated container teardown"
        ],
        "status": "PASS: 8/8 Tests Succeeded"
    },
    {
        "stage": "STAGE 3",
        "title": "Deploy Stage",
        "icon": "[ DEPLOY ]",
        "color": "#a855f7",
        "bg": "#1e293b",
        "items": [
            "- Authenticate with GHCR",
            "- Tag ghcr.io/<repo>:latest",
            "- Push image to Docker registry",
            "- Launch production container",
            "- HTTP 200 response verified"
        ],
        "status": "PASS: GHCR Deployed"
    }
]

box_w, box_h = 340, 310
start_y = 120
gap = 45

for i, s in enumerate(stages):
    bx = 40 + i * (box_w + gap)
    by = start_y
    
    # Outer card
    draw.rounded_rectangle([bx, by, bx + box_w, by + box_h], radius=12, fill=s["bg"], outline="#334155", width=2)
    # Header strip
    draw.rounded_rectangle([bx, by, bx + box_w, by + 45], radius=12, fill="#182234")
    draw.rectangle([bx, by + 30, bx + box_w, by + 45], fill="#182234")
    draw.rectangle([bx, by + 43, bx + box_w, by + 45], fill=s["color"])
    
    # Tag and title
    draw.text((bx + 16, by + 12), s["stage"], fill=s["color"], font=font_box_tag)
    draw.text((bx + 85, by + 10), s["title"], fill="#f8fafc", font=font_box_title)
    
    # Bullet points
    item_y = by + 65
    for item in s["items"]:
        draw.text((bx + 18, item_y), item, fill="#cbd5e1", font=font_box_desc)
        item_y += 32
        
    # Status badge at bottom
    draw.rounded_rectangle([bx + 16, by + box_h - 45, bx + box_w - 16, by + box_h - 15], radius=6, fill="#0f172a", outline=s["color"], width=1)
    draw.text((bx + 30, by + box_h - 38), s["status"], fill="#38bdf8", font=font_box_tag)

    # Draw arrow connecting stages
    if i < 2:
        arrow_x = bx + box_w + 8
        arrow_y = by + box_h // 2 - 10
        draw.text((arrow_x, arrow_y), "==>", fill="#64748b", font=font_box_title)

out_path = r"C:\Users\Kartik Mahindrakar\Desktop\ASDD Assignment 2\pipeline-architecture.png"
img.save(out_path)
print("Saved pipeline architecture image to", out_path)
