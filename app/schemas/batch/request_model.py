from pydantic import BaseModel, Field
from typing import List


class User(BaseModel):
    name: str
    note: str

class ReportsInBatchRequest(BaseModel):
    system_instruction: str = Field(default=None)
    prompt: str = Field(default=None)
    users: List[User]