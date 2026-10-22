from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image,
    PageBreak, Preformatted, KeepTogether
)

ROOT = Path(__file__).parent
OUT = ROOT / "Assignment-2-Python-CI-CD-Report.pdf"

# Fonts
pdfmetrics.registerFont(TTFont("Arial", r"C:\Windows\Fonts\arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", r"C:\Windows\Fonts\arialbd.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Italic", r"C:\Windows\Fonts\ariali.ttf"))
pdfmetrics.registerFont(TTFont("Georgia", r"C:\Windows\Fonts\georgia.ttf"))
pdfmetrics.registerFont(TTFont("Georgia-Bold", r"C:\Windows\Fonts\georgiab.ttf"))
pdfmetrics.registerFont(TTFont("Georgia-Italic", r"C:\Windows\Fonts\georgiai.ttf"))

styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name="ReportTitle", parent=styles["Title"], fontName="Georgia-Bold",
    fontSize=24, leading=28, textColor=colors.HexColor("#0f172a"),
    alignment=TA_CENTER, spaceAfter=6,
))
styles.add(ParagraphStyle(
    name="Subtitle", parent=styles["Normal"], fontName="Georgia-Italic", fontSize=12, leading=16,
    textColor=colors.HexColor("#2563eb"), alignment=TA_CENTER, spaceAfter=18,
))
styles.add(ParagraphStyle(
    name="Section", parent=styles["Heading2"], fontName="Georgia-Bold",
    fontSize=16, leading=20, textColor=colors.HexColor("#0f172a"),
    spaceBefore=14, spaceAfter=8,
))
styles.add(ParagraphStyle(
    name="Subsection", parent=styles["Heading3"], fontName="Georgia-Bold",
    fontSize=12, leading=16, textColor=colors.HexColor("#1e293b"),
    spaceBefore=9, spaceAfter=5,
))
styles.add(ParagraphStyle(
    name="Body", parent=styles["BodyText"], fontName="Georgia", fontSize=9.5, leading=14.5,
    textColor=colors.HexColor("#1e293b"), spaceAfter=5,
))
styles.add(ParagraphStyle(
    name="Small", parent=styles["BodyText"], fontName="Georgia", fontSize=8.5, leading=11.5,
    textColor=colors.HexColor("#475569"), spaceAfter=3,
))
styles.add(ParagraphStyle(
    name="Caption", parent=styles["BodyText"], fontName="Georgia-Bold",
    fontSize=9.5, leading=13, textColor=colors.HexColor("#0f172a"), spaceBefore=4,
))
styles.add(ParagraphStyle(
    name="CodeSmall", parent=styles["Code"], fontName="Courier",
    fontSize=6.8, leading=8.8, textColor=colors.HexColor("#e2e8f0"),
))

def P(text, style="Body"):
    return Paragraph(text, styles[style])

def code_panel(text):
    code = Preformatted(text, styles["CodeSmall"])
    panel = Table([[code]], colWidths=[6.45 * inch])
    panel.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#0f172a")),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#334155")),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    return panel

def evidence(image_name, title, explanation):
    image_path = ROOT / image_name
    if not image_path.exists():
        return KeepTogether([P(f"[Missing Image: {image_name}]", "Caption")])
    source_width, source_height = PILImage.open(image_path).size
    max_width, max_height = 6.45 * inch, 3.8 * inch
    scale = min(max_width / source_width, max_height / source_height)
    image = Image(str(image_path), width=source_width * scale, height=source_height * scale)
    image.hAlign = "CENTER"
    card = Table([[P(title, "Caption")], [image], [P(explanation, "Small")]], colWidths=[6.45 * inch])
    card.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#cbd5e1")),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return KeepTogether([card])

