from pydantic import BaseModel, Field, field_validator
from typing import Optional

class ItemCreate(BaseModel):
    name: str = Field(..., min_length=2, example="Ноутбук")
    description: Optional[str] = Field(None, max_length=500, example="Описание товара")
    price: float = Field(..., gt=0, example=100.0)
    tax: Optional[float] = Field(None, example=10.5)

    @field_validator('price')
    @classmethod
    def validate_price(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('Цена должна быть положительной')
        return v

class ItemResponse(ItemCreate):
    id: int = Field(..., example=1)