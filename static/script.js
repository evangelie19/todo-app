// This function fetches tasks from the API and displays them on the page
async function getTasks() {
    try {
        // Fetch tasks using the Fetch API
        const response = await fetch('http://localhost:8000/tasks/');
        const tasks = await response.json();

        // Get the div where tasks will be displayed
        const taskListElement = document.getElementById('taskList');

        // Clear the current content of the div
        taskListElement.innerHTML = '';

        // Check the number of tasks
        if (tasks.length === 0) {
            // If there are no tasks, hide the "Delete All" button
            document.getElementById('deleteAllContainer').style.display = 'none';
        } else {
            // If there are tasks, show the "Delete All" button
            document.getElementById('deleteAllContainer').style.display = 'block';

            // Add each task to the div
            tasks.forEach((task) => {
                const taskElement = document.createElement('div');
                taskElement.classList.add('task-container');  // Add a class to the task container
                taskElement.innerHTML = `
                    <div class="task-content">
                        <input type="checkbox" onclick="toggleTaskStatus('${task.id}', this.checked)" ${task.done ? 'checked' : ''}>
                        <div class="text-content">
                            <h2>${task.title}</h2>
                            <p>${task.description}</p>
                        </div>
                    </div>
                    <button onclick="deleteTask('${task.id}')">Delete</button>
                `;
                taskListElement.appendChild(taskElement);
            });
        }
    } catch (error) {
        console.error('An error occurred while fetching the tasks:', error);
    }
}


// New function to send a new task to the API
async function createTask() {
    // Get data from the form
    const title = document.getElementById('taskTitle').value;
    const description = document.getElementById('taskDescription').value;

    // Create a new task object
    const task = {
        title: title,
        description: description,
        done: false  // By default, the task is not done
    };

    try {
        // Send the task to the API using the Fetch API
        await fetch('http://localhost:8000/tasks/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(task),
        });

        // Clear the form
        document.getElementById('taskTitle').value = '';
        document.getElementById('taskDescription').value = '';

        // Reload tasks to see the new task in the list
        getTasks();
    } catch (error) {
        console.error('An error occurred while creating the task:', error);
    }
}

// Function to update task status
async function toggleTaskStatus(id, status) {
    try {
        // Send the updated status to the API using the Fetch API
        await fetch(`http://localhost:8000/tasks/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ done: status }),  // Update status only
        });

        // Reload tasks to see the updated status in the list
        getTasks();
    } catch (error) {
        console.error('An error occurred while updating the task:', error);
    }
}

// Function to delete a task
async function deleteTask(id) {
    try {
        // Send a DELETE request to the API to delete the task
        await fetch(`http://localhost:8000/tasks/${id}`, {
            method: 'DELETE',
        });

        // Reload the tasks to reflect the change
        getTasks();
    } catch (error) {
        console.error('An error occurred while deleting the task:', error);
    }
}

// New function to delete all tasks
async function deleteAllTasks() {
    try {
        // Send a DELETE request to the new API endpoint to delete all tasks
        await fetch('http://localhost:8000/tasks/', {
            method: 'DELETE',
        });

        // Reload the tasks to reflect the change
        getTasks();
    } catch (error) {
        console.error('An error occurred while deleting all tasks:', error);
    }
}
