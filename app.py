from flask import Flask, jsonify, request, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    phone = "phonebook.db"
    conn = sqlite3.connect(phone)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/add_contact', methods =['POST'])
def add_contact():
    data = request.json
    new_name = data.get("name")
    new_phone = data.get("phone")

    conn = get_db_connection()
    cursor = conn.cursor()

    my_data = (new_name, new_phone)
    my_sql ='INSERT INTO contacts (name, phone) VALUES (?, ?)'

    cursor.execute(my_sql, my_data)
    conn.commit()
    conn.close()

    return jsonify({"message": "บันทึกเบอร์เรียบร้อย", "name": new_name})



@app.route('/api/contact/<name>')
def get_contact(name):
    conn = get_db_connection()
    cursor = conn.cursor()

    target_name = name
    search_sql = 'SELECT * FROM contacts WHERE name = ?'
    search_data = (target_name,)


    cursor.execute(search_sql, search_data)

    contact = cursor.fetchone()
    conn.close()

    if contact:
        return jsonify({
            "name": contact["name"],
            "phone": contact["phone"] 
        })
    
    else:
        return jsonify({"error": "ไม่พบรายชื่อนี้"}), 404
if __name__== "__main__":
    app.run(debug=True)