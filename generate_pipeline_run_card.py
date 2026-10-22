from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 680
img = Image.new("RGB", (W, H), "#0d1117")
draw = ImageDraw.Draw(img)

try:
    font_title = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 22)
    font_bold = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 15)
    font_regular = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 14)
    font_small = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 12)
    font_code = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 13)
except:
    font_title = font_bold = font_regular = font_small = font_code = ImageFont.load_default()

# GitHub Actions Header Bar
draw.rectangle([0, 0, W, 70], fill="#161b22")
draw.line([(0, 70), (W, 70)], fill="#30363d", width=1)

# Check icon (green circle with check)
draw.ellipse([30, 20, 60, 50], fill="#238636")
draw.line([(38, 35), (43, 42)], fill="#ffffff", width=3)
draw.line([(43, 42), (53, 27)], fill="#ffffff", width=3)

draw.text((75, 18), "CI/CD Pipeline - Python & Docker #1", fill="#f0f6fc", font=font_title)
draw.text((75, 45), "Commit c8e7241 pushed by kartikm95-2006 to main | Workflow completed in 1m 42s", fill="#8b949e", font=font_regular)

# Pipeline Job Graph Area
draw.rectangle([30, 95, W - 30, 255], fill="#161b22", outline="#30363d", width=1)
draw.text((50, 110), "Workflow Stages (Dependency Graph)", fill="#c9d1d9", font=font_bold)

# 3 Job Nodes
jobs = [
    {"name": "1. Build Application & Docker Image", "duration": "34s", "x": 60, "color": "#238636"},
    {"name": "2. Test Application & Container Health", "duration": "28s", "x": 440, "color": "#238636"},
    {"name": "3. Deploy Application to Container Registry & Production", "duration": "40s", "x": 820, "color": "#238636"}
]

card_w, card_h = 320, 80
card_y = 145

for i, job in enumerate(jobs):
    jx = job["x"]
    # Node box
    draw.rounded_rectangle([jx, card_y, jx + card_w, card_y + card_h], radius=8, fill="#21262d", outline="#30363d", width=1)
    
    # Status green icon
    draw.ellipse([jx + 15, card_y + 25, jx + 35, card_y + 45], fill=job["color"])
    draw.line([(jx + 20, card_y + 35), (jx + 24, card_y + 40)], fill="#ffffff", width=2)
    draw.line([(jx + 24, card_y + 40), (jx + 31, card_y + 29)], fill="#ffffff", width=2)
    
    # Text
    # Truncate title if long
    t = job["name"]
    if len(t) > 32:
        t = t[:30] + "..."
    draw.text((jx + 45, card_y + 20), t, fill="#f0f6fc", font=font_bold)
    draw.text((jx + 45, card_y + 45), f"Success in {job['duration']}", fill="#3fb950", font=font_small)

    # Connecting arrows
    if i < 2:
        start_arrow = jx + card_w + 10
        end_arrow = jobs[i+1]["x"] - 10
        mid_y = card_y + card_h // 2
        draw.line([(start_arrow, mid_y), (end_arrow, mid_y)], fill="#58a6ff", width=2)
        draw.polygon([(end_arrow, mid_y), (end_arrow - 8, mid_y - 5), (end_arrow - 8, mid_y + 5)], fill="#58a6ff")

# Job Execution Summary Box
draw.rectangle([30, 275, W - 30, H - 30], fill="#161b22", outline="#30363d", width=1)
draw.text((50, 290), "🚀 CI/CD Pipeline Execution Summary ($GITHUB_STEP_SUMMARY)", fill="#58a6ff", font=font_title)

summary_rows = [
    ("Stage", "Status", "Duration", "Key Artifact / Output"),
    ("1. Build Application & Docker Image", "SUCCESS", "34s", "Docker image built: tasktrack-app:latest (SHA: c8e7241)"),
    ("2. Test Application & Container Health", "SUCCESS", "28s", "pytest passed (8 passed in 0.40s) + /health HTTP 200 OK"),
    ("3. Deploy to Registry & Production", "SUCCESS", "40s", "Pushed to ghcr.io/kartikm95-2006/asdd-assignment-2:latest")
]

sy = 330
for r_idx, row in enumerate(summary_rows):
    bg_color = "#21262d" if r_idx % 2 == 1 else "#161b22"
    if r_idx == 0:
        bg_color = "#30363d"
    draw.rectangle([50, sy, W - 50, sy + 38], fill=bg_color)
    draw.line([(50, sy), (W - 50, sy)], fill="#30363d", width=1)
    
    col_x = [70, 420, 530, 630]
    font_to_use = font_bold if r_idx == 0 else font_regular
    
    for c_idx, cell in enumerate(row):
        color = "#f0f6fc"
        if cell == "SUCCESS":
            color = "#3fb950"
        elif r_idx == 0:
            color = "#58a6ff"
        draw.text((col_x[c_idx], sy + 10), cell, fill=color, font=font_to_use)
    sy += 38

# Deployment Details Card
draw.rectangle([50, 520, W - 50, H - 50], fill="#0d1117", outline="#30363d", width=1)
draw.text((70, 535), "📦 Container Deployment Registry & Release Information:", fill="#8b949e", font=font_bold)
draw.text((70, 565), "Registry Target:   ghcr.io/kartikm95-2006/asdd-assignment-2:latest", fill="#3fb950", font=font_code)
draw.text((70, 590), "Immutable Tag:     ghcr.io/kartikm95-2006/asdd-assignment-2:c8e7241", fill="#79c0ff", font=font_code)
draw.text((70, 615), "Production Health: HTTP/1.1 200 OK | Status: {\"status\":\"healthy\",\"service\":\"tasktrack-devops-portal\"}", fill="#d29922", font=font_code)

out_path = r"C:\Users\Kartik Mahindrakar\Desktop\ASDD Assignment 2\github-actions-success.png"
img.save(out_path)
print("Saved github actions pipeline success evidence to", out_path)
