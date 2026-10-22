import pytest
from app import app, tasks

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test health check endpoint used by Docker and CI/CD pipeline"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert "service" in data
    assert "version" in data

def test_index_route(client):
    """Test the main HTML UI loads successfully"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"TaskTrack DevOps Portal" in response.data
    assert b"CI/CD Pipeline: Active" in response.data

def test_get_tasks_api(client):
    """Test retrieving tasks via JSON REST API"""
    response = client.get("/api/tasks")
    assert response.status_code == 200
    data = response.get_json()
    assert "tasks" in data
    assert isinstance(data["tasks"], list)
    assert data["count"] == len(data["tasks"])

def test_create_task_api_success(client):
    """Test creating a new task via REST API"""
    payload = {
        "title": "Verify GitHub Actions Deployment Stage",
        "description": "Ensure Docker deployment triggers properly",
        "priority": "High"
    }
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Task created successfully"
    assert data["task"]["title"] == payload["title"]
    assert data["task"]["priority"] == "High"
    assert data["task"]["status"] == "Pending"

def test_create_task_api_missing_title(client):
    """Test validation when title is missing in payload"""
    response = client.post("/api/tasks", json={"description": "No title provided"})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_delete_task_api_success(client):
    """Test deleting an existing task via REST API"""
    # Create task first
    res = client.post("/api/tasks", json={"title": "Temporary Task To Delete"})
    task_id = res.get_json()["task"]["id"]

    # Delete task
    del_res = client.delete(f"/api/tasks/{task_id}")
    assert del_res.status_code == 200
    assert "deleted successfully" in del_res.get_json()["message"]

def test_delete_task_api_not_found(client):
    """Test deleting a non-existent task returns 404"""
    response = client.delete("/api/tasks/999999")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data

def test_web_form_create_and_toggle(client):
    """Test creating task via web form and toggling completion"""
    # Create via form
    res = client.post("/tasks/create", data={
        "title": "Web Form Task",
        "priority": "Low",
        "description": "Created from HTML form"
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b"Web Form Task" in res.data

    # Toggle the last task
    last_id = tasks[-1]["id"]
    toggle_res = client.post(f"/tasks/{last_id}/toggle", follow_redirects=True)
    assert toggle_res.status_code == 200
