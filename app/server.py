from fastapi import FastAPI, Path, HTTPException
from fastapi.responses import FileResponse
from .db import task_collection, TaskSchema
from .queue import process_topic, q
from bson import ObjectId
from .utils import create_pdf, save_to_disk
import asyncio



app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hi from this page!!"}


@app.get("/research/{task_id}")
async def response(task_id: str = Path(..., description="ID of the task")):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid task ID"
        )
    task = await task_collection.find_one({"_id": ObjectId(task_id)})
    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    if not task["report"]:
        return {"message": task["status"]}
    
    file_path = f"/mnt/uploads/{task_id}/report.pdf"
    file_name = "report.pdf"
    await task_collection.update_one({"_id": ObjectId(task_id)}, {
                    "$set": {
                        "status": "Converting_to_PDF"
                    }
                })
    pdf_bytes = await asyncio.to_thread(
        create_pdf,
        task
    )
    await save_to_disk(
        pdf_bytes,
        file_path
    )
    await task_collection.update_one({"_id": ObjectId(task_id)}, {
                        "$set": {
                            "status": "PDF_Generated"
                        }
                    })
    return FileResponse(
                        path=file_path,
                        media_type="application/pdf",
                        filename=file_name
                    )

@app.post("/research")
async def research(topic: str):
    db_task = await task_collection.insert_one(document=TaskSchema(
                                                        topic=topic,
                                                        status="Initiated"
                                                    ).model_dump())
    task_id = str(db_task.inserted_id)

    q.enqueue(process_topic, topic, task_id)

    await task_collection.update_one({"_id": ObjectId(task_id)}, {
            "$set": {
                "status": "Queued"
            }
        })

    return {"task_id": task_id}