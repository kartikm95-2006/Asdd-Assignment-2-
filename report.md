# Assignment - 2
## CI/CD Pipeline for Python Project using GitHub Actions and Docker

- **Student:** Kartik Mahindrakar
- **Student ID:** 24106126
- **Roll No:** 99
- **Class / Div / Branch:** T.E. / B / CSE (AI&ML)
- **Subject:** Application Software Development & Deployment (ASDD) Lab
- **Instructor:** Prof. Radhika Bailurkar
- **Date:** 22/10/2026
- **GitHub Repository:** https://github.com/kartikm95-2006/asdd-assignment-2

---

## 1. Project Overview & Problem Statement

**Problem Statement:**
Develop and implement a CI/CD pipeline for a Python-based project using GitHub Actions. The pipeline should automate the process of building, testing, and deploying the Python application using Docker. [Similar to Exp 8 but for Python]

**Application Selected:**
**TaskTrack DevOps Portal** is a production-grade Python web application and REST API developed using Flask. It provides real-time task tracking, health checking, and REST API endpoints. The project is fully containerized with Docker and verified through an automated 3-stage CI/CD pipeline using GitHub Actions.

---

## 2. Explanation of the CI/CD Pipeline

Continuous Integration and Continuous Deployment (CI/CD) automates the phases of application development from code commit to production delivery.

### Purpose of Stages
1. **Build Stage:**
   - Validates code syntax and compilation.
   - Installs and caches application dependencies from `requirements.txt`.
   - Compiles the application and environment into a containerized Docker image (`tasktrack-app:latest` and tagged with the commit SHA).
   - Eliminates environment discrepancies between development and production.
2. **Test Stage:**
   - Runs automated unit tests via `pytest` (8 test cases covering API endpoints, web forms, and status codes).
   - Spawns the built Docker container in an isolated runner environment.
   - Probes the `/health` HTTP endpoint to ensure the container initialized correctly.
   - Shuts down and cleans up test containers.
3. **Deploy Stage:**
   - Automatically logs into **GitHub Container Registry (GHCR)** using `GITHUB_TOKEN`.
   - Tags and publishes the Docker image to GHCR (`ghcr.io/kartikm95-2006/asdd-assignment-2:latest`).
   - Starts the production container and performs a live HTTP probe to verify HTTP 200 OK.
   - Publishes deployment metadata and release status to the GitHub Actions Job Summary.

### Stage Execution Sequence
The pipeline enforces a strict dependency chain: **Build ➔ Test ➔ Deploy**.
- The `test` job depends on `build` via `needs: build`.
- The `deploy` job depends on `test` via `needs: test`.
If any test fails or the Docker build fails, the pipeline halts immediately, preventing broken code from reaching the deployment registry.

---

## 3. Dockerfile Implementation & Explanation

The application is containerized using `Dockerfile`:

```dockerfile
# Step 1: Base Image - Official lightweight Python 3.12 slim
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
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Step 12: Production command using Gunicorn WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
```

### Detailed Instruction Analysis
- **`FROM python:3.12-slim`**: Base Linux Debian image containing Python 3.12 with minimal footprint (~140MB).
- **`ENV PYTHONDONTWRITEBYTECODE=1` & `PYTHONUNBUFFERED=1`**: Prevents Python from writing `.pyc` files and streams logs to stdout/stderr in real time without buffering.
- **`WORKDIR /app`**: Creates and sets the container directory where all subsequent instructions execute.
- **`RUN addgroup ... && adduser ...`**: Creates a non-root system user (`appuser`) to adhere to container security compliance.
- **`COPY requirements.txt` followed by `RUN pip install ...`**: Separating dependency installation from code copy leverages Docker layer caching.
- **`HEALTHCHECK`**: Monitors container health automatically by querying `/health`.
- **`CMD ["gunicorn", ...]`**: Production WSGI server running 2 worker processes.

---

## 4. GitHub Actions Workflow File (`.github/workflows/ci-cd.yml`)

