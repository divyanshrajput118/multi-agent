from redis import Redis
from rq import Queue

q = Queue(connection=Redis(
    host="valkey",
    port=6379
))

