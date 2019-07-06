from flask import Flask, render_template, request, jsonify, Response
import subprocess

app = Flask(__name__, template_folder="static")

MARU_DIR = "../../maru"
MARU_PATH = f"{MARU_DIR}/maru"
MARU_EXAMPLES_DIR = f"{MARU_DIR}/examples"
MARU_DEMO_PATH = f"{MARU_EXAMPLES_DIR}/intro_to_maru.mu"

with open(MARU_DEMO_PATH) as f:
    DEFAULT_CODE = f.read()

def run_code(code: str) -> str:
    return subprocess.check_output([MARU_PATH, "--show-last", "-c", code])

@app.route('/')
def send_index():
    return render_template("index.html", input=DEFAULT_CODE)

@app.route("/", methods=["POST"])
def compute():
    print("COMPUTING")
    code = request.form["code"]
    output = run_code(code).decode()
    return render_template("index.html", input=code, output=output)

if __name__ == "__main__":
    app.run("0.0.0.0", 5000, False)

