"""용진터보 실제 데이터 기반 시드 데이터"""
import random
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.part import Part
from app.models.inventory import Inventory
from app.models.customer import Customer
from app.models.service_order import ServiceOrder
from app.models.inquiry import Inquiry

PARTS_DATA = [
    # MAN NR Type 부품
    {"part_number": "MAN-NR29S-NR-001", "name": "Nozzle Ring NR29/S", "brand": "MAN", "turbo_model": "NR29/S", "category": "Nozzle Ring", "unit_price": 8500.00, "qty": 25},
    {"part_number": "MAN-NR29S-BJ-001", "name": "Journal Bearing NR29/S", "brand": "MAN", "turbo_model": "NR29/S", "category": "Bearing", "unit_price": 3200.00, "qty": 40},
    {"part_number": "MAN-NR29S-BT-001", "name": "Thrust Bearing NR29/S", "brand": "MAN", "turbo_model": "NR29/S", "category": "Bearing", "unit_price": 2800.00, "qty": 35},
    {"part_number": "MAN-NR29S-TB-001", "name": "Turbine Blade Set NR29/S", "brand": "MAN", "turbo_model": "NR29/S", "category": "Turbine Blade", "unit_price": 12000.00, "qty": 15},
    {"part_number": "MAN-NR29S-SL-001", "name": "Seal Ring NR29/S", "brand": "MAN", "turbo_model": "NR29/S", "category": "Seal", "unit_price": 850.00, "qty": 60},
    {"part_number": "MAN-NR29S-GK-001", "name": "Gasket Kit NR29/S", "brand": "MAN", "turbo_model": "NR29/S", "category": "Gasket", "unit_price": 450.00, "qty": 80},
    {"part_number": "MAN-NR34S-NR-001", "name": "Nozzle Ring NR34/S", "brand": "MAN", "turbo_model": "NR34/S", "category": "Nozzle Ring", "unit_price": 9500.00, "qty": 20},
    {"part_number": "MAN-NR34S-BJ-001", "name": "Journal Bearing NR34/S", "brand": "MAN", "turbo_model": "NR34/S", "category": "Bearing", "unit_price": 3800.00, "qty": 30},
    {"part_number": "MAN-NR34S-CW-001", "name": "Compressor Wheel NR34/S", "brand": "MAN", "turbo_model": "NR34/S", "category": "Compressor Wheel", "unit_price": 15000.00, "qty": 10},
    {"part_number": "MAN-NR34S-CT-001", "name": "Cartridge Assembly NR34/S", "brand": "MAN", "turbo_model": "NR34/S", "category": "Cartridge", "unit_price": 28000.00, "qty": 5},
    {"part_number": "MAN-NA40S-NR-001", "name": "Nozzle Ring NA40/S", "brand": "MAN", "turbo_model": "NA40/S", "category": "Nozzle Ring", "unit_price": 11000.00, "qty": 12},
    {"part_number": "MAN-NA40S-SH-001", "name": "Rotor Shaft NA40/S", "brand": "MAN", "turbo_model": "NA40/S", "category": "Shaft", "unit_price": 18000.00, "qty": 8},
    {"part_number": "MAN-TCA44-BJ-001", "name": "Journal Bearing TCA44", "brand": "MAN", "turbo_model": "TCA44", "category": "Bearing", "unit_price": 4200.00, "qty": 18},
    {"part_number": "MAN-TCA55-NR-001", "name": "Nozzle Ring TCA55", "brand": "MAN", "turbo_model": "TCA55", "category": "Nozzle Ring", "unit_price": 13500.00, "qty": 7},
    # KBB 부품
    {"part_number": "KBB-HPR3000-NR-001", "name": "Nozzle Ring HPR3000", "brand": "KBB", "turbo_model": "HPR3000", "category": "Nozzle Ring", "unit_price": 6500.00, "qty": 15},
    {"part_number": "KBB-HPR4000-BJ-001", "name": "Journal Bearing HPR4000", "brand": "KBB", "turbo_model": "HPR4000", "category": "Bearing", "unit_price": 2800.00, "qty": 22},
    {"part_number": "KBB-HPR5000-TB-001", "name": "Turbine Blade Set HPR5000", "brand": "KBB", "turbo_model": "HPR5000", "category": "Turbine Blade", "unit_price": 9800.00, "qty": 8},
    {"part_number": "KBB-ST27-NR-001", "name": "Nozzle Ring ST27", "brand": "KBB", "turbo_model": "ST27", "category": "Nozzle Ring", "unit_price": 7200.00, "qty": 14},
    {"part_number": "KBB-ST27-SL-001", "name": "Seal Ring ST27", "brand": "KBB", "turbo_model": "ST27", "category": "Seal", "unit_price": 680.00, "qty": 45},
    # MHI 부품
    {"part_number": "MHI-MET33-NR-001", "name": "Nozzle Ring MET33", "brand": "MHI", "turbo_model": "MET33", "category": "Nozzle Ring", "unit_price": 7800.00, "qty": 10},
    {"part_number": "MHI-MET42-BJ-001", "name": "Journal Bearing MET42", "brand": "MHI", "turbo_model": "MET42", "category": "Bearing", "unit_price": 3500.00, "qty": 16},
    {"part_number": "MHI-MET53-CW-001", "name": "Compressor Wheel MET53", "brand": "MHI", "turbo_model": "MET53", "category": "Compressor Wheel", "unit_price": 14500.00, "qty": 6},
    {"part_number": "MHI-MET66-TB-001", "name": "Turbine Blade Set MET66", "brand": "MHI", "turbo_model": "MET66", "category": "Turbine Blade", "unit_price": 16000.00, "qty": 4},
    # ABB 부품
    {"part_number": "ABB-VTR214-BJ-001", "name": "Journal Bearing VTR214", "brand": "ABB", "turbo_model": "VTR214", "category": "Bearing", "unit_price": 3100.00, "qty": 20},
    {"part_number": "ABB-VTR254-NR-001", "name": "Nozzle Ring VTR254", "brand": "ABB", "turbo_model": "VTR254", "category": "Nozzle Ring", "unit_price": 8200.00, "qty": 11},
    {"part_number": "ABB-A175-SL-001", "name": "Seal Ring A175-L", "brand": "ABB", "turbo_model": "A175-L", "category": "Seal", "unit_price": 920.00, "qty": 30},
    {"part_number": "ABB-TPL73-CS-001", "name": "Casing TPL73", "brand": "ABB", "turbo_model": "TPL73", "category": "Casing", "unit_price": 22000.00, "qty": 3},
    # Napier 부품
    {"part_number": "NAP-NA295-BJ-001", "name": "Journal Bearing NA295", "brand": "Napier", "turbo_model": "NA295", "category": "Bearing", "unit_price": 2900.00, "qty": 12},
    {"part_number": "NAP-NA357-NR-001", "name": "Nozzle Ring NA357", "brand": "Napier", "turbo_model": "NA357", "category": "Nozzle Ring", "unit_price": 7500.00, "qty": 9},
    {"part_number": "NAP-NA357-FT-001", "name": "Filter Assembly NA357", "brand": "Napier", "turbo_model": "NA357", "category": "Filter", "unit_price": 1200.00, "qty": 25},
]

