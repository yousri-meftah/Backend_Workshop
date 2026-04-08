// Minimal Express version of the FastAPI todo app (project1).
// This file is for workshop comparison only.

const express = require("express");

const app = express();
app.use(express.json());

const todos = [
  {
    id: 1,
    title: "Explain what REST means",
    completed: false,
    created_at: new Date().toISOString(),
  },
  {
    id: 2,
    title: "Show CRUD with FastAPI",
    completed: true,
    created_at: new Date().toISOString(),
  },
];

let nextId = 3;

app.get("/project1/todos", (req, res) => {
  res.json(todos);
});

app.post("/project1/todos", (req, res) => {
  const title = String(req.body?.title || "").trim();
  if (!title) {
    return res.status(400).json({ detail: "title is required" });
  }

  const item = {
    id: nextId,
    title,
    completed: false,
    created_at: new Date().toISOString(),
  };
  nextId += 1;
  todos.unshift(item);
  res.json(item);
});

app.put("/project1/todos/:todoId", (req, res) => {
  const todoId = Number(req.params.todoId);
  const todo = todos.find((t) => t.id === todoId);
  if (!todo) {
    return res.status(404).json({ detail: "Todo not found" });
  }

  if (req.body.title !== undefined) {
    todo.title = String(req.body.title).trim();
  }
  if (req.body.completed !== undefined) {
    todo.completed = Boolean(req.body.completed);
  }

  res.json(todo);
});

app.patch("/project1/todos/:todoId/toggle", (req, res) => {
  const todoId = Number(req.params.todoId);
  const todo = todos.find((t) => t.id === todoId);
  if (!todo) {
    return res.status(404).json({ detail: "Todo not found" });
  }

  todo.completed = !todo.completed;
  res.json(todo);
});

app.delete("/project1/todos/:todoId", (req, res) => {
  const todoId = Number(req.params.todoId);
  const index = todos.findIndex((t) => t.id === todoId);
  if (index === -1) {
    return res.status(404).json({ detail: "Todo not found" });
  }

  const removed = todos.splice(index, 1)[0];
  res.json({ deleted: true, item: removed });
});

// Optional run command if you want to demo quickly:
// node todo_express.js
const PORT = 8001;
app.listen(PORT, () => {
  console.log(`Todo Express server running on http://localhost:${PORT}`);
});

