from rq import Worker, Queue, Connection
import redis

import os


listen = ['high', 'default', 'low']

redis_url = os.environ.get('REDISTOGO_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)


if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
