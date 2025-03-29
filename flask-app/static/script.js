async function fetchTasks() {
  const response = await fetch("/tasks");
  const tasks = await response.json();
  const taskList = document.getElementById("taskList");
  taskList.innerHTML = "";

  tasks.forEach((task) => {
    const li = document.createElement("li");
    li.classList.add("list-group-item", "task-item");
    if (task.completed) li.classList.add("completed");

    const taskName = document.createElement("span");
    taskName.textContent = task.name;
    taskName.classList.add("task-name");

    const toggleBtn = document.createElement("button");
    toggleBtn.textContent = task.completed ? "Undo" : "Done";
    toggleBtn.classList.add("btn", "btn-success", "btn-sm", "mx-2");
    toggleBtn.onclick = () => toggleTask(task.id);

    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "Delete";
    deleteBtn.classList.add("btn", "btn-danger", "btn-sm");
    deleteBtn.onclick = () => deleteTask(task.id);

    li.appendChild(taskName);
    li.appendChild(toggleBtn);
    li.appendChild(deleteBtn);

    taskList.appendChild(li);
  });
}

async function addTask() {
  const taskInput = document.getElementById("taskInput");
  if (taskInput.value.trim() === "") return;

  await fetch("/tasks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: taskInput.value }),
  });

  taskInput.value = "";
  fetchTasks();
}

async function toggleTask(taskId) {
  await fetch(`/tasks/${taskId}`, { method: "PUT" });
  fetchTasks();
}

async function deleteTask(taskId) {
  await fetch(`/tasks/${taskId}`, { method: "DELETE" });
  fetchTasks();
}

fetchTasks();
