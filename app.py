from flask import Flask, render_template_string, request, jsonify, redirect, url_for
from datetime import datetime, timezone

app = Flask(__name__)

# In-memory storage for demonstration (resets on container restart or persists during runtime)
tasks = [
    {
        "id": 1,
        "title": "Configure GitHub Actions CI/CD Pipeline",
        "description": "Set up Build, Test, and Deploy jobs in ci-cd.yml",
        "status": "Completed",
        "priority": "High",
        "created_at": "2026-10-22 10:00:00"
    },
    {
        "id": 2,
        "title": "Write Dockerfile for Python Flask App",
        "description": "Containerize the application with Python 3.12-slim base image",
        "status": "Completed",
        "priority": "High",
        "created_at": "2026-10-22 10:30:00"
    },
    {
        "id": 3,
        "title": "Implement Unit & Integration Tests",
        "description": "Create pytest test suite covering all REST endpoints and routes",
        "status": "Completed",
        "priority": "Medium",
        "created_at": "2026-10-22 11:00:00"
    },
    {
        "id": 4,
        "title": "Deploy Container Image to GitHub Container Registry",
        "description": "Automate pushing Docker images to GHCR on pipeline success",
        "status": "Pending",
        "priority": "High",
        "created_at": "2026-10-22 11:30:00"
    }
]

