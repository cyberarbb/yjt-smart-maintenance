from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models.inventory import Inventory
from app.models.part import Part
from app.schemas.inventory import (
    InventoryCreate,
    InventoryUpdate,
    InventoryAdjust,
    InventoryResponse,
    InventoryWithPart,
)

router = APIRouter()


@router.get("/", response_model=list[InventoryWithPart])
def get_inventory(
    low_stock_only: bool = False,
    warehouse: str | None = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    query = db.query(Inventory).options(joinedload(Inventory.part))
    if low_stock_only:
        query = query.filter(Inventory.quantity <= Inventory.min_quantity)
    if warehouse:
        query = query.filter(Inventory.warehouse == warehouse)

    items = query.offset(skip).limit(limit).all()

    result = []
    for item in items:
        inv = InventoryWithPart(
            id=item.id,
            part_id=item.part_id,
            quantity=item.quantity,
            min_quantity=item.min_quantity,
            warehouse=item.warehouse,
            last_updated=item.last_updated,
            is_low_stock=item.is_low_stock,
            part_name=item.part.name if item.part else "",
            part_number=item.part.part_number if item.part else "",
            brand=item.part.brand if item.part else "",
            turbo_model=item.part.turbo_model if item.part else "",
        )
        result.append(inv)
    return result


@router.get("/low-stock", response_model=list[InventoryWithPart])
def get_low_stock(db: Session = Depends(get_db)):
    items = (
        db.query(Inventory)
        .options(joinedload(Inventory.part))
        .filter(Inventory.quantity <= Inventory.min_quantity)
        .all()
    )
    result = []
    for item in items:
        inv = InventoryWithPart(
            id=item.id,
            part_id=item.part_id,
            quantity=item.quantity,
            min_quantity=item.min_quantity,
            warehouse=item.warehouse,
            last_updated=item.last_updated,
            is_low_stock=True,
            part_name=item.part.name if item.part else "",
            part_number=item.part.part_number if item.part else "",
            brand=item.part.brand if item.part else "",
            turbo_model=item.part.turbo_model if item.part else "",
        )
        result.append(inv)
    return result


@router.get("/stats")
def get_inventory_stats(db: Session = Depends(get_db)):
    total_items = db.query(Inventory).count()
    low_stock = db.query(Inventory).filter(Inventory.quantity <= Inventory.min_quantity).count()
    total_quantity = sum(
        i.quantity for i in db.query(Inventory.quantity).all()
    )
    return {
        "total_items": total_items,
        "low_stock_count": low_stock,
        "total_quantity": total_quantity,
    }


@router.put("/{inventory_id}", response_model=InventoryResponse)
def update_inventory(inventory_id: str, data: InventoryUpdate, db: Session = Depends(get_db)):
    inv = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Inventory not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(inv, key, value)
    db.commit()
    db.refresh(inv)
    return inv


@router.post("/{inventory_id}/adjust", response_model=InventoryResponse)
def adjust_inventory(inventory_id: str, data: InventoryAdjust, db: Session = Depends(get_db)):
    inv = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Inventory not found")

    new_qty = inv.quantity + data.adjustment
    if new_qty < 0:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    inv.quantity = new_qty
    db.commit()
    db.refresh(inv)
    return inv
