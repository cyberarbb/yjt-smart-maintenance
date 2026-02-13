"""알림 서비스 - 알림 생성 및 관리"""
from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.models.user import User


def create_notification(
    db: Session,
    user_id: str,
    title: str,
    message: str,
    type: str = "info",
    reference_id: str = None,
    reference_type: str = None,
) -> Notification:
    """단일 사용자에게 알림 생성"""
    notif = Notification(
        user_id=user_id,
        title=title,
        message=message,
        type=type,
        reference_id=reference_id,
        reference_type=reference_type,
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif


def notify_admins(
    db: Session,
    title: str,
    message: str,
    type: str = "info",
    reference_id: str = None,
    reference_type: str = None,
):
    """모든 관리자에게 알림 전송"""
    admins = db.query(User).filter(User.is_admin == True, User.is_active == True).all()
    for admin in admins:
        notif = Notification(
            user_id=admin.id,
            title=title,
            message=message,
            type=type,
            reference_id=reference_id,
            reference_type=reference_type,
        )
        db.add(notif)
    db.commit()


def notify_customer_by_email(
    db: Session,
    email: str,
    title: str,
    message: str,
    type: str = "info",
    reference_id: str = None,
    reference_type: str = None,
):
    """이메일로 고객 사용자를 찾아 알림 전송"""
    user = db.query(User).filter(User.email == email).first()
    if user:
        create_notification(db, user.id, title, message, type, reference_id, reference_type)


def check_low_stock_notification(
    db: Session,
    part_name: str,
    new_quantity: int,
    min_quantity: int,
    inventory_id: str,
):
    """재고 부족 시 관리자에게 알림"""
    if new_quantity <= min_quantity:
        notify_admins(
            db,
            title="Low Stock Alert",
            message=f"{part_name}: {new_quantity} units remaining (min: {min_quantity})",
            type="warning",
            reference_id=inventory_id,
            reference_type="inventory",
        )
