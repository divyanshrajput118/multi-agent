from fastapi import FastAPI, Path, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from .db import task_collection, TaskSchema
from .queue import process_topic, q
from bson import ObjectId
from .utils import create_pdf, save_to_disk
from .input_schema import InputSchema
import asyncio
import os



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],)


async def get_task_or_404(task_id: str):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")
    task = await task_collection.find_one({"_id": ObjectId(task_id)})
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.get("/health")
def home():
    return {"message": "Hi from this page!!"}


@app.get("/research/{task_id}")
async def response(task_id: str = Path(..., description="ID of the task")):
    task = await get_task_or_404(task_id)
    return {
        "status": task.get("status"),
        "report_ready": bool(task.get("report")),
    }


@app.get("/research/{task_id}/pdf") 
async def download_pdf(task_id: str = Path(..., description="ID of the task")):
    task = await get_task_or_404(task_id)
    if not task.get("report"):
        raise HTTPException(status_code=409, detail="Report not ready yet")
    file_path = f"/mnt/uploads/{task_id}/report.pdf"
    file_name = "report.pdf"
    if not os.path.exists(file_path):
        await task_collection.update_one(
            {"_id": ObjectId(task_id)}, {"$set": {"status": "Converting_to_PDF"}}
        )
        pdf_bytes = await asyncio.to_thread(create_pdf, task)
        await save_to_disk(pdf_bytes, file_path)
        await task_collection.update_one(
            {"_id": ObjectId(task_id)}, {"$set": {"status": "PDF_Generated"}}
        )

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=file_name
    )


@app.post("/research")
async def research(input_data: InputSchema):
    topic = input_data.topic
    db_task = await task_collection.insert_one(document=TaskSchema(
                                                        topic=topic,
                                                        status="Initiated"
                                                    ).model_dump())
    task_id = str(db_task.inserted_id)

    await task_collection.update_one({"_id": ObjectId(task_id)}, {
            "$set": {
                "status": "Queued"
            }
        })

    q.enqueue(process_topic, topic, task_id)

    return {"task_id": task_id}