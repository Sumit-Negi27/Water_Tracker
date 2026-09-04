# 💧 Water Tracker AI

A simple, mobile-friendly water intake tracker built with **Flask**, **SQLite**, and **Groq AI** for personalized hydration tips — plus a 7-day progress graph to visualize your habits.

![status](https://img.shields.io/badge/status-working-brightgreen)
![python](https://img.shields.io/badge/python-3.x-blue)
![flask](https://img.shields.io/badge/flask-backend-black)
![sqlite](https://img.shields.io/badge/database-SQLite-lightgrey)

---

## ✨ Features

- 💧 Log water intake with quick-add buttons (250ml, 500ml, 1L) or a custom amount
- 📊 Live progress bar showing today's intake vs. daily goal
- 📅 A 7-day bar graph to track your weekly hydration trend
- 📝 See every entry you logged today, with timestamps
- ✨ Get a fun, emoji-filled AI hydration tip based on your progress (powered by Groq)
- 📱 Fully responsive — works on both desktop and mobile
- 🗄️ Data is stored permanently in a local SQLite database

---

## 🛠️ Tech Stack

| Layer      | Technology                  |
|------------|------------------------------|
| Frontend   | HTML, CSS, JavaScript, Chart.js |
| Backend    | Python (Flask)               |
| Database   | SQLite                       |
| AI Model   | Groq API (OpenAI-compatible) |
| Config     | python-dotenv                |

---

## 📂 Project Structure

```
Water_Tracker/
│
├── app.py                # Flask backend, routes, and database logic
├── water.db              # SQLite database (auto-created on first run)
├── .env                  # API key (not committed to GitHub)
├── static/
│   ├── style.css          # UI styling
│   └── script.js          # Frontend logic (fetch calls, chart, DOM updates)
├── templates/
│   └── index.html         # App UI markup
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/Water-Tracker.git
cd Water_Tracker
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install dependencies
```bash
pip install flask openai python-dotenv
```

### 4. Add your API key
Create a `.env` file in the root folder:
```
GROQ_API_KEY=your_api_key_here
```

### 5. Run the app
```bash
python app.py
```

Then open your browser at:
```
http://127.0.0.1:5000/
```

---

## 🧠 How It Works

1. The frontend sends a `fetch()` request to Flask whenever water is added or data needs refreshing.
2. Flask inserts or reads rows from the `water_logs` table in SQLite.
3. Every action (adding water, loading today's total, loading the weekly graph) has its own Flask route.
4. When you tap "Get AI Hydration Tip," Flask sends your current progress to the Groq API, which returns a short, personalized tip.

---

## 🔮 Future Improvements

- [ ] Customizable daily goal
- [ ] Delete individual entries
- [ ] Reminders / notifications to drink water
- [ ] User accounts for multiple people

---

## 📄 License

This project is open source and free to use for learning purposes.