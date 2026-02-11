from pydantic import BaseModel
from datetime import datetime


class CustomerBase(BaseModel):
    company_name: str
    contact_name: str
    email: str
    phone: str | None = None
    country: str
    vessel_type: str | None = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    company_name: str | None = None
    contact_name: str | None = None
    email: str | None = None
    phone: str | None = None
    country: str | None = None
    vessel_type: str | None = None


class CustomerResponse(CustomerBase):
    id: str
    created_at: datetime

    model_config = {"from_attributes": True}