def cover(canvas, doc):
    canvas.saveState()
    paper = colors.HexColor("#f8fafc")
    blue = colors.HexColor("#2563eb")
    dark = colors.HexColor("#0f172a")
    
    # Header Accent Bar
    canvas.setFillColor(blue)
    canvas.rect(42, 785, A4[0] - 84, 15, fill=1, stroke=0)
    
    # Institution & Dept Header
    canvas.setFillColor(dark)
    canvas.setFont("Arial-Bold", 11)
    canvas.drawCentredString(A4[0] / 2, 760, "A. P. SHAH INSTITUTE OF TECHNOLOGY, THANE")
    canvas.setFont("Arial", 9.5)
    canvas.drawCentredString(A4[0] / 2, 744, "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING (AI & ML)")
    canvas.setFont("Arial-Italic", 9)
    canvas.drawCentredString(A4[0] / 2, 730, "Academic Year: 2026-27 | Semester V | ASSD Lab")
    
    # Dividing Line
    canvas.setStrokeColor(colors.HexColor("#cbd5e1"))
    canvas.line(42, 715, A4[0] - 42, 715)
    
    # Title Box
    canvas.setFillColor(paper)
    canvas.rect(42, 490, A4[0] - 84, 210, fill=1, stroke=0)
    canvas.setFillColor(blue)
    canvas.rect(42, 490, 8, 210, fill=1, stroke=0)
    
    canvas.setFillColor(blue)
    canvas.setFont("Arial-Bold", 10)
    canvas.drawString(65, 672, "LAB ASSIGNMENT - 2  |  EXPERIMENT 8")
    
    canvas.setFillColor(dark)
    canvas.setFont("Georgia-Bold", 20)
    canvas.drawString(65, 642, "CI/CD Pipeline for Python Application")
    canvas.setFont("Georgia", 16)
    canvas.drawString(65, 618, "Automated Build, Test & Deployment with Docker & GitHub Actions")
    
    # Metadata Table Box on Cover
    left_x, right_x = 65, 330
    y = 570
    canvas.setFont("Arial-Bold", 8.5)
    canvas.drawString(left_x, y, "STUDENT NAME")
    canvas.drawString(right_x, y, "CLASS & DIVISION")
    canvas.setFont("Georgia", 10.5)
    canvas.drawString(left_x, y - 14, "Kartik Mahindrakar")
    canvas.drawString(right_x, y - 14, "T.E. / Div B / CSE(AI&ML) - Roll No: 99")
    
    y = 525
    canvas.setFont("Arial-Bold", 8.5)
    canvas.drawString(left_x, y, "STUDENT ID / INSTRUCTOR")
    canvas.drawString(right_x, y, "GITHUB REPOSITORY")
    canvas.setFont("Georgia", 10.5)
    canvas.drawString(left_x, y - 14, "24106126 / Prof. Radhika Bailurkar")
    canvas.drawString(right_x, y - 14, "github.com/kartikm95-2006/asdd-assignment-2")
    
    # Problem Statement Summary Box
    canvas.setFillColor(colors.HexColor("#f1f5f9"))
    canvas.roundRect(42, 335, A4[0] - 84, 135, 8, fill=1, stroke=0)
    canvas.setFillColor(dark)
    canvas.setFont("Arial-Bold", 9.5)
    canvas.drawString(60, 445, "PROBLEM STATEMENT & OBJECTIVES:")
    canvas.setFont("Georgia", 9)
    canvas.drawString(60, 425, "Develop and implement an automated CI/CD pipeline for a Python project using GitHub Actions.")
    canvas.drawString(60, 408, "The pipeline must automate Building the Docker image, Testing application endpoints via pytest,")
    canvas.drawString(60, 391, "and Deploying the application to GitHub Container Registry (GHCR) with live container verification.")
    canvas.drawString(60, 374, "Output: Fully automated Build -> Test -> Deploy pipeline, Dockerfile, workflow YAML, and evidence.")
    canvas.drawString(60, 352, "Date of Performance: 22/10/2026               Date of Submission: 22/10/2026")
    
    canvas.restoreState()

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#cbd5e1"))
    canvas.line(42, 32, A4[0] - 42, 32)
    canvas.setFont("Arial", 8)
    canvas.setFillColor(colors.HexColor("#64748b"))
    canvas.drawString(42, 20, "APSIT CSE (AI&ML) | ASSD Lab Assignment - 2 (Python CI/CD with Docker)")
    canvas.drawRightString(A4[0] - 42, 20, f"Page {doc.page}")
    canvas.restoreState()

story = [Spacer(1, 1), PageBreak()]

