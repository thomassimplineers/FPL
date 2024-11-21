document.addEventListener('DOMContentLoaded', () => {
    const taskForm = document.getElementById('task-form');
    const taskInput = document.getElementById('task-input');
    const taskList = document.getElementById('task-list');

    // Hämta uppgifter från LocalStorage
    const getTasks = () => {
        const tasks = localStorage.getItem('tasks');
        return tasks ? JSON.parse(tasks) : [];
    };

    // Spara uppgifter till LocalStorage
    const saveTasks = (tasks) => {
        localStorage.setItem('tasks', JSON.stringify(tasks));
    };

    // Lägg till uppgift i DOM och spara
    const addTask = (task) => {
        const li = document.createElement('li');
        li.textContent = task;
        li.addEventListener('click', () => {
            li.classList.toggle('done');
        });

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Ta bort';
        deleteButton.addEventListener('click', () => {
            taskList.removeChild(li);
            const tasks = getTasks().filter(t => t !== task);
            saveTasks(tasks);
        });

        li.appendChild(deleteButton);
        taskList.appendChild(li);
    };

    // Rendera alla uppgifter
    getTasks().forEach(addTask);

    // Lägg till ny uppgift via formuläret
    taskForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const task = taskInput.value.trim();
        if (task) {
            addTask(task);
            const tasks = getTasks();
            tasks.push(task);
            saveTasks(tasks);
            taskInput.value = '';
        }
    });
});
