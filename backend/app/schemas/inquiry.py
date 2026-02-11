from pydantic import BaseModel
from datetime import datetime


class InquiryBase(BaseModel):
    subject: str
    message: str
    contact_email: str
    customer_id: str | None = None


class InquiryCreate(InquiryBase):
    pass


class InquiryUpdate(BaseModel):
    is_resolved: bool | None = None
    response: str | None = None


class InquiryResponse(InquiryBase):
    id: str
    is_resolved: bool
    response: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
