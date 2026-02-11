from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models.service_order import ServiceOrder
from app.schemas.service_order import (
    ServiceOrderCreate,
    ServiceOrderUpdate,
    ServiceOrderResponse,
    ServiceOrderWithCustomer,
)

router = APIRouter()


@router.get("/", response_model=list[ServiceOrderWithCustomer])
def get_orders(
    skip: int = 0,
    limit: int = 50,
    status: str | None = None,
    order_type: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(ServiceOrder).options(joinedload(ServiceOrder.customer))
    if status:
        query = query.filter(ServiceOrder.status == status)
    if order_type:
        query = query.filter(ServiceOrder.order_type == order_type)

    orders = query.order_by(ServiceOrder.created_at.desc()).offset(skip).limit(limit).all()

    result = []
    for order in orders:
        o = ServiceOrderWithCustomer(
            id=order.id,
            customer_id=order.customer_id,
            order_type=order.order_type,
            turbo_brand=order.turbo_brand,
            turbo_model=order.turbo_model,
            vessel_name=order.vessel_name,
            status=order.status,
            description=order.description,
            created_at=order.created_at,
            updated_at=order.updated_at,
            customer_name=order.customer.contact_name if order.customer else "",
            customer_company=order.customer.company_name if order.customer else "",
        )
        result.append(o)
    return result


@router.get("/stats")
def get_order_stats(db: Session = Depends(get_db)):
    total = db.query(ServiceOrder).count()
    pending = db.query(ServiceOrder).filter(ServiceOrder.status == "Pending").count()
    in_progress = db.query(ServiceOrder).filter(ServiceOrder.status == "In Progress").count()
    completed = db.query(ServiceOrder).filter(ServiceOrder.status == "Completed").count()
    return {
        "total": total,
        "pending": pending,
        "in_progress": in_progress,
        "completed": completed,
    }


@router.get("/{order_id}", response_model=ServiceOrderResponse)
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(ServiceOrder).filter(ServiceOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("/", response_model=ServiceOrderResponse, status_code=201)
def create_order(data: ServiceOrderCreate, db: Session = Depends(get_db)):
    order = ServiceOrder(**data.model_dump())
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.put("/{order_id}", response_model=ServiceOrderResponse)
def update_order(order_id: str, data: ServiceOrderUpdate, db: Session = Depends(get_db)):
    order = db.query(ServiceOrder).filter(ServiceOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(order, key, value)
    db.commit()
    db.refresh(order)
    return order
