from pymongo.asynchronous.collection import AsyncCollection
from ..mdb import database 


COLLECTION_NAME = "task"
task_collection: AsyncCollection = database[COLLECTION_NAME]