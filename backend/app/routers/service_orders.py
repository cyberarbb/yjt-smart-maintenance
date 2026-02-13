from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models.service_order import ServiceOrder
from app.models.customer import Customer
from app.models.user import User
from app.schemas.service_order import (
    ServiceOrderCreate,
    ServiceOrderUpdate,
    ServiceOrderResponse,
    ServiceOrderWithCustomer,
)
from app.services.auth_service import get_current_user, get_admin_user
from app.services.notification_service import notify_customer_by_email

router = APIRouter()


@router.get("", response_model=list[ServiceOrderWithCustomer])
def get_orders(
    skip: int = 0,
    limit: int = 50,
    status: str | None = None,
    order_type: str | None = None,
    user: User = Depends(get_current_user),
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


@router.get("/my-orders", response_model=list[ServiceOrderWithCustomer])
def get_my_orders(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """고객: 자신의 주문만 조회 (이메일 기반 매칭)"""
    customer = db.query(Customer).filter(Customer.email == user.email).first()
    if not customer:
        return []

    orders = (
        db.query(ServiceOrder)
        .options(joinedload(ServiceOrder.customer))
        .filter(ServiceOrder.customer_id == customer.id)
        .order_by(ServiceOrder.created_at.desc())
        .all()
    )

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
def get_order_stats(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
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
def get_order(order_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    order = db.query(ServiceOrder).filter(ServiceOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("", response_model=ServiceOrderResponse, status_code=201)
def create_order(data: ServiceOrderCreate, admin: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    order = ServiceOrder(**data.model_dump())
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.put("/{order_id}", response_model=ServiceOrderResponse)
def update_order(order_id: str, data: ServiceOrderUpdate, admin: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    order = db.query(ServiceOrder).filter(ServiceOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    old_status = order.status
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(order, key, value)
    db.commit()
    db.refresh(order)

    # 상태 변경 시 고객 알림
    if old_status != order.status and order.customer:
        notify_customer_by_email(
            db,
            email=order.customer.email,
            title=f"Order Status Updated: {order.status}",
            message=f"Your order for {order.turbo_brand} {order.turbo_model} has been updated to '{order.status}'.",
            type="order",
            reference_id=order.id,
            reference_type="order",
        )

    return order
