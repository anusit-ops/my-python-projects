from flask import Flask, jsonify, request
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
app.json.ensure_ascii = False
CORS(app)

def get_db_connection():
    hr = "hr_system.db"
    conn = sqlite3.connect(hr)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/api/employees', methods = ['GET'])
def employees():
   

    conn = get_db_connection()
    cursor = conn.cursor()

 
    my_sql ='SELECT * FROM employees'
    cursor.execute(my_sql)

    rows = cursor.fetchall()

    results_list = [dict(row) for row in rows]
    conn.close()

    return jsonify(results_list)   



@app.route('/api/delete_employee/<int:emp_id>', methods = ['DELETE'])
def delete_employee(emp_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        my_sql = 'DELETE FROM employees WHERE id = ?'
        
        cursor.execute(my_sql, (emp_id,))

        if cursor.rowcount == 0:
            conn.close()  
            return jsonify({"message": f"ไม่พบรหัส {emp_id}"}), 404 

        conn.commit()
        conn.close()

        return jsonify({"message": f"ลบพนักงานรหัส {emp_id} เรียบร้อยแล้ว"})

    except Exception as e:
        return jsonify({"error" : str(e)}),500



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

    return jsonify({"message": "บันทึกข้อมูลพนักงานเรียบร้อย", "name": full_name})

if __name__== "__main__":
    app.run(debug=True)

