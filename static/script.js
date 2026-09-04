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


// ---------- Load logs when page first opens ----------
loadLogs();