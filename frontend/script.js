const inputTopic = document.getElementById("input")
const submitBtn = document.getElementById("button")
const statusSpan = document.getElementById("status")
const statusID = document.getElementById("return_id")
const checkBtn = document.getElementById("check")
const inputTaskId = document.getElementById("task_id")
const downloadDiv = document.getElementById("download")
const downloadBtn = document.getElementById("download-button")

const API = `http://${window.location.hostname}:8000`

let readyTaskId = null

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

    const result = await response.json()
    
    return result
}

async function getResearch(task_id){
    const get_url = `${API}/research/${task_id}`
    const response = await fetch(get_url)
    const data = await response.json()
    return data
}

submitBtn.addEventListener('click', async function () {
    const output_response = await postTopic()
    if(output_response.task_id){
        const currentTaskId = output_response.task_id
        statusID.textContent = "Task created: " + currentTaskId
    }

    else{
        statusID.textContent = "Error: " + output_response.error; 
    }
})

checkBtn.addEventListener('click', async function (){
    const taskID = inputTaskId.value.trim()
    if (!taskID) {
        statusSpan.textContent = "Enter a task id first"
        return
    }
    const data = await getResearch(taskID)
    statusSpan.textContent = "Your status: " + data.status

    if (data.report_ready) {
            readyTaskId = taskID
            downloadBtn.style.display = "inline-block"
        } else {
            readyTaskId = null
            downloadBtn.style.display = "none"
        }
})


downloadBtn.addEventListener('click', async function(){
    if (!readyTaskId) {
        downloadDiv.textContent = "Report not ready"
        return
    }

    window.location.href = `${API}/research/${readyTaskId}/pdf`
    
})