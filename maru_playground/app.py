from flask import Flask, render_template, request, jsonify, Response
import subprocess
import datetime as dt
from typing import List
import multiprocessing

app = Flask(__name__, template_folder="static")

MARU_DIR = "../../maru"
MARU_PATH = f"{MARU_DIR}/maru"
MARU_EXAMPLES_DIR = f"{MARU_DIR}/examples"
MARU_DEMO_PATH = f"{MARU_EXAMPLES_DIR}/intro_to_maru.mu"

LOGS_PATH = "../code.log"
LOG_LINE_LEN = 50

TIMEOUT = 1

with open(MARU_DEMO_PATH) as f:
    DEFAULT_CODE = f.read()

manager = multiprocessing.Manager()

def apply_with_timeout(f, timeout, *args, **kwargs):
    return_dict = manager.dict()
    def wrapped(*args, **kwargs):
        try:
            return_dict["ret"] = f(*args, **kwargs)
        except Exception as e:
            return_dict["ret"] = e

    p = multiprocessing.Process(target=wrapped, args=args, kwargs=kwargs)
    p.start()
    p.join(timeout)
    if(p.is_alive()):
        p.terminate()
        raise TimeoutError
    if isinstance(return_dict.get("ret"), Exception):
        raise return_dict.get("ret")
    return return_dict.get("ret")

def run_cmd(cmd: List[str]) -> str:
    return subprocess.check_output(cmd)

def run_code(code: str) -> str:
    cmd = [MARU_PATH, "--show-last", "-c", code]
    return run_cmd(cmd).decode()

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
        output = apply_with_timeout(run_code, TIMEOUT, (code))
    except TimeoutError:
        output = f"Server Timeout Error: MARU program took longer than {TIMEOUT} second to run and was killed"
    except Exception as e:
        output = f"Server Exception when executing MARU program: \n\t{e}"
    log_output("__DEFAULT_OUTPUT__" if is_default else output)
    return render_template("index.html", input=code, output=output)

if __name__ == "__main__":
    app.run("0.0.0.0", 5000, False)

