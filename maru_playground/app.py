from flask import Flask, render_template, request, jsonify, Response
import subprocess

app = Flask(__name__, template_folder="static")

MARU_PATH = "../maru/maru"

DEFAULT_CODE = """# This is a MARU program.

# Use the printl built in function to print strings.
printl("Hello World!");

# You can also use print if you want to print strings on the same line.
print("Hello ");
print("World!");

# An empty printl goes to the next line
printl();

# You can use repr to represent maru objects that are not strings.
print("Printing a number: ");
repr(2);

# In MARU, the syntax to create variables is simple:
my_var = 1;
a_string_variable = "this is a string";
a_boolean = true;

# In MARU, everything is an expression, even declaring a variable! 
# So you can do things like this:
a = (b = 1);
repr(b);
repr(a);

"""

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
    app.run("0.0.0.0", 5000, True)
