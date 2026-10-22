# ==========================================
# Multi-Stage / Optimized Python Dockerfile
# Project: TaskTrack CI/CD DevOps Portal
# ==========================================

# Step 1: Base Image - Official lightweight Python 3.12 slim
FROM python:3.12-slim

# Step 2: Set Environment Variables
# Prevents Python from writing .pyc files to container
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout/stderr (real-time logging)
ENV PYTHONUNBUFFERED=1
# Default application port
ENV PORT=5000

# Step 3: Set Working Directory inside container
WORKDIR /app

# Step 4: Security - Create a dedicated non-root user and group
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Step 5: Leverage Docker Layer Caching for Dependencies
# Copy requirements file first so docker caches pip layer unless requirements change
COPY requirements.txt /app/

# Step 6: Install dependencies without caching pip packages to keep image small
RUN pip install --no-cache-dir -r requirements.txt

# Step 7: Copy application source code into the image
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
