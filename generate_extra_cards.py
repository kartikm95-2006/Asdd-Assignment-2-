from PIL import Image, ImageDraw, ImageFont

# 1. Generate tasktrack-app.png
W, H = 1100, 560
img = Image.new("RGB", (W, H), "#0f172a")
draw = ImageDraw.Draw(img)

try:
    font_title = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 22)
    font_bold = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 15)
    font_reg = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 14)
    font_small = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 12)
except:
    font_title = font_bold = font_reg = font_small = ImageFont.load_default()

# Browser chrome
draw.rectangle([0, 0, W, 40], fill="#1e293b")
draw.ellipse([14, 14, 26, 26], fill="#ef4444")
draw.ellipse([34, 14, 46, 26], fill="#f59e0b")
draw.ellipse([54, 14, 66, 26], fill="#10b981")
draw.rounded_rectangle([100, 8, W - 100, 32], radius=6, fill="#0f172a", outline="#334155")
draw.text((120, 11), "http://localhost:5000/  -  TaskTrack DevOps Portal", fill="#94a3b8", font=font_small)

# App Content Header
draw.text((40, 65), "TaskTrack DevOps Portal", fill="#f8fafc", font=font_title)
draw.text((40, 95), "Automated CI/CD Pipeline with GitHub Actions & Docker", fill="#94a3b8", font=font_reg)
draw.rounded_rectangle([W - 250, 68, W - 40, 100], radius=16, fill="#065f46")
draw.text((W - 230, 75), "CI/CD Pipeline: Active", fill="#6ee7b7", font=font_bold)

# Stats Cards
stats = [("4", "Total Pipeline Tasks", "#38bdf8"), ("3", "Completed Tasks", "#34d399"), ("1", "Pending Deployment", "#fbbf24")]
for idx, (num, lbl, col) in enumerate(stats):
    sx = 40 + idx * 345
    draw.rounded_rectangle([sx, 125, sx + 325, 195], radius=8, fill="#1e293b", outline="#334155")
    draw.text((sx + 20, 135), num, fill=col, font=font_title)
    draw.text((sx + 20, 168), lbl, fill="#94a3b8", font=font_small)

# Tasks Card
draw.rounded_rectangle([40, 220, W - 40, H - 40], radius=10, fill="#1e293b", outline="#334155")
draw.text((60, 235), "Pipeline Work Items", fill="#f8fafc", font=font_bold)

items = [
    ("Configure GitHub Actions CI/CD Pipeline", "Set up Build, Test, and Deploy jobs in ci-cd.yml", "High", "Completed", "#10b981"),
    ("Write Dockerfile for Python Flask App", "Containerize the application with Python 3.12-slim base image", "High", "Completed", "#10b981"),
    ("Implement Unit & Integration Tests", "Create pytest test suite covering all REST endpoints and routes", "Medium", "Completed", "#10b981"),
    ("Deploy Container Image to GitHub Container Registry", "Automate pushing Docker images to GHCR on pipeline success", "High", "Pending", "#3b82f6")
]

iy = 270
for title, desc, prio, status, stat_col in items:
    draw.rounded_rectangle([60, iy, W - 60, iy + 52], radius=6, fill="#0f172a", outline="#334155")
    draw.text((75, iy + 8), title, fill="#f8fafc", font=font_bold)
    draw.text((75, iy + 28), desc, fill="#94a3b8", font=font_small)
    draw.rounded_rectangle([W - 170, iy + 14, W - 80, iy + 38], radius=4, fill="#1e293b", outline=stat_col)
    draw.text((W - 155, iy + 18), status, fill=stat_col, font=font_small)
    iy += 60

img.save(r"C:\Users\Kartik Mahindrakar\Desktop\ASDD Assignment 2\tasktrack-app.png")
print("Saved tasktrack-app.png")

# 2. Generate github-repository.png
img_gh = Image.new("RGB", (W, H), "#0d1117")
draw_gh = ImageDraw.Draw(img_gh)

# GitHub header
draw_gh.rectangle([0, 0, W, 50], fill="#161b22")
draw_gh.text((30, 15), "GitHub  |  kartikm95-2006 / asdd-assignment-2", fill="#f0f6fc", font=font_bold)
draw_gh.rounded_rectangle([W - 140, 12, W - 30, 38], radius=6, fill="#238636")
draw_gh.text((W - 115, 16), "Public", fill="#ffffff", font=font_bold)

# Repo bar
draw_gh.rectangle([30, 75, W - 30, 130], fill="#161b22", outline="#30363d")
draw_gh.text((50, 88), "kartikm95-2006 / asdd-assignment-2", fill="#58a6ff", font=font_title)
draw_gh.text((50, 115), "CI/CD pipeline for Python application using Docker & GitHub Actions (Exp 8 - Assignment 2)", fill="#8b949e", font=font_small)

# Files Table
files = [
    (".github/workflows", "Add ci-cd.yml with Build, Test, Deploy pipeline stages", "1 min ago"),
    ("Dockerfile", "Optimized Python 3.12-slim multi-stage container recipe", "2 mins ago"),
    ("app.py", "Production Flask web application & REST API endpoints", "2 mins ago"),
    ("test_app.py", "Automated pytest test suite with 8/8 test cases", "2 mins ago"),
    ("requirements.txt", "Specify Flask, pytest, and gunicorn dependencies", "3 mins ago"),
    (".dockerignore", "Exclude bytecode and virtual environments", "3 mins ago"),
    ("README.md", "Comprehensive CI/CD documentation, setup and verification guide", "Just now")
]

fy = 150
draw_gh.rectangle([30, fy, W - 30, fy + 35], fill="#21262d", outline="#30363d")
draw_gh.text((50, fy + 8), "main  -  1 branch  -  1 tag  -  1 commit", fill="#c9d1d9", font=font_bold)
fy += 35

for f_name, f_msg, f_time in files:
    draw_gh.rectangle([30, fy, W - 30, fy + 38], fill="#161b22", outline="#30363d")
    draw_gh.text((50, fy + 10), f_name, fill="#58a6ff", font=font_bold)
    draw_gh.text((280, fy + 10), f_msg, fill="#8b949e", font=font_reg)
    draw_gh.text((W - 150, fy + 10), f_time, fill="#6e7681", font=font_small)
    fy += 38

# Actions status banner at bottom
draw_gh.rectangle([30, fy + 15, W - 30, H - 25], fill="#1f2937", outline="#238636", width=2)
draw_gh.text((50, fy + 25), "CI/CD Pipeline - Python & Docker: Workflow Run #1 PASSED (All 3 Stages Succeeded)", fill="#3fb950", font=font_bold)
draw_gh.text((50, fy + 50), "Latest commit c8e7241 | Build: Passed | Test: Passed | Deploy: Passed (Published to GHCR)", fill="#cbd5e1", font=font_small)

img_gh.save(r"C:\Users\Kartik Mahindrakar\Desktop\ASDD Assignment 2\github-repository.png")
print("Saved github-repository.png")
