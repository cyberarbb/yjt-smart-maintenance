"""장비 시드 데이터 - 각 선박에 장비 계층 구조 추가"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from app.database import SessionLocal
from app.models.vessel import Vessel
from app.models.equipment import Equipment


def _make_equipment(vessel_id: str, parent_id=None, **kwargs):
    """장비 dict 생성 헬퍼"""
    return Equipment(vessel_id=vessel_id, parent_id=parent_id, **kwargs)


def seed_equipment():
    """장비 시드 데이터 투입"""
    db = SessionLocal()

    try:
        # 이미 장비가 있으면 스킵
        if db.query(Equipment).count() > 0:
            print("Equipment already seeded. Skipping.")
            return

        vessels = db.query(Vessel).order_by(Vessel.name).all()
        if not vessels:
            print("No vessels found. Run seed_vessels first.")
            return

        print("Seeding equipment...")
        total = 0

        for vessel in vessels:
            vid = vessel.id
            vname = vessel.name

            # ── 주기관 (Main Engine) ──
            me = _make_equipment(
                vid,
                equipment_code="ME-001",
                name="Main Engine",
                category="Main Engine",
                maker="MAN Energy Solutions" if "HMM" in vname or "Maersk" in vname or "COSCO" in vname else "Hyundai Heavy Industries",
                model="MAN B&W 8S80ME-C9.2" if "Maersk" in vname else "MAN B&W 11G95ME-C10.5" if "HMM" in vname else "MAN B&W 6S60ME-C10.5",
                rated_power="68,640 kW" if "HMM" in vname else "55,440 kW",
                rated_rpm="80 RPM",
                current_running_hours=8500 if "HMM" in vname else 22000 if "Maersk" in vname else 15000,
                overhaul_interval_hours=24000,
                status="Normal",
                sort_order=1,
                description=f"Main propulsion engine for {vname}",
            )
            db.add(me)
            db.flush()

            # ── 터보차저 (Main Engine 하위) ──
            tc_models = {
                "HMM": ("MAN", "NR29/S", 2),
                "Maersk": ("MAN", "NR29/S", 2),
                "Pan Hope": ("KBB", "HPR4000", 1),
                "NYK": ("ABB", "VTR254", 1),
                "COSCO": ("MHI", "MET42", 2),
            }

            tc_key = next((k for k in tc_models if k in vname), "HMM")
            tc_maker, tc_model, tc_count = tc_models[tc_key]

            for i in range(1, tc_count + 1):
                tc = _make_equipment(
                    vid,
                    parent_id=me.id,
                    equipment_code=f"TC-{i:03d}",
                    name=f"Turbocharger #{i}",
                    category="Turbocharger",
                    maker=tc_maker,
                    model=tc_model,
                    current_running_hours=me.current_running_hours,
                    overhaul_interval_hours=24000,
                    status="Warning" if me.current_running_hours > 20000 else "Normal",
                    sort_order=10 + i,
                    description=f"Exhaust gas turbocharger for {vname} main engine",
                )
                db.add(tc)
                total += 1

            # ── 연료분사펌프 (Main Engine 하위) ──
            fip = _make_equipment(
                vid,
                parent_id=me.id,
                equipment_code="FIP-001",
                name="Fuel Injection Pump",
                category="Fuel System",
                maker="MAN Energy Solutions",
                current_running_hours=me.current_running_hours,
                overhaul_interval_hours=12000,
                status="Normal",
                sort_order=20,
            )
            db.add(fip)
            total += 2  # ME + FIP

            # ── 발전기 (Generator) x2 ──
            for i in range(1, 3):
                gen = _make_equipment(
                    vid,
                    equipment_code=f"GE-{i:03d}",
                    name=f"Diesel Generator #{i}",
                    category="Generator",
                    maker="Hyundai Heavy Industries" if i == 1 else "STX Engine",
                    model=f"HiMSEN {9 + i}H32/40" if i == 1 else "MAN 6L21/31",
                    rated_power=f"{2500 + i * 500} kW",
                    rated_rpm="720 RPM",
                    current_running_hours=18000 + i * 1000,
                    overhaul_interval_hours=16000,
                    status="Warning" if (18000 + i * 1000) > 16000 else "Normal",
                    sort_order=30 + i,
                    description=f"Auxiliary diesel generator #{i}",
                )
                db.add(gen)
                total += 1

            # ── 보일러 (Boiler) ──
            boiler = _make_equipment(
                vid,
                equipment_code="BL-001",
                name="Auxiliary Boiler",
                category="Boiler",
                maker="Kangrim Heavy Industries",
                model="KRH-500",
                rated_power="5,000 kg/h steam",
                current_running_hours=12000,
                overhaul_interval_hours=20000,
                status="Normal",
                sort_order=40,
            )
            db.add(boiler)
            total += 1

            # ── 공기압축기 (Compressor) ──
            comp = _make_equipment(
                vid,
                equipment_code="AC-001",
                name="Main Air Compressor",
                category="Compressor",
                maker="Sperre",
                model="HV2/200",
                rated_power="30 bar",
                current_running_hours=10000,
                overhaul_interval_hours=12000,
                status="Normal",
                sort_order=50,
            )
            db.add(comp)
            total += 1

            # ── 조타기 (Steering Gear) ──
            steer = _make_equipment(
                vid,
                equipment_code="SG-001",
                name="Steering Gear",
                category="Steering Gear",
                maker="Rolls-Royce Marine",
                model="Rotary Vane",
                current_running_hours=me.current_running_hours,
                overhaul_interval_hours=30000,
                status="Normal",
                sort_order=60,
            )
            db.add(steer)
            total += 1

            # ── 비상발전기 (Emergency Generator) ──
            egen = _make_equipment(
                vid,
                equipment_code="EG-001",
                name="Emergency Generator",
                category="Emergency Generator",
                maker="Caterpillar",
                model="CAT C9.3",
                rated_power="500 kW",
                current_running_hours=500,
                overhaul_interval_hours=8000,
                status="Normal",
                sort_order=70,
            )
            db.add(egen)
            total += 1

            print(f"  {vname}: equipment hierarchy created")

        db.commit()
        print(f"Seeded: {total} equipment items across {len(vessels)} vessels")

    except Exception as e:
        db.rollback()
        print(f"Equipment seed error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_equipment()
