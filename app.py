from flask import Flask, render_template, request
from cryptography.fernet import Fernet
import psycopg2

# Load encryption key
with open("secret.txt", "rb") as f:
    key = f.read()

fernet = Fernet(key)

# Decrypt password
with open("encrypted_pass.txt", "rb") as file:
    encrypted_password = file.read()

decrypted_password = fernet.decrypt(encrypted_password).decode()

app = Flask(__name__)

# Supabase config using decrypted password
db_config = {
    "user": "postgres.rhnbeekxsnpqcefyybsa",
    "password": decrypted_password,
    "host": "aws-0-ap-south-1.pooler.supabase.com",
    "port": "5432",
    "dbname": "postgres"
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    name = data.get("name")
    age = data.get("age")
    gender = data.get("gender")
    course = data.get("course")
    email = data.get("email")

    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO students (name, age, gender, course, email) VALUES (%s, %s, %s, %s, %s)",
            (name, age, gender, course, email)
        )
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Success"}, 200
    except Exception as e:
        print("Error:", e)
        return {"message": "Database error"}, 500

if __name__ == '__main__':
    app.run(debug=True)
