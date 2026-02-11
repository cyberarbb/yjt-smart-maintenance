from pydantic import BaseModel
from datetime import datetime


class PartBase(BaseModel):
    part_number: str
    name: str
    brand: str
    turbo_model: str
    category: str
    description: str | None = None
    unit_price: float = 0.0


class PartCreate(PartBase):
    pass


class PartUpdate(BaseModel):
    name: str | None = None
    brand: str | None = None
    turbo_model: str | None = None
    category: str | None = None
    description: str | None = None
    unit_price: float | None = None


class PartResponse(PartBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PartWithInventory(PartResponse):
    inventory: "InventoryBrief | None" = None


class InventoryBrief(BaseModel):
    quantity: int
    min_quantity: int
    warehouse: str
    is_low_stock: bool = False

    model_config = {"from_attributes": True}


PartWithInventory.model_rebuild()
