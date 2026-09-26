from ..langgraph import my_graph
from ..db import task_collection
from bson import ObjectId
import openai

async def process_topic(topic: str, task_id: str):
    try:
        await task_collection.update_one({"_id": ObjectId(task_id)}, {
            "$set": {
                "status": "Processing"
            }
        })
        state = {"topic": topic}
        response = await my_graph.ainvoke(state)
        await task_collection.update_one({"_id": ObjectId(task_id)}, {
                "$set": {
                    "status": "Research_Completed",
                    "report": response['report']
                }
            })

    except openai.APIStatusError as e:
        if e.status_code == 402:
            error_status = "Insufficient Balance Error"
        else:
            error_status = "API Error"
        await task_collection.update_one(
            {"_id": ObjectId(task_id)},
            {
                "$set": {
                    "status": error_status,
                    "error_details": str(e)
                }
            }
        )
        raise e

    except Exception as e:
        await task_collection.update_one(
            {"_id": ObjectId(task_id)},
            {
                "$set": {
                    "status": "Failed",
                    "error_details": str(e)
                }
            }
        )
        raise e

