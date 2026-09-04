// ================================
// Water Tracker JS
// ================================

const progressFill = document.getElementById("progressFill");
const currentAmountEl = document.getElementById("currentAmount");
const goalAmountEl = document.getElementById("goalAmount");
const tipBtn = document.getElementById("tipBtn");
const tipText = document.getElementById("tipText");
const customAmount = document.getElementById("customAmount");
const customAddBtn = document.getElementById("customAddBtn");

// Store current total in a variable so we can reuse it (e.g. for AI tip)
let currentTotal = 0;
let dailyGoal = 3000;


// ---------- Fetch today's logs and update the progress bar ----------
function loadLogs() {
  fetch("/get_logs")
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      currentTotal = data.total;
      dailyGoal = data.goal;

      currentAmountEl.textContent = currentTotal;
      goalAmountEl.textContent = dailyGoal;

      // Calculate percentage, but cap it at 100%
      let percent = (currentTotal / dailyGoal) * 100;
      if (percent > 100) percent = 100;

      progressFill.style.width = percent + "%";
    });
}


// ---------- Add water amount to the backend ----------
function addWater(amount) {
  fetch("/add_water", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ amount: amount })
  })
  .then(function (response) {
    return response.json();
  })
  .then(function () {
    // After adding, refresh the progress bar
    loadLogs();
    loadTodayEntries();
  });
}

// ---------- Fetch today's individual entries and show as a list ----------
function loadTodayEntries() {
  fetch("/get_today_entries")
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      const entriesSection = document.getElementById("entriesSection");
      entriesSection.innerHTML = ""; // purani list saaf karo

      data.entries.forEach(function (entry) {
        const row = document.createElement("div");
        row.className = "entry-row";
        row.innerHTML = `<span>${entry.amount} ml</span><span>${entry.time}</span>`;
        entriesSection.appendChild(row);
      });
    });
} 

// ---------- Quick add buttons (250ml, 500ml, 1L) ----------
const quickButtons = document.querySelectorAll(".add-btn");
quickButtons.forEach(function (btn) {
  btn.addEventListener("click", function () {
    const amount = parseInt(btn.getAttribute("data-amount"));
    addWater(amount);
  });
});


// ---------- Custom amount button ----------
customAddBtn.addEventListener("click", function () {
  const amount = parseInt(customAmount.value);
  if (!amount || amount <= 0) {
    return; // ignore invalid input
  }
  addWater(amount);
  customAmount.value = "";
});


// ---------- AI Tip button ----------
tipBtn.addEventListener("click", function () {
  tipText.textContent = "Thinking...";

  fetch("/get_tip", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ total: currentTotal })
  })
  .then(function (response) {
    return response.json();
  })
  .then(function (data) {
    tipText.textContent = data.tip;
  });
});

// ---------- Fetch weekly data and draw the graph ----------
function loadWeeklyChart() {
  fetch("/get_weekly_data")
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      const ctx = document.getElementById("weeklyChart").getContext("2d");

      new Chart(ctx, {
        type: "bar",
        data: {
          labels: data.labels,
          datasets: [{
            label: "Water (ml)",
            data: data.totals,
            backgroundColor: "#2e8bc0",
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { display: false }
          },
          scales: {
            y: { beginAtZero: true }
          }
        }
      });
    });
}

// Draw the graph when page loads
loadWeeklyChart();


// ---------- Load logs when page first opens ----------
loadLogs();