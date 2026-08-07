from redis import Redis
from rq import SimpleWorker, Queue

# Connect to the Redis server running in Docker on port 6379
redis_conn = Redis(host="localhost", port=6379)

if __name__ == "__main__":
    # Create a worker that watches the "default" queue for new jobs
    queue = Queue(connection=redis_conn)
    worker = SimpleWorker([queue], connection=redis_conn)
    worker.work()