next_id = 5

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TaskTrack CI/CD - DevOps Portal</title>
    <style>
        :root {
            --primary: #2563eb;
            --primary-dark: #1d4ed8;
            --bg: #0f172a;
            --card-bg: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --border: #334155;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            line-height: 1.6;
            padding: 2rem 1rem;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        header {
            margin-bottom: 2rem;
            border-bottom: 1px solid var(--border);
            padding-bottom: 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }
        .badge-pipeline {
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
            padding: 0.35rem 0.8rem;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }
        .pulse-dot {
            width: 8px;
            height: 8px;
            background: #fff;
            border-radius: 50%;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.4; transform: scale(0.85); }
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }
        .stat-card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 1.25rem;
        }
        .stat-val {
            font-size: 1.75rem;
            font-weight: 700;
            color: #38bdf8;
        }
        .stat-label {
            font-size: 0.875rem;
            color: var(--text-muted);
        }
        .card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 2rem;
        }
        h2 { font-size: 1.25rem; margin-bottom: 1rem; color: #e2e8f0; }
        .form-row {
            display: grid;
            grid-template-columns: 2fr 1fr 1fr auto;
            gap: 0.75rem;
            align-items: end;
        }
        @media (max-width: 680px) {
            .form-row { grid-template-columns: 1fr; }
        }
        input, select, button {
            padding: 0.65rem 0.85rem;
            border-radius: 6px;
            border: 1px solid var(--border);
            background: #0f172a;
            color: white;
            font-size: 0.95rem;
        }
        input:focus, select:focus {
            outline: 2px solid var(--primary);
        }
        button.btn-primary {
            background: var(--primary);
            border: none;
            cursor: pointer;
            font-weight: 600;
            transition: background 0.2s;
        }
        button.btn-primary:hover { background: var(--primary-dark); }
        .task-list {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }
        .task-item {
            background: #0f172a;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
        }
        .task-info h3 {
            font-size: 1rem;
            margin-bottom: 0.2rem;
        }
        .task-info p {
            font-size: 0.85rem;
            color: var(--text-muted);
        }
        .task-meta {
            display: flex;
            gap: 0.5rem;
            align-items: center;
        }
        .tag {
            font-size: 0.75rem;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-weight: 600;
        }
        .tag-High { background: rgba(239, 68, 68, 0.2); color: #fca5a5; }
        .tag-Medium { background: rgba(245, 158, 11, 0.2); color: #fde68a; }
        .tag-Low { background: rgba(16, 185, 129, 0.2); color: #6ee7b7; }
        .tag-Completed { background: rgba(16, 185, 129, 0.2); color: #34d399; }
        .tag-Pending { background: rgba(59, 130, 246, 0.2); color: #93c5fd; }
        .actions {
            display: flex;
            gap: 0.5rem;
        }
        .btn-action {
            background: transparent;
            border: 1px solid var(--border);
            padding: 0.35rem 0.65rem;
            font-size: 0.8rem;
            cursor: pointer;
            border-radius: 4px;
        }
        .btn-action:hover { background: #334155; }
        .btn-danger { color: #f87171; border-color: rgba(239, 68, 68, 0.4); }
        .btn-danger:hover { background: rgba(239, 68, 68, 0.2); }
        footer {
            text-align: center;
            margin-top: 3rem;
            font-size: 0.85rem;
            color: var(--text-muted);
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div>
                <h1>TaskTrack DevOps Portal</h1>
                <p style="color: var(--text-muted); font-size: 0.9rem;">Automated CI/CD Pipeline with GitHub Actions & Docker</p>
            </div>
            <div class="badge-pipeline">
                <div class="pulse-dot"></div>
                <span>CI/CD Pipeline: Active</span>
            </div>
        </header>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-val">{{ tasks|length }}</div>
                <div class="stat-label">Total Pipeline Tasks</div>
            </div>
            <div class="stat-card">
                <div class="stat-val">{{ tasks|selectattr('status', 'equalto', 'Completed')|list|length }}</div>
                <div class="stat-label">Completed Tasks</div>
            </div>
            <div class="stat-card">
                <div class="stat-val">{{ tasks|selectattr('status', 'equalto', 'Pending')|list|length }}</div>
                <div class="stat-label">Pending Deployment</div>
            </div>
        </div>

        <div class="card">
            <h2>Add New Deployment Task</h2>
            <form method="POST" action="/tasks/create">
                <div class="form-row">
                    <div>
                        <input type="text" name="title" placeholder="Task title / feature" required style="width: 100%;">
                    </div>
                    <div>
                        <select name="priority" style="width: 100%;">
                            <option value="High">High Priority</option>
                            <option value="Medium" selected>Medium Priority</option>
                            <option value="Low">Low Priority</option>
                        </select>
                    </div>
                    <div>
                        <input type="text" name="description" placeholder="Short description" style="width: 100%;">
                    </div>
                    <div>
                        <button type="submit" class="btn-primary">+ Add Task</button>
                    </div>
                </div>
            </form>
        </div>

        <div class="card">
            <h2>Pipeline Work Items</h2>
            <ul class="task-list">
                {% for t in tasks %}
                <li class="task-item">
                    <div class="task-info">
                        <h3>{{ t.title }}</h3>
                        <p>{{ t.description }}</p>
                        <div class="task-meta" style="margin-top: 0.4rem;">
                            <span class="tag tag-{{ t.priority }}">{{ t.priority }}</span>
                            <span class="tag tag-{{ t.status }}">{{ t.status }}</span>
                            <span style="font-size: 0.75rem; color: var(--text-muted);">{{ t.created_at }}</span>
                        </div>
                    </div>
                    <div class="actions">
                        {% if t.status != 'Completed' %}
                        <form method="POST" action="/tasks/{{ t.id }}/toggle" style="display:inline;">
                            <button type="submit" class="btn-action">Complete</button>
                        </form>
                        {% endif %}
                        <form method="POST" action="/tasks/{{ t.id }}/delete" style="display:inline;">
                            <button type="submit" class="btn-action btn-danger">Delete</button>
                        </form>
                    </div>
                </li>
                {% endfor %}
            </ul>
        </div>

        <footer>
            <p>ASDD Assignment 2 &bull; APSIT CSE (AI&ML) &bull; Student: Kartik Mahindrakar (Roll No: 99)</p>
            <p>Automated with GitHub Actions | Dockerized on Python 3.12-slim</p>
        </footer>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, tasks=tasks)

@app.route("/health", methods=["GET"])
def health():
    """Healthcheck endpoint for Docker container and pipeline validation"""
    return jsonify({
        "status": "healthy",
        "service": "tasktrack-devops-portal",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200

# REST API Endpoints
@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify({"count": len(tasks), "tasks": tasks}), 200

@app.route("/api/tasks", methods=["POST"])
def create_task_api():
    global next_id
    data = request.get_json() or {}
    title = data.get("title")
    if not title:
        return jsonify({"error": "Title is required"}), 400
    new_task = {
        "id": next_id,
        "title": title,
        "description": data.get("description", ""),
        "status": data.get("status", "Pending"),
        "priority": data.get("priority", "Medium"),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    next_id += 1
    tasks.append(new_task)
    return jsonify({"message": "Task created successfully", "task": new_task}), 201

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task_api(task_id):
    global tasks
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": f"Task {task_id} deleted successfully"}), 200

# Web Form Handlers
@app.route("/tasks/create", methods=["POST"])
def create_task_form():
    global next_id
    title = request.form.get("title")
    if title:
        new_task = {
            "id": next_id,
            "title": title,
            "description": request.form.get("description", ""),
            "status": "Pending",
            "priority": request.form.get("priority", "Medium"),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        next_id += 1
        tasks.append(new_task)
    return redirect(url_for("index"))

@app.route("/tasks/<int:task_id>/toggle", methods=["POST"])
def toggle_task(task_id):
    for t in tasks:
        if t["id"] == task_id:
            t["status"] = "Completed" if t["status"] != "Completed" else "Pending"
            break
    return redirect(url_for("index"))

@app.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task_form(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
