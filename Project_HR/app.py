from flask import Flask, jsonify, request
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_db_connection():
    hr = "hr_system.db"
    conn = sqlite3.connect(hr)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/api/add_employees', methods =['POST'])
def add_employees():
    data = request.json
    full_name = data.get("fullname")
    position = data.get("position")

    conn = get_db_connection()
    cursor = conn.cursor()

    my_data = (full_name, position)
    my_sql ='INSERT INTO employees (fullname, position) VALUES (?, ?)'

    cursor.execute(my_sql, my_data)
    conn.commit()
    conn.close()

    return jsonify({"message": "บันทึกข้อมูลพนักงานเรียนร้อย", "name": full_name})

if __name__== "__main__":
    app.run(debug=True)