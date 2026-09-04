from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import sqlite3
from datetime import datetime, date ,timedelta
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
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    tip = response.choices[0].message.content
    return jsonify({"tip": tip})

# ---------- Route: Pichle 7 dino ka data (graph ke liye) ----------
@app.route("/get_weekly_data")
def get_weekly_data():
    conn = sqlite3.connect("water.db")
    cursor = conn.cursor()

    labels = []
    totals = []

    # 6 din pehle se aaj tak, ek-ek din check karo
    for i in range(6, -1, -1):
        day = date.today() - timedelta(days=i)
        day_str = day.isoformat()

        cursor.execute(
            "SELECT SUM(amount) FROM water_logs WHERE timestamp LIKE ?",
            (day_str + "%",)
        )
        result = cursor.fetchone()[0]
        total = result if result else 0

        labels.append(day.strftime("%a"))  # jaise "Mon", "Tue"
        totals.append(total)

    conn.close()
    return jsonify({"labels": labels, "totals": totals})

# ---------- Route: Aaj ki har individual entry dikhao ----------
@app.route("/get_today_entries")
def get_today_entries():
    today = date.today().isoformat()

    conn = sqlite3.connect("water.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT amount, timestamp FROM water_logs WHERE timestamp LIKE ? ORDER BY timestamp DESC",
        (today + "%",)
    )
    rows = cursor.fetchall()
    conn.close()

    entries = []
    for amount, timestamp in rows:
        # timestamp jaisa "2026-09-04T15:48:09.123" hai, ismein se sirf time nikaalte hain
        time_part = timestamp.split("T")[1][:5]  # "15:48"
        entries.append({"amount": amount, "time": time_part})

    return jsonify({"entries": entries})

# ---------- Server run karo ----------
if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))