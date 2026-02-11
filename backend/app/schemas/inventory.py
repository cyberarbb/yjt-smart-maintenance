from pydantic import BaseModel
from datetime import datetime


class InventoryBase(BaseModel):
    part_id: str
    quantity: int = 0
    min_quantity: int = 5
    warehouse: str = "Busan HQ"


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(BaseModel):
    quantity: int | None = None
    min_quantity: int | None = None
    warehouse: str | None = None


class InventoryAdjust(BaseModel):
    adjustment: int  # positive = 입고, negative = 출고
    reason: str = ""


class InventoryResponse(InventoryBase):
    id: str
    last_updated: datetime
    is_low_stock: bool = False

    model_config = {"from_attributes": True}


class InventoryWithPart(InventoryResponse):
    part_name: str = ""
    part_number: str = ""
    brand: str = ""
    turbo_model: str = ""
