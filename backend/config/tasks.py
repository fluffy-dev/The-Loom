from pydantic import Field
from pydantic_settings import BaseSettings



class TaskSettings(BaseSettings):
    """
    Configuration for background tasks.
    """
    CLEANUP_INTERVAL_SECONDS: int = Field(3600, alias="CLEANUP_INTERVAL_SECONDS")  # 1 час
    ROOM_LIFETIME_DAYS: int = Field(7, alias="ROOM_LIFETIME_DAYS")
    ROOM_INACTIVITY_HOURS: int = Field(3, alias="ROOM_INACTIVITY_HOURS")

task_settings = TaskSettings()