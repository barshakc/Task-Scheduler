document.addEventListener("DOMContentLoaded", () => {
    const apiBase = "http://127.0.0.1:8000/tasks"; 

    // Populate table
    async function fetchTasks() {
        try {
            const res = await fetch(apiBase);
            if (!res.ok) throw new Error("Failed to fetch tasks");

            const tasks = await res.json();
            const tbody = document.querySelector("#tasksTable tbody");
            tbody.innerHTML = "";

            tasks.forEach(task => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${task.id}</td>
                    <td>${task.name}</td>
                    <td>${task.status}</td>
                    <td>${task.schedule_type}</td>
                    <td>${task.created_at ?? '-'}</td>
                    <td>
                      <button class="btn btn-sm btn-warning me-1" onclick="pauseTask(${task.id})">Pause</button>
                      <button class="btn btn-sm btn-success me-1" onclick="resumeTask(${task.id})">Resume</button>
                      <button class="btn btn-sm btn-danger" onclick="deleteTask(${task.id})">Delete</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        } catch (err) {
            console.error(err);
        }
    }

    // CRUD functions need to be global for inline onclick
    window.pauseTask = async (id) => { 
        const res = await fetch(`${apiBase}/${id}/pause`, {method:'PATCH'});
        if(!res.ok) alert("Failed to pause task");
        fetchTasks(); 
    };

    window.resumeTask = async (id) => { 
        const res = await fetch(`${apiBase}/${id}/resume`, {method:'PATCH'});
        if(!res.ok) alert("Failed to resume task");
        fetchTasks(); 
    };

    window.deleteTask = async (id) => { 
        if(confirm('Delete?')) { 
            const res = await fetch(`${apiBase}/${id}`, {method:'DELETE'}); 
            if(!res.ok) alert("Failed to delete task");
            fetchTasks(); 
        } 
    };

    // Create task form
    const createForm = document.getElementById("createTaskForm");
    createForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const data = {
            name: document.getElementById("taskName").value,
            description: document.getElementById("taskDescription").value,
            schedule_type: document.getElementById("taskScheduleType").value,
            schedule_value: document.getElementById("taskScheduleValue").value,
            max_retries: Number(document.getElementById("taskMaxRetries").value),
            retry_delay: Number(document.getElementById("taskRetryDelay").value)
        };
        try {
            const res = await fetch(apiBase, {
                method: "POST",
                headers: {"Content-Type":"application/json"},
                body: JSON.stringify(data)
            });
            if(!res.ok) throw new Error(await res.text());

            fetchTasks();
            bootstrap.Modal.getInstance(document.getElementById('createTaskModal')).hide();
            createForm.reset();
        } catch(err) {
            console.error(err);
            alert("Failed to create task: " + err.message);
        }
    });

    fetchTasks();
    setInterval(fetchTasks, 5000);
});
