from datetime import datetime
from enum import StrEnum
from typing import Optional
from uuid import uuid4
from pydantic import BaseModel, Field, field_validator

class JobStatus(StrEnum):
    """
    Defines the lifecycle for a job.

    State Transitions
    TODO: state transition diagram
    """
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class SchedulingPolicy(StrEnum): 
    """
    Defines the job scheduling policies to be used. 
    """
    FIFO = "fifo"
    PRIORITY = "priority"
    FIRST_FIT = "first_fit"

class Job(BaseModel):
    """
    Represents an ML workload to be scheduled. 
    """
    job_id: uuid4
    command: str

    vram_required_mb: int

    status: JobStatus

    submitted_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]

    exit_code: int
