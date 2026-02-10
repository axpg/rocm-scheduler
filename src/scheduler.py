import redis.asyncio as redis
from models import Job, JobStatus, SchedulingPolicy
from datetime import datetime, timezone
import json

class RedisQueue:
    """
    A class for queuing jobs in Redis.

    PENDING_QUEUE, PRIORITY_QUEUE, JOB_PREFIX
    are all keys for our redis instance. (kinda)

    Only store job_id in the queue


    """

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.PENDING_QUEUE = "queue:pending"
        self.PRIORITY_QUEUE = "queue:priority"
        self.JOB_PREFIX = "job:"

    async def enqueue(self, job: Job) -> None:
        """
        """
        job_key = f"{self.JOB_PREFIX}{job.job_id}"
        job_data = job.model_dump_json()

        await self.redis.hset(job_key, "data", job_data)
        await self.redis.lpush(self.PENDING_QUEUE, job.job_id)
        await self.redis.zadd(self.PRIORITY_QUEUE, job.job_id)
        return
    
    async def dequeue_fifo(self) -> Job | None:
        job_id = await self.redis.rpop(self.PENDING_QUEUE)
        return await self.get_job(job_id)
    
    async def dequeue_priority(self) -> Job | None:
        job_id = await self.redis.zpopmax(self.PRIORITY_QUEUE)
        return await self.get_job(job_id)
    
    async def get_job(self, job_id: int) -> Job | None:
        job_data : json = await self.redis.hget(f"{self.JOB_PREFIX}{job_id}")
        # TODO: logic to deserialize json into Job object
        return 
        
    async def update_job(self, job_id) -> None:
        return