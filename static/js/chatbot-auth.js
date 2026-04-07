const authForm = document.getElementById("auth-form");
const authMessage = document.getElementById("auth-message");
const authSubmit = document.getElementById("auth-submit");
const showLoginButton = document.getElementById("show-login");
const showRegisterButton = document.getElementById("show-register");
const usernameInput = document.getElementById("auth-username");
const passwordInput = document.getElementById("auth-password");
const registerSuccessModal = document.getElementById("register-success-modal");
const closeSuccessModalButton = document.getElementById("close-success-modal");

let mode = "login";

function setMode(nextMode) {
  mode = nextMode;
  authSubmit.textContent = mode === "login" ? "Login" : "Register";
  showLoginButton.classList.toggle("active", mode === "login");
  showRegisterButton.classList.toggle("active", mode === "register");
  authMessage.textContent = "";
}

async function submitAuth(event) {
  event.preventDefault();

  const response = await fetch(apiUrl(mode === "login" ? "/project2/login" : "/project2/register"), {
    credentials: "include",
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: usernameInput.value.trim(),
      password: passwordInput.value.trim(),
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    authMessage.textContent = data.detail || "Request failed.";
    return;
  }

  if (mode === "register") {
    registerSuccessModal.classList.remove("hidden");
    setMode("login");
    passwordInput.value = "";
    return;
  }

  window.location.href = "/chatbot";
}

showLoginButton.addEventListener("click", () => setMode("login"));
showRegisterButton.addEventListener("click", () => setMode("register"));
authForm.addEventListener("submit", submitAuth);
closeSuccessModalButton.addEventListener("click", () => {
  registerSuccessModal.classList.add("hidden");
});

setMode("login");
