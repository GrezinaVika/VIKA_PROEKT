from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TableCreate(BaseModel):
    table_number: int
    seats: int

class TableUpdate(BaseModel):
    seats: Optional[int] = None
    is_occupied: Optional[bool] = None

class TableResponse(BaseModel):
    id: int
    table_number: int
    seats: int
    is_occupied: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
