from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app.models.part import Part
from app.models.inventory import Inventory
from app.schemas.part import PartCreate, PartUpdate, PartResponse, PartWithInventory

router = APIRouter()


@router.get("/", response_model=list[PartWithInventory])
def get_parts(
    skip: int = 0,
    limit: int = 50,
    brand: str | None = None,
    category: str | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Part)
    if brand:
        query = query.filter(Part.brand == brand)
    if category:
        query = query.filter(Part.category == category)
    if search:
        query = query.filter(
            or_(
                Part.name.ilike(f"%{search}%"),
                Part.part_number.ilike(f"%{search}%"),
                Part.turbo_model.ilike(f"%{search}%"),
            )
        )
    parts = query.offset(skip).limit(limit).all()

    result = []
    for part in parts:
        part_dict = PartWithInventory.model_validate(part)
        if part.inventory:
            part_dict.inventory = {
                "quantity": part.inventory.quantity,
                "min_quantity": part.inventory.min_quantity,
                "warehouse": part.inventory.warehouse,
                "is_low_stock": part.inventory.is_low_stock,
            }
        result.append(part_dict)
    return result


@router.get("/{part_id}", response_model=PartWithInventory)
def get_part(part_id: str, db: Session = Depends(get_db)):
    part = db.query(Part).filter(Part.id == part_id).first()
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")
    result = PartWithInventory.model_validate(part)
    if part.inventory:
        result.inventory = {
            "quantity": part.inventory.quantity,
            "min_quantity": part.inventory.min_quantity,
            "warehouse": part.inventory.warehouse,
            "is_low_stock": part.inventory.is_low_stock,
        }
    return result


@router.post("/", response_model=PartResponse, status_code=201)
def create_part(part_data: PartCreate, db: Session = Depends(get_db)):
    existing = db.query(Part).filter(Part.part_number == part_data.part_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Part number already exists")

    part = Part(**part_data.model_dump())
    db.add(part)
    db.commit()
    db.refresh(part)

    # Auto-create inventory record
    inv = Inventory(part_id=part.id)
    db.add(inv)
    db.commit()

    return part


@router.put("/{part_id}", response_model=PartResponse)
def update_part(part_id: str, part_data: PartUpdate, db: Session = Depends(get_db)):
    part = db.query(Part).filter(Part.id == part_id).first()
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")

    for key, value in part_data.model_dump(exclude_unset=True).items():
        setattr(part, key, value)
    db.commit()
    db.refresh(part)
    return part


@router.delete("/{part_id}")
def delete_part(part_id: str, db: Session = Depends(get_db)):
    part = db.query(Part).filter(Part.id == part_id).first()
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")
    db.delete(part)
    db.commit()
    return {"message": "Part deleted"}


@router.get("/brands/list", response_model=list[str])
def get_brands(db: Session = Depends(get_db)):
    brands = db.query(Part.brand).distinct().all()
    return [b[0] for b in brands]


@router.get("/categories/list", response_model=list[str])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Part.category).distinct().all()
    return [c[0] for c in categories]
