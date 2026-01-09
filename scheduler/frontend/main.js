const apiBase = "http://127.0.0.1:8000"; 

async function fetchTasks() {
    const res = await fetch(`${apiBase}/tasks`);
    const tasks = await res.json();
    renderTasks(tasks);
}

function renderTasks(tasks) {
    const tbody = document.querySelector("#tasksTable tbody");
    tbody.innerHTML = "";

    tasks.forEach(task => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${task.id}</td>
            <td>${task.name}</td>
            <td>
                <span class="badge ${task.status === 'active' ? 'bg-success' : 'bg-warning'}">
                    ${task.status}
                </span>
            </td>
            <td>${task.schedule_type}</td>
            <td>${task.next_run ?? '-'}</td>
            <td>
                <button class="btn btn-sm btn-warning me-1" onclick="pauseTask(${task.id})">Pause</button>
                <button class="btn btn-sm btn-success me-1" onclick="resumeTask(${task.id})">Resume</button>
                <button class="btn btn-sm btn-danger" onclick="deleteTask(${task.id})">Delete</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// Action functions (PATCH/DELETE)
async function pauseTask(id) {
    await fetch(`${apiBase}/tasks/${id}/pause`, { method: 'PATCH' });
    fetchTasks();
}
async function resumeTask(id) {
    await fetch(`${apiBase}/tasks/${id}/resume`, { method: 'PATCH' });
    fetchTasks();
}
async function deleteTask(id) {
    if (!confirm('Are you sure?')) return;
    await fetch(`${apiBase}/tasks/${id}`, { method: 'DELETE' });
    fetchTasks();
}

// Auto-refresh table every 5 seconds
setInterval(fetchTasks, 5000);
fetchTasks();
