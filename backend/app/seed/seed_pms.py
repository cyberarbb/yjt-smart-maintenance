"""PMS 시드 데이터 - 정비 계획 + 작업 지시서"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import random
from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models.user import User
from app.models.vessel import Vessel
from app.models.equipment import Equipment
from app.models.maintenance_plan import MaintenancePlan
from app.models.work_order import WorkOrder


def seed_pms():
    """PMS 시드 데이터"""
    db = SessionLocal()

    try:
        if db.query(MaintenancePlan).count() > 0:
            print("PMS already seeded. Skipping.")
            return

        vessels = db.query(Vessel).all()
        if not vessels:
            print("No vessels found. Run vessel seeds first.")
            return

        print("Seeding PMS data...")
        plan_count = 0
        wo_count = 0
        now = datetime.utcnow()

        for vessel in vessels:
            equipment = db.query(Equipment).filter(
                Equipment.vessel_id == vessel.id,
                Equipment.is_active == True,
            ).all()

            for eq in equipment:
                # 장비 카테고리별 정비 계획 생성
                plans_data = _get_plans_for_category(eq.category)

                for plan_data in plans_data:
                    last_done = now - timedelta(days=random.randint(30, 300))
                    if plan_data["interval_type"] == "Calendar":
                        interval_months = plan_data["interval_value"]
                        next_due = last_done + timedelta(days=int(interval_months * 30))
                    else:
                        next_due = now + timedelta(days=random.randint(-30, 180))

                    plan = MaintenancePlan(
                        equipment_id=eq.id,
                        vessel_id=vessel.id,
                        title=plan_data["title"],
                        description=plan_data.get("description"),
                        interval_type=plan_data["interval_type"],
                        interval_value=plan_data["interval_value"],
                        interval_unit=plan_data["interval_unit"],
                        priority=plan_data["priority"],
                        is_class_related=plan_data.get("class_related", False),
                        estimated_hours=plan_data.get("estimated_hours"),
                        last_done_date=last_done,
                        next_due_date=next_due,
                    )
                    db.add(plan)
                    db.flush()
                    plan_count += 1

                    # 작업 지시서 1-2개 생성
                    for i in range(random.randint(1, 2)):
                        planned = now + timedelta(days=random.randint(-60, 60))
                        due = planned + timedelta(days=random.randint(7, 30))

                        status_choices = ["Planned", "Planned", "InProgress", "Completed", "Completed"]
                        status = random.choice(status_choices)

                        wo = WorkOrder(
                            maintenance_plan_id=plan.id,
                            equipment_id=eq.id,
                            vessel_id=vessel.id,
                            title=f"{plan_data['title']} - {eq.equipment_code}",
                            description=f"Scheduled {plan_data['title'].lower()} for {eq.name}",
                            status=status,
                            priority=plan_data["priority"],
                            planned_date=planned,
                            due_date=due,
                            started_date=planned + timedelta(days=1) if status in ("InProgress", "Completed") else None,
                            completed_date=planned + timedelta(days=random.randint(2, 7)) if status == "Completed" else None,
                            is_class_related=plan_data.get("class_related", False),
                            actual_hours=plan_data.get("estimated_hours", 4) * random.uniform(0.8, 1.3) if status == "Completed" else None,
                        )
                        db.add(wo)
                        wo_count += 1

        db.commit()
        print(f"Seeded: {plan_count} maintenance plans, {wo_count} work orders")

    except Exception as e:
        db.rollback()
        print(f"PMS seed error: {e}")
        raise
    finally:
        db.close()


def _get_plans_for_category(category: str) -> list[dict]:
    """카테고리별 정비 계획 템플릿"""
    plans = {
        "Main Engine": [
            {"title": "Main Engine Overhaul", "interval_type": "RunningHours", "interval_value": 24000, "interval_unit": "hours", "priority": "Critical", "class_related": True, "estimated_hours": 120},
            {"title": "Cylinder Liner Inspection", "interval_type": "Calendar", "interval_value": 6, "interval_unit": "months", "priority": "High", "estimated_hours": 8},
        ],
        "Turbocharger": [
            {"title": "Turbocharger Overhaul", "interval_type": "RunningHours", "interval_value": 24000, "interval_unit": "hours", "priority": "Critical", "class_related": True, "estimated_hours": 48},
            {"title": "TC Bearing Inspection", "interval_type": "Calendar", "interval_value": 12, "interval_unit": "months", "priority": "High", "estimated_hours": 6},
        ],
        "Generator": [
            {"title": "Generator Overhaul", "interval_type": "RunningHours", "interval_value": 16000, "interval_unit": "hours", "priority": "High", "estimated_hours": 72},
            {"title": "Generator Valve Adjustment", "interval_type": "Calendar", "interval_value": 3, "interval_unit": "months", "priority": "Medium", "estimated_hours": 4},
        ],
        "Boiler": [
            {"title": "Boiler Tube Inspection", "interval_type": "Calendar", "interval_value": 12, "interval_unit": "months", "priority": "High", "class_related": True, "estimated_hours": 16},
        ],
        "Compressor": [
            {"title": "Air Compressor Valve Overhaul", "interval_type": "RunningHours", "interval_value": 12000, "interval_unit": "hours", "priority": "Medium", "estimated_hours": 8},
        ],
        "Steering Gear": [
            {"title": "Steering Gear Inspection", "interval_type": "Calendar", "interval_value": 6, "interval_unit": "months", "priority": "High", "class_related": True, "estimated_hours": 4},
        ],
        "Emergency Generator": [
            {"title": "Emergency Generator Test", "interval_type": "Calendar", "interval_value": 1, "interval_unit": "months", "priority": "Critical", "class_related": True, "estimated_hours": 2},
        ],
    }
    return plans.get(category, [
        {"title": f"{category} Routine Maintenance", "interval_type": "Calendar", "interval_value": 6, "interval_unit": "months", "priority": "Medium", "estimated_hours": 4}
    ])


if __name__ == "__main__":
    seed_pms()