# Section 1: Explain CI/CD Pipeline
story.extend([
    P("1. Explanation of the CI/CD Pipeline", "Section"),
    P("Continuous Integration (CI) and Continuous Deployment (CD) represent a modern DevOps paradigm designed to automate the software delivery lifecycle. In this project, a 3-stage pipeline is constructed using GitHub Actions runners and Docker containerization.", "Body"),
    P("Purpose of Pipeline Stages:", "Subsection"),
    P("<b>1. Build Stage:</b> The primary goal of the build stage is to turn human-readable source code into a reliable, executable, and portable artifact. In our Python application, this encompasses validating code compilation, resolving dependencies listed in <code>requirements.txt</code>, setting up Docker Buildx, and building the container image <code>tasktrack-app:latest</code>. Isolating the environment inside a container ensures cross-platform consistency and eliminates the classic 'it works on my machine' issue.", "Body"),
    P("<b>2. Test Stage:</b> The test stage ensures code quality, functionality, and regression prevention before any code can be approved for production. In our pipeline, this stage executes two layers of automated verification: (a) automated unit and integration tests using <code>pytest</code> covering REST endpoints and status codes, and (b) container runtime verification, where the Docker image is launched and the <code>/health</code> HTTP probe is tested.", "Body"),
    P("<b>3. Deploy Stage:</b> The deployment stage automates releasing the tested software to the target environment. In our pipeline, it authenticates with <b>GitHub Container Registry (GHCR)</b> using <code>GITHUB_TOKEN</code>, tags the Docker image with semantic and immutable commit SHA tags, pushes the image to GHCR, boots up the production container, and validates deployment with an automated HTTP probe.", "Body"),
    P("Execution Sequence and Dependency Enforcement:", "Subsection"),
    P("The stages execute in a strict sequential dependency graph: <b>Build ➔ Test ➔ Deploy</b>. This order is strictly enforced using GitHub Actions' <code>needs</code> keyword:", "Body"),
    P("&bull; The <b>Test</b> job declares <code>needs: build</code>, guaranteeing tests only run if compilation and Docker image creation succeed.<br/>&bull; The <b>Deploy</b> job declares <code>needs: test</code>, ensuring buggy or broken code is halted immediately and never pushed to production registries.", "Body"),
    Spacer(1, 4),
    evidence("pipeline-architecture.png", "Figure 1: Automated CI/CD Pipeline Architecture & Stage Execution Graph", "Diagram illustrating the 3 sequential pipeline stages: Build (compilation & image packaging), Test (automated pytest suite & health probe), and Deploy (GHCR publication & live verification)."),
    PageBreak(),
])

# Section 2: Dockerfile
story.extend([
    P("2. Dockerfile Implementation and Analysis", "Section"),
    P("The application is containerized using an optimized, secure Dockerfile based on official lightweight Python 3.12 slim distribution. Below is the complete content of the Dockerfile followed by an instruction-by-instruction technical breakdown.", "Body"),
])

dockerfile_content = """# Step 1: Base Image - Official lightweight Python 3.12 slim
FROM python:3.12-slim

# Step 2: Set Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Step 3: Set Working Directory inside container
WORKDIR /app

# Step 4: Security - Create dedicated non-root user and group
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Step 5: Leverage Docker Layer Caching for Dependencies
COPY requirements.txt /app/

# Step 6: Install dependencies without caching pip packages
RUN pip install --no-cache-dir -r requirements.txt

# Step 7: Copy application source code into image
COPY . /app/

# Step 8: Change file ownership to non-root user
RUN chown -R appuser:appgroup /app

# Step 9: Switch to non-root user for security compliance
USER appuser

# Step 10: Expose network port 5000
EXPOSE 5000

# Step 11: Container Health Check (polls /health endpoint every 30s)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \\
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Step 12: Production command using Gunicorn WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]"""

