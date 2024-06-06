from flask import Flask, render_template, request
from flask import redirect, url_for
import pickle
from beautifultable import BeautifulTable

app = Flask(__name__)

# Function to save the checklist
def save_checklist(checklist):
    with open("checklist.pkl", "wb") as f:
        pickle.dump(checklist, f)

# Function to load the checklist
def load_checklist():
    try:
        with open("checklist.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []
    except (pickle.PickleError, IOError, EOFError):
        print("Error loading checklist or empty checklist file.")
        return []

# Function to view the checklist
def view_checklist():
    checklist = load_checklist()
    table = BeautifulTable()
    table.headers = ["Index", "Task"]

    if checklist:
        for index, item in enumerate(checklist, 0):
            table.rows.append([index, item])
    else:
        table.rows.append(["Hooray! You are free from work.", ""])
    return str(table)

# Function to add to the checklist
def add_to_checklist(task):
    checklist = load_checklist()
    checklist.append(task)
    save_checklist(checklist)

# Function for checking off a task
def check_off_task(index):
    checklist = load_checklist()
    if 0 <= index < len(checklist):
        task = checklist.pop(index)
        save_checklist(checklist)
        return f"Checked off task: {task}"
    else:
        return "Invalid index."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/view", methods=["GET"])
def view():
    checklist = view_checklist()
    return render_template("view.html", checklist=checklist)

@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")
    add_to_checklist(task)
    return redirect(url_for("index"))

@app.route("/check", methods=["POST"])
def check():
    index_str = request.form.get("index")
    if index_str.strip():  # Check if index_str is not empty after stripping whitespace
        try:
            index = int(index_str)
            result = check_off_task(index)
            return result
        except ValueError:
            return "Invalid input. Please enter a valid index as a number."
    else:
        return "Index is empty. Please enter a valid index."


if __name__ == "__main__":
    app.run(debug=True)
