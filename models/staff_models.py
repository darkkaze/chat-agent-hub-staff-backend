from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from .helper import id_generator
import json


class Staff(SQLModel, table=True):
    """Modelo para personal del punto de venta con horarios de trabajo."""
    id: str = Field(default_factory=id_generator('staff', 10), primary_key=True)
    name: str = Field(index=True)
    email: str | None = Field(default=None, index=True)
    schedule: str = Field(default="{}")  # JSON string for weekly schedule
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def get_schedule(self) -> dict:
        """Parse schedule JSON string to Python dict."""
        return json.loads(self.schedule) if self.schedule else {}

    def set_schedule(self, schedule: dict):
        """Set schedule from Python dict to JSON string."""
        self.schedule = json.dumps(schedule)
