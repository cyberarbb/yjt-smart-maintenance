"""운전시간 시드 데이터 - 30일분 일일 운전시간"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import random
from datetime import date, timedelta
from app.database import SessionLocal
from app.models.user import User  # noqa: must import for FK resolution
from app.models.vessel import Vessel  # noqa: must import before Equipment
from app.models.equipment import Equipment
from app.models.running_hours import RunningHours


def seed_running_hours():
    """30일분 운전시간 시드 데이터"""
    db = SessionLocal()

    try:
        if db.query(RunningHours).count() > 0:
            print("Running hours already seeded. Skipping.")
            return

        # 주기관, 발전기, 터보차저만 운전시간 기록 (나머지는 생략)
        target_categories = {"Main Engine", "Generator", "Turbocharger"}
        equipment_list = (
            db.query(Equipment)
            .filter(Equipment.category.in_(target_categories), Equipment.is_active == True)
            .all()
        )

        if not equipment_list:
            print("No target equipment found. Run seed_equipment first.")
            return

        print(f"Seeding running hours for {len(equipment_list)} equipment items...")
        total_records = 0
        today = date.today()

        for eq in equipment_list:
            # 30일 전부터 시작
            base_hours = eq.current_running_hours - 30 * 21  # 대략 30일 x 21시간
            if base_hours < 0:
                base_hours = 0

            cumulative = base_hours

            for day_offset in range(30, 0, -1):
                record_date = today - timedelta(days=day_offset)

                # 일일 운전 시간 (18~23시간 랜덤, 가끔 0 = 정비일)
                if random.random() < 0.05:  # 5% 확률로 정비일
                    daily = 0.0
                    note = "Maintenance day"
                elif eq.category == "Emergency Generator":
                    daily = round(random.uniform(0.5, 2.0), 1)  # 비상발전기는 적게
                    note = None
                else:
                    daily = round(random.uniform(18.0, 23.0), 1)
                    note = None

                cumulative += daily

                record = RunningHours(
                    equipment_id=eq.id,
                    recorded_date=record_date,
                    daily_hours=daily,
                    total_hours=round(cumulative, 1),
                    note=note,
                )
                db.add(record)
                total_records += 1

            # Equipment의 current_running_hours 업데이트
            eq.current_running_hours = round(cumulative, 1)

            # 상태 업데이트
            if eq.overhaul_interval_hours:
                ratio = cumulative / eq.overhaul_interval_hours
                if ratio >= 1.0:
                    eq.status = "Critical"
                elif ratio >= 0.85:
                    eq.status = "Warning"

        db.commit()
        print(f"Seeded: {total_records} running hours records for {len(equipment_list)} equipment items")

    except Exception as e:
        db.rollback()
        print(f"Running hours seed error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_running_hours()
