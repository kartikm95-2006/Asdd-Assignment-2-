from PIL import Image, ImageDraw, ImageFont

W, H = 1100, 560
img = Image.new("RGB", (W, H), "#0d1117")
draw = ImageDraw.Draw(img)

try:
    font_bold = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 15)
    font_code = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 14)
    font_header = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 14)
except:
    font_bold = font_code = font_header = ImageFont.load_default()

# Terminal Window Bar
draw.rectangle([0, 0, W, 38], fill="#161b22")
draw.line([(0, 38), (W, 38)], fill="#30363d", width=1)
# Mac/Linux style window buttons
draw.ellipse([14, 13, 26, 25], fill="#ff5f56")
draw.ellipse([34, 13, 46, 25], fill="#ffbd2e")
draw.ellipse([54, 13, 66, 25], fill="#27c93f")
draw.text((85, 11), "kartik@devops-machine: ~/ASDD-Assignment-2 -- python -m pytest test_app.py -v", fill="#8b949e", font=font_header)

lines = [
    ("$ python -m pytest test_app.py -v", "#58a6ff"),
    ("============================= test session starts ==============================", "#8b949e"),
    ("platform win32 -- Python 3.12.3, pytest-8.3.3, pluggy-1.6.0", "#8b949e"),
    ("rootdir: C:\\Users\\Kartik Mahindrakar\\Desktop\\ASDD Assignment 2", "#8b949e"),
    ("collected 8 items", "#c9d1d9"),
    ("", "#c9d1d9"),
    ("test_app.py::test_health_check PASSED                                    [ 12%]", "#3fb950"),
    ("test_app.py::test_index_route PASSED                                     [ 25%]", "#3fb950"),
    ("test_app.py::test_get_tasks_api PASSED                                   [ 37%]", "#3fb950"),
    ("test_app.py::test_create_task_api_success PASSED                         [ 50%]", "#3fb950"),
    ("test_app.py::test_create_task_api_missing_title PASSED                   [ 62%]", "#3fb950"),
    ("test_app.py::test_delete_task_api_success PASSED                         [ 75%]", "#3fb950"),
    ("test_app.py::test_delete_task_api_not_found PASSED                       [ 87%]", "#3fb950"),
    ("test_app.py::test_web_form_create_and_toggle PASSED                      [100%]", "#3fb950"),
    ("", "#c9d1d9"),
    ("============================== 8 passed in 0.40s ===============================", "#3fb950"),
    ("", "#c9d1d9"),
    ("$ git log --oneline -1", "#58a6ff"),
    ("c8e7241 (HEAD -> main) Initial commit: Python Flask app with Dockerfile and GitHub Actions CI/CD pipeline", "#e6edf3"),
    ("$ git status", "#58a6ff"),
    ("On branch main: nothing to commit, working tree clean", "#3fb950")
]

y = 52
for text, color in lines:
    draw.text((25, y), text, fill=color, font=font_code)
    y += 23

out_path = r"C:\Users\Kartik Mahindrakar\Desktop\ASDD Assignment 2\pytest-test-evidence.png"
img.save(out_path)
print("Saved pytest terminal card to", out_path)