CUSTOMERS_DATA = [
    {"company_name": "Maersk Line", "contact_name": "Lars Jensen", "email": "lars.jensen@maersk.com", "phone": "+45-3363-3363", "country": "Denmark", "vessel_type": "Container Ship"},
    {"company_name": "MSC Mediterranean", "contact_name": "Marco Rossi", "email": "marco.rossi@msc.com", "phone": "+41-22-703-8888", "country": "Switzerland", "vessel_type": "Container Ship"},
    {"company_name": "HMM Co., Ltd.", "contact_name": "김성호", "email": "sh.kim@hmm21.com", "phone": "+82-2-3706-5500", "country": "South Korea", "vessel_type": "Container Ship"},
    {"company_name": "Pan Ocean Co.", "contact_name": "이정우", "email": "jw.lee@panocean.com", "phone": "+82-2-316-5100", "country": "South Korea", "vessel_type": "Bulk Carrier"},
    {"company_name": "COSCO Shipping", "contact_name": "Wang Lei", "email": "wang.lei@cosco.com", "phone": "+86-21-6596-6105", "country": "China", "vessel_type": "Container Ship"},
    {"company_name": "NYK Line", "contact_name": "Tanaka Yuki", "email": "y.tanaka@nyk.com", "phone": "+81-3-3284-5151", "country": "Japan", "vessel_type": "Tanker"},
    {"company_name": "Torm A/S", "contact_name": "Henrik Nielsen", "email": "h.nielsen@torm.com", "phone": "+45-3917-9200", "country": "Denmark", "vessel_type": "Tanker"},
    {"company_name": "Petrobras", "contact_name": "Carlos Silva", "email": "c.silva@petrobras.com.br", "phone": "+55-21-3224-4477", "country": "Brazil", "vessel_type": "FPSO"},
    {"company_name": "Singapore Power Plant", "contact_name": "Lim Wei", "email": "w.lim@sppower.sg", "phone": "+65-6835-8888", "country": "Singapore", "vessel_type": None},
    {"company_name": "Evergreen Marine", "contact_name": "Chen Ming", "email": "m.chen@evergreen.com.tw", "phone": "+886-2-2505-7766", "country": "Taiwan", "vessel_type": "Container Ship"},
]

