counter = document.querySelector(".task")

for (const task of document.querySelectorAll(".tasks_jobs")){
    task.addEventListener('change',()=>{

        fetch(`/done-task/`+String(task.id), {
        method: "post",
        headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
          .value,
      },
      });
        task.parentElement.parentElement.parentElement.remove()
        counter = counter.textContent -= 1 
        
    }
)
}