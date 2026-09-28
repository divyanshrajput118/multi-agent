const inputTopic = document.getElementById("input")
const submitBtn = document.getElementById("button")
const statusSpan = document.getElementById("status")
const statusID = document.getElementById("return_id")
const checkBtn = document.getElementById("check")
const inputTaskId = document.getElementById("task_id")
const downloadDiv = document.getElementById("download")

const API = "http://localhost:8000"

async function postTopic(){
    const post_URL = `${API}/research`
    const data = {
        topic: inputTopic.value.trim()
    }
    const response = await fetch(post_URL,
        {
            method:'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        })

    const task_id = await response.json()
    
    return task_id.task_id
}

async function getResearch(task_id){
    const get_url = `${API}/research/${task_id}`
    const response = await fetch(get_url)
    const data = await response.json()
    return data
}
submitBtn.addEventListener('click', async function () {
    const currentTaskId = await postTopic()
    statusID.textContent = "Task created: " + currentTaskId
})

checkBtn.addEventListener('click', async function (){
    const taskID = inputTaskId.value.trim()
    if (!taskID) {
        statusSpan.textContent = "Enter a task id first"
        return
    }
    downloadDiv.textContent = ""
    const data = await getResearch(taskID)
    statusSpan.textContent = "Your status: " + data.status
    if (data.report_ready) {
            const link = document.createElement("a")
            link.href = `${API}/research/${taskID}/pdf`
            link.textContent = "Download report"
            link.style.color = "antiquewhite"
            downloadDiv.appendChild(link)
        }
})