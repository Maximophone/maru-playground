from flask import Flask, render_template, request, jsonify, Response
import subprocess
import datetime as dt

app = Flask(__name__, template_folder="static")

MARU_DIR = "../../maru"
MARU_PATH = f"{MARU_DIR}/maru"
MARU_EXAMPLES_DIR = f"{MARU_DIR}/examples"
MARU_DEMO_PATH = f"{MARU_EXAMPLES_DIR}/intro_to_maru.mu"

LOGS_PATH = "../code.log"
LOG_LINE_LEN = 50

with open(MARU_DEMO_PATH) as f:
    DEFAULT_CODE = f.read()

def run_code(code: str) -> str:
    return subprocess.check_output([MARU_PATH, "--show-last", "-c", code])

def write_line(f):
    f.write("-"*LOG_LINE_LEN + "\n")

def log_code(code: str):
    with open(LOGS_PATH, 'a') as f:
        f.write("\n")
        write_line(f)
        f.write(str(dt.datetime.now()) + "\n")
        f.write("CODE: \n")
        write_line(f)
        f.write(code + "\n")
        write_line(f)

def log_output(output: str):
    with open(LOGS_PATH, 'a') as f:
        f.write("OUTPUT: \n")
        write_line(f)
        f.write(output +"\n")
        write_line(f)

@app.route('/')
def send_index():
    return render_template("index.html", input=DEFAULT_CODE)

@app.route("/", methods=["POST"])
def compute():
    code = request.form["code"].replace("\r", "")
    is_default = code == DEFAULT_CODE
    log_code("__DEFAULT_PROGRAM__" if is_default else code)
    try:
        output = run_code(code).decode()
    except UnicodeDecodeError:
        output = "Unicode Decode Error"
    log_output("__DEFAULT_OUTPUT__" if is_default else output)
    return render_template("index.html", input=code, output=output)

if __name__ == "__main__":
    app.run("0.0.0.0", 5000, False)

