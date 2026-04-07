const todoForm = document.getElementById("todo-form");
const todoInput = document.getElementById("todo-input");
const todoList = document.getElementById("todo-list");
const todoMessage = document.getElementById("todo-message");
const reloadTodosButton = document.getElementById("reload-todos");

async function loadTodos() {
  todoMessage.textContent = "Loading todos...";
  const response = await fetch(apiUrl("/project1/todos"));
  const todos = await response.json();

  todoList.innerHTML = "";

  if (!todos.length) {
    todoList.innerHTML = '<div class="todo-card">No todos yet.</div>';
    todoMessage.textContent = "";
    return;
  }

  todos.forEach((todo) => {
    const card = document.createElement("article");
    card.className = `todo-card ${todo.completed ? "completed" : ""}`;
    card.innerHTML = `
      <strong>${todo.title}</strong>
      <div class="todo-meta">${todo.completed ? "Completed" : "Pending"}</div>
      <div class="todo-actions">
        <button class="mini-btn" data-action="toggle" data-id="${todo.id}">${todo.completed ? "Undo" : "Toggle"}</button>
        <button class="mini-btn" data-action="edit" data-id="${todo.id}" data-title="${todo.title}">Edit</button>
        <button class="mini-btn" data-action="delete" data-id="${todo.id}">Delete</button>
      </div>
    `;
    todoList.appendChild(card);
  });

  todoMessage.textContent = "";
}

async function createTodo(event) {
  event.preventDefault();
  const title = todoInput.value.trim();
  if (!title) {
    todoMessage.textContent = "Write something first.";
    return;
  }

  const response = await fetch(apiUrl("/project1/todos"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });

  if (!response.ok) {
    todoMessage.textContent = "Could not create todo.";
    return;
  }

  todoInput.value = "";
  todoMessage.textContent = "Todo created.";
  loadTodos();
}

async function handleTodoActions(event) {
  const button = event.target.closest("button");
  if (!button) {
    return;
  }

  const id = button.dataset.id;
  const action = button.dataset.action;

  if (action === "toggle") {
    await fetch(apiUrl(`/project1/todos/${id}/toggle`), { method: "PATCH" });
    loadTodos();
    return;
  }

  if (action === "edit") {
    const nextTitle = window.prompt("Update todo title", button.dataset.title || "");
    if (!nextTitle) {
      return;
    }
    await fetch(apiUrl(`/project1/todos/${id}`), {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: nextTitle }),
    });
    loadTodos();
    return;
  }

  if (action === "delete") {
    await fetch(apiUrl(`/project1/todos/${id}`), { method: "DELETE" });
    loadTodos();
  }
}

todoForm.addEventListener("submit", createTodo);
todoList.addEventListener("click", handleTodoActions);
reloadTodosButton.addEventListener("click", loadTodos);

loadTodos();
