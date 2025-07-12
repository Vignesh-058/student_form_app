from flask import Flask, render_template, request
from cryptography.fernet import Fernet
import mysql.connector
import json

app = Flask(__name__)

# Load encryption key
with open("secret.txt", "rb") as f:
    key = f.read()

f = Fernet(key)

# Decrypt password
with open("encrypted_pass.txt", "rb") as file:
    encrypted_password = file.read()

decrypted_password = f.decrypt(encrypted_password).decode()

# MySQL config
db_config = {
    "host": "localhost",
    "user": "root",
    "password": decrypted_password,
    "database": "studentdb"
}

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    name = data.get("name")
    age = data.get("age")
    gender = data.get("gender")
    course = data.get("course")
    email = data.get("email")

    try:
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        query = "INSERT INTO students (name, age, gender, course, email) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(query, (name, age, gender, course, email))
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Success"}, 200
    except Exception as e:
        print("Error:", e)
        return {"message": "Error saving data"}, 500

if __name__ == '__main__':
    app.run(debug=True)
