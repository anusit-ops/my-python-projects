from flask import Flask, jsonify, request, render_template
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
app.json.ensure_ascii = False
CORS(app)

def get_db_connection():
    # ตรวจสอบชื่อไฟล์ db ให้ตรงกับที่มี (hr_system.db)
    conn = sqlite3.connect('hr_system.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- 1. หน้าแรก (Home Page) ---
@app.route('/')
def home():
    return render_template('index.html')

# --- 2. API: ดูรายชื่อ (GET) ---
@app.route('/api/employees', methods=['GET'])
def get_employees():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employees')
        rows = cursor.fetchall()
        conn.close()
        return jsonify([dict(row) for row in rows])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 3. API: เพิ่มพนักงาน (POST) ---
@app.route('/api/add_employees', methods=['POST'])
def add_employees():
    try:
        data = request.json
        full_name = data.get("fullname")
        position = data.get("position")
        phone = data.get("phone")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO employees (fullname, position, phone) VALUES (?, ?, ?)', 
                       (full_name, position,phone))
        conn.commit()
        conn.close()
        return jsonify({"message": "บันทึกสำเร็จ", "name": full_name})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 4. API: ลบพนักงาน (DELETE) ---
@app.route('/api/delete_employee/<int:emp_id>', methods=['DELETE'])
def delete_employee(emp_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM employees WHERE id = ?', (emp_id,))
        
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"message": "ไม่พบรหัส"}), 404

        conn.commit()
        conn.close()
        return jsonify({"message": "ลบสำเร็จ"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 5. API: แก้ไขพนักงาน (PUT) ---
@app.route('/api/update_employee/<int:emp_id>', methods=['PUT'])
def update_employee(emp_id):
    try:
        data = request.json
        new_name = data.get("fullname")
        new_position = data.get("position")
        new_phone = data.get("phone")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE employees SET fullname = ?, position = ?, phone = ? WHERE id = ?', 
                       (new_name, new_position, new_phone, emp_id))

        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"message": "ไม่พบรหัส"}), 404

        conn.commit()
        conn.close()
        return jsonify({"message": "แก้ไขสำเร็จ"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)