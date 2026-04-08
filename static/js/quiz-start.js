const startButton = document.getElementById("start-button");
const startMessage = document.getElementById("start-message");

function resetQuizState(totalQuestions) {
  localStorage.setItem("quiz_score", "0");
  localStorage.setItem("quiz_total", String(totalQuestions));
}

async function startQuiz() {
  startMessage.textContent = "Starting...";
  const response = await fetch(apiUrl("/project4/sessions/1"));
  const payload = await response.json();
  if (!response.ok) {
    startMessage.textContent = payload.detail || "Could not start quiz.";
    return;
  }
  resetQuizState(payload.question_count || 15);
  window.location.href = "/quiz/1";
}

startButton.addEventListener("click", startQuiz);
