from flask import Flask, request, jsonify, render_template
import psycopg2
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "tasks_db"),
        user=os.getenv("POSTGRES_USER", "user"),
        password=os.getenv("POSTGRES_PASSWORD", "password"),
        host=os.getenv("POSTGRES_HOST", "db"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY, 
            name TEXT,
            completed BOOLEAN DEFAULT FALSE
        )
    ''')
    conn.commit()
    c.close()
    conn.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = [{"id": row[0], "name": row[1], "completed": row[2]} for row in c.fetchall()]
    c.close()
    conn.close()
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    name = data.get("name")
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO tasks (name) VALUES (%s) RETURNING id", (name,))
    task_id = c.fetchone()[0]
    conn.commit()
    c.close()
    conn.close()
    return jsonify({"message": "Task added", "id": task_id}), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("UPDATE tasks SET completed = NOT completed WHERE id = %s RETURNING completed", (task_id,))
    updated_status = c.fetchone()
    conn.commit()
    c.close()
    conn.close()
    return jsonify({"message": "Task updated", "completed": updated_status[0]})

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db_connection()
    c = conn.cursor()    
    c.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    c.close()
    conn.close()
    return jsonify({"message": "Task deleted"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
