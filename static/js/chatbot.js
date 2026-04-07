const conversationList = document.getElementById("conversation-list");
const chatMessages = document.getElementById("chat-messages");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const newConversationButton = document.getElementById("new-conversation");
const conversationModal = document.getElementById("conversation-modal");
const closeModalButton = document.getElementById("close-modal");
const conversationForm = document.getElementById("conversation-form");
const conversationTitleInput = document.getElementById("conversation-title");
const authModal = document.getElementById("auth-modal");
const logoutButton = document.getElementById("logout-button");
const sendButton = chatForm.querySelector("button[type='submit']");

let activeConversationId = null;

async function readJson(response) {
  const text = await response.text();
  return text ? JSON.parse(text) : {};
}

function showAuthModal() {
  authModal.classList.remove("hidden");
}

async function stopIfUnauthorized(response) {
  if (response.status === 401) {
    showAuthModal();
    return true;
  }
  return false;
}

async function loadConversations() {
  const response = await fetch(apiUrl("/project2/conversations"), {
    credentials: "include",
  });
  if (await stopIfUnauthorized(response)) {
    return;
  }
  const conversations = await readJson(response);
  conversationList.innerHTML = "";

  conversations.forEach((conversation) => {
    const card = document.createElement("button");
    card.className = "conversation-card";
    card.dataset.id = conversation.id;
    card.innerHTML = `
      <strong>${conversation.title}</strong>
      <div class="conversation-meta">${conversation.summary || "No summary yet."}</div>
      <div class="conversation-meta">${conversation.message_count} messages</div>
    `;
    conversationList.appendChild(card);
  });

  if (!activeConversationId && conversations.length) {
    activeConversationId = conversations[0].id;
  }

  if (activeConversationId) {
    loadConversation(activeConversationId);
  }
}

async function loadConversation(id) {
  activeConversationId = id;
  const response = await fetch(apiUrl(`/project2/conversations/${id}`), {
    credentials: "include",
  });
  if (await stopIfUnauthorized(response)) {
    return;
  }
  const conversation = await readJson(response);
  renderMessages(conversation.messages);
}

function renderMessages(messages) {
  chatMessages.innerHTML = "";

  if (!messages.length) {
    chatMessages.innerHTML = '<div class="bubble assistant">Start the conversation.</div>';
    return;
  }

  messages.forEach((message) => {
    const bubble = document.createElement("div");
    bubble.className = `bubble ${message.role}`;
    bubble.textContent = message.content;
    chatMessages.appendChild(bubble);
  });

  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function appendBubble(role, text, extraClass = "") {
  const bubble = document.createElement("div");
  bubble.className = `bubble ${role} ${extraClass}`.trim();
  bubble.textContent = text;
  chatMessages.appendChild(bubble);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  return bubble;
}

function setSendingState(isSending) {
  chatInput.disabled = isSending;
  sendButton.disabled = isSending;
  sendButton.textContent = isSending ? "Waiting..." : "Send";
  if (!isSending) {
    chatInput.focus();
  }
}

function openConversationModal() {
  conversationModal.classList.remove("hidden");
  conversationTitleInput.focus();
}

function closeConversationModal() {
  conversationModal.classList.add("hidden");
  conversationForm.reset();
}

async function createConversation(event) {
  event.preventDefault();
  const title = conversationTitleInput.value.trim();

  const response = await fetch(apiUrl("/project2/conversations"), {
    credentials: "include",
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ title: title || "New conversation" }),
  });
  if (await stopIfUnauthorized(response)) {
    return;
  }
  const conversation = await readJson(response);
  activeConversationId = conversation.id;
  closeConversationModal();
  await loadConversations();
}

async function sendMessage(event) {
  event.preventDefault();
  const message = chatInput.value.trim();
  if (!message || !activeConversationId) {
    return;
  }

  chatInput.value = "";
  appendBubble("user", message);
  const loadingBubble = appendBubble("assistant", "Gemini is thinking...");
  setSendingState(true);

  const response = await fetch(apiUrl(`/project2/conversations/${activeConversationId}/messages`), {
    credentials: "include",
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message, lang: "English" }),
  });
  if (await stopIfUnauthorized(response)) {
    loadingBubble.remove();
    setSendingState(false);
    return;
  }

  loadingBubble.remove();
  setSendingState(false);
  await loadConversation(activeConversationId);
  await loadConversations();
}

async function logout() {
  await fetch(apiUrl("/project2/logout"), {
    credentials: "include",
    method: "POST",
  });
  window.location.href = "/chatbot-auth";
}

conversationList.addEventListener("click", (event) => {
  const card = event.target.closest("[data-id]");
  if (!card) {
    return;
  }
  loadConversation(card.dataset.id);
});

chatForm.addEventListener("submit", sendMessage);
newConversationButton.addEventListener("click", openConversationModal);
closeModalButton.addEventListener("click", closeConversationModal);
conversationForm.addEventListener("submit", createConversation);
conversationModal.addEventListener("click", (event) => {
  if (event.target === conversationModal) {
    closeConversationModal();
  }
});
logoutButton.addEventListener("click", logout);

loadConversations();
