from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("ncnw.db")
    conn.row_factory = sqlite3.Row
    return conn

# Test route
@app.route("/")
def home():
    return "NCNW API Running"

# Submit application
@app.route("/apply", methods=["POST"])
def apply():
    data = request.json

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO applications (
            application_date,
            first_name,
            last_name,
            email,
            phone,
            address,
            city,
            state,
            zip,
            member_status,
            membership_type_id,
            comments,
            application_status,
            submitted_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d"),
        data.get("first_name"),
        data.get("last_name"),
        data.get("email"),
        data.get("phone"),
        data.get("address"),
        data.get("city"),
        data.get("state"),
        data.get("zip"),
        data.get("member_status"),
        data.get("membership_type_id"),
        data.get("comments"),
        "Pending",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Application submitted successfully"})

if __name__ == "__main__":
    app.run(debug=True)