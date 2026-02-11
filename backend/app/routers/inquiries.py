from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.inquiry import Inquiry
from app.schemas.inquiry import InquiryCreate, InquiryUpdate, InquiryResponse

router = APIRouter()


@router.get("/", response_model=list[InquiryResponse])
def get_inquiries(
    skip: int = 0,
    limit: int = 50,
    resolved: bool | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Inquiry)
    if resolved is not None:
        query = query.filter(Inquiry.is_resolved == resolved)
    return query.order_by(Inquiry.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/{inquiry_id}", response_model=InquiryResponse)
def get_inquiry(inquiry_id: str, db: Session = Depends(get_db)):
    inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    return inquiry


@router.post("/", response_model=InquiryResponse, status_code=201)
def create_inquiry(data: InquiryCreate, db: Session = Depends(get_db)):
    inquiry = Inquiry(**data.model_dump())
    db.add(inquiry)
    db.commit()
    db.refresh(inquiry)
    return inquiry


@router.put("/{inquiry_id}", response_model=InquiryResponse)
def update_inquiry(inquiry_id: str, data: InquiryUpdate, db: Session = Depends(get_db)):
    inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(inquiry, key, value)
    db.commit()
    db.refresh(inquiry)
    return inquiry