story.extend([
    code_panel(dockerfile_content),
    Spacer(1, 6),
    P("Dockerfile Instructions Breakdown:", "Subsection"),
    P("<b>1. FROM python:3.12-slim:</b> Pulls the minimal Debian-based official Python 3.12 image (~140MB). It avoids unnecessary build utilities, minimizing container vulnerabilities and build latency.", "Body"),
    P("<b>2. ENV Variables:</b> <code>PYTHONDONTWRITEBYTECODE=1</code> avoids writing temporary <code>.pyc</code> cache files into the container image. <code>PYTHONUNBUFFERED=1</code> streams application log output directly to stdout/stderr in real time without terminal buffering.", "Body"),
    P("<b>3. WORKDIR /app:</b> Sets <code>/app</code> as the execution and working directory for all subsequent commands (RUN, COPY, CMD).", "Body"),
    P("<b>4. Non-Root User (appuser):</b> Following container security best practices, a dedicated non-privileged user and group are created. Running as root inside a container represents a major security vulnerability.", "Body"),
    P("<b>5. Layer Caching (COPY requirements.txt):</b> By copying <code>requirements.txt</code> alone before the application code, Docker can cache the installed pip packages layer. Re-building after minor source code edits takes seconds instead of re-downloading dependencies.", "Body"),
    P("<b>6. HEALTHCHECK:</b> Configures a self-healing health monitor using Python's standard library <code>urllib.request</code> to probe <code>http://localhost:5000/health</code> every 30 seconds.", "Body"),
    P("<b>7. CMD Gunicorn:</b> Uses <code>gunicorn</code>, an industry-standard WSGI HTTP server running 2 worker processes, rather than Flask's single-threaded development server.", "Body"),
    PageBreak(),
])

# Section 3: GitHub Actions Workflow
story.extend([
    P("3. GitHub Actions Workflow Configuration", "Section"),
    P("The workflow is defined in <code>.github/workflows/ci-cd.yml</code>. It specifies automated triggers, necessary security permissions, runner configurations, and the three interdependent jobs (Build, Test, Deploy).", "Body"),
])

workflow_yaml = """name: CI/CD Pipeline - Python & Docker

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:

permissions:
  contents: read
  packages: write

jobs:
  build:
    name: 1. Build Application & Docker Image
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12', cache: 'pip' }
      - run: pip install -r requirements.txt
      - run: python -m compileall app.py test_app.py
      - uses: docker/setup-buildx-action@v3
      - run: docker build -t tasktrack-app:latest -t tasktrack-app:${{ github.sha }} .

  test:
    name: 2. Test Application & Container Health
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install -r requirements.txt
      - run: python -m pytest test_app.py -v
      - run: docker build -t tasktrack-test:latest .
      - run: |
          docker run -d --name test-container -p 5000:5000 tasktrack-test:latest
          sleep 6
          curl --fail http://localhost:5000/health
          docker stop test-container

  deploy:
    name: 3. Deploy Application to Container Registry & Production
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - run: |
          IMAGE_REPO=$(echo "ghcr.io/${{ github.repository }}" | tr '[:upper:]' '[:lower:]')
          docker build -t "$IMAGE_REPO:latest" -t "$IMAGE_REPO:${{ github.sha }}" .
          docker push "$IMAGE_REPO:latest"
          docker push "$IMAGE_REPO:${{ github.sha }}"
      - run: |
          IMAGE_REPO=$(echo "ghcr.io/${{ github.repository }}" | tr '[:upper:]' '[:lower:]')
          docker run -d --name prod -p 5000:5000 "$IMAGE_REPO:latest"
          sleep 6
          curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/ | grep -q 200"""

story.extend([
    code_panel(workflow_yaml),
    Spacer(1, 6),
    P("Key Workflow Features Explained:", "Subsection"),
    P("<b>&bull; Triggers (<code>on:</code>):</b> Configured for automated push events, pull requests, and manual execution via <code>workflow_dispatch</code>.", "Body"),
    P("<b>&bull; Permissions (<code>packages: write</code>):</b> Automatically grants the workflow permission to push the built container image to GitHub Container Registry using the built-in <code>GITHUB_TOKEN</code> without manual credentials.", "Body"),
    P("<b>&bull; Test Isolation:</b> The test job executes both standalone Python tests via <code>pytest</code> and starts the Docker container to perform integration testing on the live network port.", "Body"),
    P("<b>&bull; Deployment Verification:</b> The deploy job tags images with both mutable (<code>latest</code>) and immutable (<code>${{ github.sha }}</code>) tags, pushes to GHCR, and performs a live curl validation probe verifying HTTP 200 OK.", "Body"),
    PageBreak(),
])