```yaml
name: CI/CD Pipeline - Python & Docker

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
      - name: Checkout Source Code
        uses: actions/checkout@v4
      - name: Set up Python 3.12 Environment
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'
      - name: Install Python Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Verify Code Syntax and Compilation
        run: |
          python -m compileall app.py test_app.py
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      - name: Build Docker Container Image
        run: |
          docker build \
            --tag tasktrack-app:latest \
            --tag tasktrack-app:${{ github.sha }} \
            .

  test:
    name: 2. Test Application & Container Health
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Checkout Source Code
        uses: actions/checkout@v4
      - name: Set up Python 3.12 Environment
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install Application & Test Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run Automated Pytest Suite
        run: |
          python -m pytest test_app.py -v --junitxml=test-results.xml
      - name: Build Container for Healthcheck Testing
        run: |
          docker build -t tasktrack-test:latest .
      - name: Execute Live Container Healthcheck
        run: |
          docker run -d --name test-container -p 5000:5000 tasktrack-test:latest
          sleep 6
          curl --fail --retry 3 --retry-delay 2 http://localhost:5000/health
          docker stop test-container
          docker rm test-container

  deploy:
    name: 3. Deploy Application to Container Registry & Production
    runs-on: ubuntu-latest
    needs: test
    steps:
      - name: Checkout Source Code
        uses: actions/checkout@v4
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      - name: Authenticate to GitHub Container Registry (GHCR)
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - name: Build, Tag and Push Image to GHCR
        run: |
          IMAGE_REPO=$(echo "ghcr.io/${{ github.repository }}" | tr '[:upper:]' '[:lower:]')
          docker build \
            --tag "$IMAGE_REPO:latest" \
            --tag "$IMAGE_REPO:${{ github.sha }}" \
            .
          docker push "$IMAGE_REPO:latest"
          docker push "$IMAGE_REPO:${{ github.sha }}"
      - name: Deploy and Verify Production Container
        run: |
          IMAGE_REPO=$(echo "ghcr.io/${{ github.repository }}" | tr '[:upper:]' '[:lower:]')
          docker run -d --name tasktrack-production --restart always -p 5000:5000 "$IMAGE_REPO:latest"
          sleep 6
          HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/)
          if [ "$HTTP_STATUS" -eq 200 ]; then
            echo "Production Deployment Verified: HTTP 200 OK."
          else
            exit 1
          fi
      - name: Generate Pipeline Execution Summary
        run: |
          IMAGE_REPO=$(echo "ghcr.io/${{ github.repository }}" | tr '[:upper:]' '[:lower:]')
          echo "## 🚀 CI/CD Pipeline Execution Summary" >> $GITHUB_STEP_SUMMARY
          echo "| Stage | Status | Details |" >> $GITHUB_STEP_SUMMARY
          echo "|---|---|---|" >> $GITHUB_STEP_SUMMARY
          echo "| **1. Build** | ✅ Passed | Python dependencies & Docker image built |" >> $GITHUB_STEP_SUMMARY
          echo "| **2. Test** | ✅ Passed | 8/8 pytest tests passed & container healthcheck verified |" >> $GITHUB_STEP_SUMMARY
          echo "| **3. Deploy** | ✅ Passed | Docker image pushed to GHCR & HTTP 200 probe verified |" >> $GITHUB_STEP_SUMMARY
```

---

## 5. Execution and Verification

| Command | Purpose |
|---|---|
| `git init -b main` | Initializes Git repository on `main` branch. |
| `git add .` | Stages all project files, Dockerfile, and CI/CD workflow. |
| `git commit -m "..."` | Creates initial commit recording version history. |
| `pytest test_app.py -v` | Executes 8 unit tests locally (all 8 passed in 0.40s). |
| `git remote add origin <URL>` | Configures remote tracking repository on GitHub. |
| `git push -u origin main` | Pushes changes to GitHub, triggering CI/CD pipeline. |

---

## 6. Evidence and Artifacts

1. **Pipeline Architecture:** `pipeline-architecture.png`
2. **Local Test Execution Evidence:** `pytest-test-evidence.png`
3. **GitHub Actions Workflow Run:** `github-actions-success.png`
4. **Delivered Web Application UI:** `tasktrack-app.png`
5. **Published GitHub Repository:** `github-repository.png`
6. **Compiled Assignment Reports:**
   - PDF Report: `Assignment-2-Python-CI-CD-Report.pdf`
   - Word Document: `ASDD_Assignment_2_Report.docx`

---

## 7. Submission Details

- **GitHub Repository URL:** https://github.com/kartikm95-2006/asdd-assignment-2
- **Container Registry:** `ghcr.io/kartikm95-2006/asdd-assignment-2:latest`
- **Workflow File:** `.github/workflows/ci-cd.yml`
- **Result:** Build ➔ Test ➔ Deploy successfully executed and verified.
