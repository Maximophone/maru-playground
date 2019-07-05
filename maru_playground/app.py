from flask import Flask, render_template, request, jsonify, Response
import subprocess

app = Flask(__name__, template_folder="static")

MARU_PATH = "./maru"

def run_code(code: str) -> str:
    return subprocess.check_output([MARU_PATH, "--show-last", "-c", code])

@app.route('/')
def send_index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def compute():
    code = request.form["code"]
    output = run_code(code).decode()
    print(output)
    return render_template("index.html", input=code, output=output)

if __name__ == "__main__":
    app.run("0.0.0.0", 5000, True)
