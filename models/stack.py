from unit import Unit
from pydantic import BaseModel, validator


class Stack(BaseModel):
    unit: Unit
    amount: int

    @validator('amount')
    def pos_int_pos_int_validator(cls, v):
        if not v > 0:
            raise ValueError(f'{v} must be greater than 0')
