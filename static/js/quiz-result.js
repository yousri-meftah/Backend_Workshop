const finalScore = document.getElementById("final-score");
const finalPercent = document.getElementById("final-percent");

function loadResult() {
  const score = Number(localStorage.getItem("quiz_score") || "0");
  const total = Number(localStorage.getItem("quiz_total") || "15");
  const percent = total > 0 ? Math.round((score / total) * 100) : 0;
  finalScore.textContent = `${score}/${total}`;
  finalPercent.textContent = `${percent}%`;
}

loadResult();
