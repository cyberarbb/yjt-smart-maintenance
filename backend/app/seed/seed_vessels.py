"""선박 시드 데이터 - 기존 DB에 선박 + 역할 추가"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from app.database import SessionLocal, engine, Base
from app.models.vessel import Vessel
from app.models.user import User

VESSELS_DATA = [
    {
        "name": "HMM Algeciras",
        "imo_number": "9863297",
        "vessel_type": "Container Ship",
        "flag": "Panama",
        "class_society": "KR",
        "gross_tonnage": 228283,
        "build_year": 2020,
        "owner_company": "HMM Co., Ltd.",
        "manager_company": "HMM Ship Management",
        "description": "24,000 TEU class, world's largest container ship series",
    },
    {
        "name": "Maersk Mc-Kinney",
        "imo_number": "9632179",
        "vessel_type": "Container Ship",
        "flag": "Denmark",
        "class_society": "DNV",
        "gross_tonnage": 194849,
        "build_year": 2013,
        "owner_company": "Maersk Line",
        "manager_company": "Maersk Ship Management",
        "description": "Triple-E class, MAN B&W 8S80ME-C9.2 engine with NR29/S turbocharger",
    },
    {
        "name": "Pan Hope",
        "imo_number": "9458700",
        "vessel_type": "Bulk Carrier",
        "flag": "South Korea",
        "class_society": "KR",
        "gross_tonnage": 93000,
        "build_year": 2012,
        "owner_company": "Pan Ocean Co.",
        "manager_company": "Pan Ocean Ship Management",
        "description": "Capesize bulk carrier, KBB HPR4000 turbocharger",
    },
    {
        "name": "NYK Vega",
        "imo_number": "9337680",
        "vessel_type": "Tanker",
        "flag": "Japan",
        "class_society": "NK",
        "gross_tonnage": 160000,
        "build_year": 2008,
        "owner_company": "NYK Line",
        "manager_company": "NYK Shipmanagement",
        "description": "VLCC, ABB VTR254 turbocharger, 24,000 running hours overhaul needed",
    },
    {
        "name": "COSCO Faith",
        "imo_number": "9785610",
        "vessel_type": "Container Ship",
        "flag": "China",
        "class_society": "CCS",
        "gross_tonnage": 199000,
        "build_year": 2018,
        "owner_company": "COSCO Shipping",
        "manager_company": "COSCO Ship Management",
        "description": "20,000 TEU class, MHI MET42 turbocharger",
    },
]


def seed_vessels():
    """선박 시드 데이터 투입"""
    db = SessionLocal()

    try:
        # 이미 선박이 있으면 스킵
        if db.query(Vessel).count() > 0:
            print("Vessels already seeded. Skipping.")
            return

        print("Seeding vessels...")

        for v_data in VESSELS_DATA:
            vessel = Vessel(**v_data)
            db.add(vessel)

        db.flush()

        # admin 유저에 role='admin' 설정
        admin_users = db.query(User).filter(User.is_admin == True).all()
        for u in admin_users:
            if not u.role or u.role == "customer":
                u.role = "admin"

        db.commit()
        print(f"Seeded: {len(VESSELS_DATA)} vessels, {len(admin_users)} admin users updated")

    except Exception as e:
        db.rollback()
        print(f"Seed error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_vessels()
