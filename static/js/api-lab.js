const snippetForm = document.getElementById("snippet-form");
const snippetTitle = document.getElementById("snippet-title");
const snippetTag = document.getElementById("snippet-tag");
const snippetContent = document.getElementById("snippet-content");
const snippetList = document.getElementById("snippet-list");
const snippetMessage = document.getElementById("snippet-message");
const loadSnippetsButton = document.getElementById("load-snippets");
const editModal = document.getElementById("edit-modal");
const closeEditModalButton = document.getElementById("close-edit-modal");
const editForm = document.getElementById("edit-form");
const editTitle = document.getElementById("edit-title");
const editTag = document.getElementById("edit-tag");
const editContent = document.getElementById("edit-content");
const editMessage = document.getElementById("edit-message");

let editingId = null;

async function loadSnippets() {
  snippetMessage.textContent = "Loading snippets...";
  const response = await fetch(apiUrl("/project3/snippet"));
  if (!response.ok) {
    snippetMessage.textContent = "List request failed. One of the API calls is wrong.";
    return;
  }
  const snippets = await response.json();
  snippetList.innerHTML = "";

  snippets.forEach((snippet) => {
    const card = document.createElement("article");
    card.className = "snippet-card";
    card.innerHTML = `
      <strong>${snippet.title}</strong>
      <div class="todo-meta">${snippet.tag}</div>
      <p>${snippet.content}</p>
      <div class="snippet-actions">
        <button class="mini-btn" data-action="edit" data-id="${snippet.id}">Edit</button>
        <button class="mini-btn" data-action="delete" data-id="${snippet.id}">Delete</button>
      </div>
    `;
    snippetList.appendChild(card);
  });

  snippetMessage.textContent = "";
}

async function saveSnippet(event) {
  event.preventDefault();
  const payload = {
    title: snippetTitle.value.trim(),
    content: snippetContent.value.trim(),
    tag: snippetTag.value.trim(),
  };

  const url = editingId ? apiUrl(`/project3/snippets/${editingId}`) : apiUrl("/project3/snippets");
  const method = editingId ? "POST" : "POST";

  const response = await fetch(url, {
    method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    snippetMessage.textContent = "Save request failed. Another API call is wrong.";
    return;
  }

  editingId = null;
  snippetForm.reset();
  snippetMessage.textContent = "Snippet saved.";
  loadSnippets();
}

function openEditModal() {
  editModal.classList.remove("hidden");
  editMessage.textContent = "";
  editTitle.focus();
}

function closeEditModal() {
  editModal.classList.add("hidden");
  editForm.reset();
  editMessage.textContent = "";
  editingId = null;
}

async function updateSnippet(event) {
  event.preventDefault();

  const response = await fetch(apiUrl(`/project3/snippets/${editingId}`), {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      title: editTitle.value.trim(),
      content: editContent.value.trim(),
      tag: editTag.value.trim(),
    }),
  });

  if (!response.ok) {
    editMessage.textContent = "Update failed. Look at the backend route method.";
    return;
  }

  closeEditModal();
  snippetMessage.textContent = "Article updated.";
  loadSnippets();
}

async function handleSnippetActions(event) {
  const button = event.target.closest("button");
  if (!button) {
    return;
  }

  const id = button.dataset.id;
  const action = button.dataset.action;

  if (action === "edit") {
    const card = button.closest(".snippet-card");
    editTitle.value = card.querySelector("strong").textContent;
    editTag.value = card.querySelector(".todo-meta").textContent;
    editContent.value = card.querySelector("p").textContent;
    editingId = id;
    openEditModal();
    return;
  }

  if (action === "delete") {
    const response = await fetch(apiUrl(`/project3/snippets?id=${id}`), { method: "DELETE" });
    if (!response.ok) {
      snippetMessage.textContent = "Delete request failed. Another API call is wrong.";
      return;
    }
    loadSnippets();
  }
}

snippetForm.addEventListener("submit", saveSnippet);
snippetList.addEventListener("click", handleSnippetActions);
loadSnippetsButton.addEventListener("click", loadSnippets);
editForm.addEventListener("submit", updateSnippet);
closeEditModalButton.addEventListener("click", closeEditModal);
editModal.addEventListener("click", (event) => {
  if (event.target === editModal) {
    closeEditModal();
  }
});

loadSnippets();
