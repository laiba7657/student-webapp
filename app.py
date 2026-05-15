from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY, name TEXT, grade TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return "<h1>Student Portal</h1><p>Welcome!</p>"

@app.route('/students', methods=['GET'])
def get_students():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)

@app.route('/add', methods=['POST'])
def add_student():
    data = request.json
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("INSERT INTO students (name, grade) VALUES (?, ?)",
              (data['name'], data['grade']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Student added"}), 201

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)