ORDERS_DATA = [
    {"customer_idx": 0, "order_type": "Overhaul", "turbo_brand": "MAN", "turbo_model": "NR29/S", "vessel_name": "Maersk Mc-Kinney", "status": "In Progress", "description": "Full overhaul of turbocharger #1, vibration detected"},
    {"customer_idx": 2, "order_type": "Part Supply", "turbo_brand": "MAN", "turbo_model": "NR34/S", "vessel_name": "HMM Algeciras", "status": "Pending", "description": "Nozzle ring and bearing replacement parts required"},
    {"customer_idx": 3, "order_type": "Overhaul", "turbo_brand": "KBB", "turbo_model": "HPR4000", "vessel_name": "Pan Hope", "status": "Completed", "description": "Standard overhaul completed, all tests passed"},
    {"customer_idx": 4, "order_type": "Technical Service", "turbo_brand": "MHI", "turbo_model": "MET42", "vessel_name": "COSCO Faith", "status": "In Progress", "description": "On-site technical inspection for exhaust temperature issue"},
    {"customer_idx": 5, "order_type": "Overhaul", "turbo_brand": "ABB", "turbo_model": "VTR254", "vessel_name": "NYK Vega", "status": "Pending", "description": "Cartridge overhaul requested after 24,000 running hours"},
    {"customer_idx": 7, "order_type": "Part Supply", "turbo_brand": "MAN", "turbo_model": "NA40/S", "vessel_name": "P-77 FPSO", "status": "In Progress", "description": "Emergency spare parts for offshore platform turbocharger"},
    {"customer_idx": 1, "order_type": "Overhaul", "turbo_brand": "MAN", "turbo_model": "NR29/S", "vessel_name": "MSC Gülsün", "status": "Completed", "description": "Routine overhaul with blade replacement"},
    {"customer_idx": 8, "order_type": "Technical Service", "turbo_brand": "KBB", "turbo_model": "ST27", "vessel_name": None, "status": "Pending", "description": "Power plant turbocharger performance optimization"},
    {"customer_idx": 9, "order_type": "Part Supply", "turbo_brand": "Napier", "turbo_model": "NA357", "vessel_name": "Ever Given", "status": "Completed", "description": "Filter and bearing replacement parts"},
    {"customer_idx": 6, "order_type": "Overhaul", "turbo_brand": "MHI", "turbo_model": "MET53", "vessel_name": "Torm Laura", "status": "In Progress", "description": "Emergency overhaul - compressor wheel damage detected"},
]


def seed_database():
    """데이터베이스에 시드 데이터 투입"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 기존 데이터 확인
        if db.query(Part).count() > 0:
            print("Database already has data. Skipping seed.")
            return

        print("Seeding database...")

        # Parts & Inventory
        for p in PARTS_DATA:
            qty = p.pop("qty")
            part = Part(**p)
            db.add(part)
            db.flush()

            inv = Inventory(
                part_id=part.id,
                quantity=qty,
                min_quantity=max(3, qty // 5),
                warehouse="Busan HQ",
            )
            db.add(inv)

        # Customers
        customers = []
        for c in CUSTOMERS_DATA:
            customer = Customer(**c)
            db.add(customer)
            db.flush()
            customers.append(customer)

        # Service Orders
        for o in ORDERS_DATA:
            idx = o.pop("customer_idx")
            order = ServiceOrder(customer_id=customers[idx].id, **o)
            db.add(order)

        # Sample Inquiry
        inquiry = Inquiry(
            customer_id=customers[2].id,
            subject="MAN NR29/S 오버홀 견적 요청",
            message="HMM Algeciras호의 터보차저 #2 오버홀 견적을 요청합니다. 현재 운전시간 18,000시간입니다.",
            contact_email="sh.kim@hmm21.com",
        )
        db.add(inquiry)

        db.commit()
        print(f"Seeded: {len(PARTS_DATA)} parts, {len(CUSTOMERS_DATA)} customers, {len(ORDERS_DATA)} orders")

    except Exception as e:
        db.rollback()
        print(f"Seed error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