# Section 4: Execution and Verification
story.extend([
    P("4. Execution and Verification of the Pipeline", "Section"),
    P("The project was implemented, tested locally, committed to Git version control, and pushed to GitHub to trigger the automated CI/CD pipeline.", "Body"),
    P("Git Operations Log:", "Subsection"),
])

commands = [
    [P("Command", "Small"), P("Purpose", "Small")],
    [P("git init -b main", "Small"), P("Initializes the Git repository on the main branch.", "Small")],
    [P("git add .", "Small"), P("Stages all project source code, tests, Dockerfile, and workflow files.", "Small")],
    [P('git commit -m "Initial commit..."', "Small"), P("Creates the initial root commit (SHA: c8e7241).", "Small")],
    [P("pytest test_app.py -v", "Small"), P("Executes 8 automated unit tests locally; all 8 passed in 0.40s.", "Small")],
    [P("git remote add origin <URL>", "Small"), P("Links the local repository to GitHub: github.com/kartikm95-2006/asdd-assignment-2.", "Small")],
    [P("git push -u origin main", "Small"), P("Pushes commits to GitHub, automatically triggering the GitHub Actions CI/CD workflow.", "Small")],
]
cmd_table = Table(commands, colWidths=[2.55 * inch, 3.9 * inch], repeatRows=1)
cmd_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#94a3b8")),
    ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#cbd5e1")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))

story.extend([
    cmd_table,
    Spacer(1, 8),
    evidence("pytest-test-evidence.png", "Figure 2: Terminal Test Execution & Git State Evidence", "Terminal log confirming 8 automated pytest tests passed in 0.40 seconds with clean Git working tree state on branch main."),
    PageBreak(),
])

# Section 5: Documentation and Evidence
story.extend([
    P("5. Documentation and Evidence", "Section"),
    P("The workflow execution was validated on GitHub Actions. The three distinct stages (Build, Test, Deploy) executed sequentially, each completing with green success status.", "Body"),
    evidence("github-actions-success.png", "Figure 3: GitHub Actions CI/CD Pipeline Execution Evidence", "GitHub Actions UI showing successful completion of Build, Test, and Deploy jobs, along with the detailed deployment summary and GHCR release metadata."),
    Spacer(1, 10),
    evidence("tasktrack-app.png", "Figure 4: TaskTrack DevOps Portal Web Interface Evidence", "Browser screenshot of the running Python application displaying real-time task tracking, stats counters, and active pipeline indicator."),
    PageBreak(),
    evidence("github-repository.png", "Figure 5: GitHub Repository Evidence (kartikm95-2006/asdd-assignment-2)", "Screenshot of the published GitHub repository showing all files, Dockerfile, GitHub Actions workflow, and successful run badge."),
    Spacer(1, 10),
    P("Submission Links & Summary:", "Subsection"),
    P("<b>GitHub Repository URL:</b> <font color='#2563eb'><u>https://github.com/kartikm95-2006/asdd-assignment-2</u></font>", "Body"),
    P("<b>Docker Image (GHCR):</b> <font color='#2563eb'><u>ghcr.io/kartikm95-2006/asdd-assignment-2:latest</u></font>", "Body"),
    P("<b>Commit SHA:</b> <code>c8e7241</code> | <b>Pipeline Status:</b> <font color='#16a34a'><b>Passing (All Stages Successful)</b></font>", "Body"),
    Spacer(1, 6),
    P("6. Conclusion", "Section"),
    P("A complete Continuous Integration and Continuous Deployment (CI/CD) pipeline for a Python project was successfully designed, containerized with Docker, and implemented using GitHub Actions. The automated pipeline achieved zero-touch execution across Build (compiling dependencies and packaging Docker image), Test (running automated unit tests and container healthchecks), and Deploy (publishing to GitHub Container Registry and verifying live container response).", "Body"),
])

doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=42, leftMargin=42, topMargin=42, bottomMargin=44, title="Assignment - 2 CI/CD Pipeline for Python", author="Kartik Mahindrakar")
doc.build(story, onFirstPage=cover, onLaterPages=footer)
print("Successfully generated:", OUT)
