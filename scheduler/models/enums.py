from enum import Enum

class ScheduleType(str, Enum):
    once = "once"
    interval = "interval"
    cron = "cron"

class TaskStatus(str, Enum):
    active = "active"
    paused = "paused"
