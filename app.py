from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import sqlite3
from datetime import datetime, date
from openai import OpenAI

# Load .env file
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Groq client (OpenAI-style, different base_url)
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

app = Flask(__name__)

# Har din ka target (ml mein) — chaho toh change kar sakte ho
DAILY_GOAL = 3000


# ---------- Database setup ----------
def init_db():
    conn = sqlite3.connect("water.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS water_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount INTEGER NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# ---------- Route 1: Home page ----------
@app.route("/")
def index():
    return render_template("index.html")


# ---------- Route 2: Water add karo ----------
@app.route("/add_water", methods=["POST"])
def add_water():
    data = request.get_json()
    amount = data.get("amount", 0)

    conn = sqlite3.connect("water.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO water_logs (amount, timestamp) VALUES (?, ?)",
        (amount, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "added": amount})


# ---------- Route 3: Aaj ka total nikaalo ----------
@app.route("/get_logs")
def get_logs():
    today = date.today().isoformat()  # jaise "2026-09-03"

    conn = sqlite3.connect("water.db")
    cursor = conn.cursor()
    # sirf aaj ke logs ka sum nikaalo
    cursor.execute(
        "SELECT SUM(amount) FROM water_logs WHERE timestamp LIKE ?",
        (today + "%",)
    )
    result = cursor.fetchone()[0]
    conn.close()

    total = result if result else 0
    return jsonify({"total": total, "goal": DAILY_GOAL})


# ---------- Route 4: AI se hydration tip lo ----------
@app.route("/get_tip", methods=["POST"])
def get_tip():
    data = request.get_json()
    total = data.get("total", 0)

    prompt = f"I have drunk {total}ml of water today out of a {DAILY_GOAL}ml goal. Give me one short, friendly hydration tip in 1-2 sentences."

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    tip = response.choices[0].message.content
    return jsonify({"tip": tip})


# ---------- Server run karo ----------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)