from pydantic import BaseModel
from datetime import datetime


class ServiceOrderBase(BaseModel):
    customer_id: str
    order_type: str
    turbo_brand: str
    turbo_model: str
    vessel_name: str | None = None
    description: str | None = None


class ServiceOrderCreate(ServiceOrderBase):
    pass


class ServiceOrderUpdate(BaseModel):
    status: str | None = None
    description: str | None = None
    vessel_name: str | None = None


class ServiceOrderResponse(ServiceOrderBase):
    id: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ServiceOrderWithCustomer(ServiceOrderResponse):
    customer_name: str = ""
    customer_company: str = ""
