const quizProgress = document.getElementById("quiz-progress");
const quizCard = document.getElementById("quiz-card");
const nextButton = document.getElementById("next-button");
const quizFeedback = document.getElementById("quiz-feedback");

let currentQuestion = null;
let currentId = 1;
let answered = false;
let totalQuestions = Number(localStorage.getItem("quiz_total") || "15");

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function getScore() {
  return Number(localStorage.getItem("quiz_score") || "0");
}

function setScore(score) {
  localStorage.setItem("quiz_score", String(score));
}

function parseQuestionId() {
  const parts = window.location.pathname.split("/").filter(Boolean);
  const last = parts[parts.length - 1];
  const value = Number(last);
  return Number.isInteger(value) && value > 0 ? value : 1;
}

function renderQuestion(question) {
  quizProgress.textContent = `Question ${question.position} of ${totalQuestions}`;
  nextButton.textContent = question.position >= totalQuestions ? "Finish" : "Next";
  nextButton.disabled = true;
  quizFeedback.textContent = "";
  answered = false;
  quizCard.innerHTML = `
    <div class="quiz-question-head">
      <span class="card-tag">Question ${question.position}</span>
      <strong>${escapeHtml(question.question)}</strong>
    </div>
    <div class="quiz-options">
      ${question.options
        .map(
          (option) => `
            <label class="quiz-option">
              <input type="radio" name="answer" value="${option.key}">
              <span><strong>${option.key}.</strong> ${escapeHtml(option.text)}</span>
            </label>
          `
        )
        .join("")}
    </div>
  `;
}

function lockOptions() {
  quizCard.querySelectorAll('input[name="answer"]').forEach((input) => {
    input.disabled = true;
  });
}

async function handleAnswerChange(event) {
  if (answered) {
    return;
  }
  const target = event.target;
  if (!target || target.name !== "answer") {
    return;
  }
  answered = true;
  const response = await fetch(apiUrl(`/project4/sessions/1/quiz/${currentId}/check`), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ selected_option: target.value }),
  });
  const payload = await response.json();
  if (!response.ok) {
    quizFeedback.textContent = payload.detail || "Could not check answer.";
    nextButton.disabled = false;
    lockOptions();
    return;
  }

  if (payload.correct) {
    const nextScore = getScore() + 1;
    setScore(nextScore);
    quizFeedback.textContent = "Correct.";
  } else {
    quizFeedback.textContent = "Wrong.";
  }
  nextButton.disabled = false;
  lockOptions();
}

function goNext() {
  if (!answered) {
    return;
  }
  if (currentId >= totalQuestions) {
    window.location.href = "/quiz/result";
    return;
  }
  window.location.href = `/quiz/${currentId + 1}`;
}

async function loadQuestion() {
  currentId = parseQuestionId();
  if (currentId > totalQuestions) {
    window.location.href = "/quiz/result";
    return;
  }
  const response = await fetch(apiUrl(`/project4/sessions/1/quiz/${currentId}`));
  const payload = await response.json();
  if (!response.ok) {
    quizProgress.textContent = "Could not load question.";
    quizCard.innerHTML = "";
    quizFeedback.textContent = payload.detail || "Error";
    nextButton.hidden = true;
    return;
  }
  currentQuestion = payload;
  renderQuestion(payload);
}

quizCard.addEventListener("change", handleAnswerChange);
nextButton.addEventListener("click", goNext);
loadQuestion();
