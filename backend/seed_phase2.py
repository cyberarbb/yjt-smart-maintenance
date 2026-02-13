import uuid
import random
from datetime import datetime, timedelta

from app.database import SessionLocal
from app.models.part import Part
from app.models.inventory import Inventory
from app.models.customer import Customer
from app.models.service_order import ServiceOrder
from app.models.inquiry import Inquiry
from app.models.user import User
from app.models.notification import Notification

db = SessionLocal()

# Clean existing data (order matters for foreign keys)
print("Cleaning existing data...")
db.query(Notification).delete()
db.query(Inquiry).delete()
db.query(ServiceOrder).delete()
db.query(Inventory).delete()
db.query(Part).delete()
db.query(Customer).delete()
db.commit()
print("All existing data cleared.")
print()

# ========== CUSTOMERS ==========
customers_data = [
    ("Hyundai Merchant Marine", "Kim Sung-ho", "kim.sh@hmm21.com", "+82-2-3770-6114", "South Korea", "Container Ship"),
    ("Maersk Line", "Lars Jensen", "l.jensen@maersk.com", "+45-3363-3363", "Denmark", "Container Ship"),
    ("NYK Line", "Tanaka Kenji", "k.tanaka@nyk.com", "+81-3-3284-5151", "Japan", "Bulk Carrier"),
    ("Evergreen Marine", "Chen Wei-lin", "wl.chen@evergreen.com.tw", "+886-2-2505-7766", "Taiwan", "Container Ship"),
    ("COSCO Shipping", "Wang Lei", "wang.lei@cosco.com", "+86-21-6596-6105", "China", "Tanker"),
    ("Pacific Basin Shipping", "Mark Harris", "m.harris@pacificbasin.com", "+852-2233-7000", "Hong Kong", "Bulk Carrier"),
    ("Oldendorff Carriers", "Thomas Mueller", "t.mueller@oldendorff.com", "+49-451-1500-0", "Germany", "Bulk Carrier"),
    ("Anglo-Eastern Ship Mgmt", "Rajesh Sharma", "r.sharma@angloeastern.com", "+91-22-2830-6611", "India", "Tanker"),
    ("Stena Bulk", "Erik Lindqvist", "e.lindqvist@stenabulk.com", "+46-31-855-000", "Sweden", "Tanker"),
    ("Mitsui O.S.K. Lines", "Yamamoto Hiro", "h.yamamoto@mol.co.jp", "+81-3-3587-7111", "Japan", "LNG Carrier"),
]

customer_ids = []
for c in customers_data:
    cid = str(uuid.uuid4())
    customer_ids.append(cid)
    db.add(Customer(id=cid, company_name=c[0], contact_name=c[1], email=c[2], phone=c[3], country=c[4], vessel_type=c[5]))

db.commit()
print(f"Added {len(customers_data)} customers")

# ========== PARTS + INVENTORY ==========
parts_data = [
    ("MAN-NR-001", "MAN TCA66 Nozzle Ring", "MAN", "TCA66", "Nozzle Ring", "Precision-cast nozzle ring for MAN TCA66 turbocharger", 8500.00, 12, 5),
    ("MAN-BRG-002", "MAN TCA55 Main Bearing", "MAN", "TCA55", "Bearing", "Journal bearing assembly for TCA55 series", 3200.00, 20, 8),
    ("MAN-TB-003", "MAN NA57 Turbine Blade Set", "MAN", "NA57", "Turbine Blade", "Inconel turbine blade set, 24 blades per set", 15000.00, 6, 3),
    ("MHI-CW-001", "MHI MET42 Compressor Wheel", "MHI", "MET42", "Compressor Wheel", "Aluminum alloy compressor wheel for MET42", 4500.00, 15, 5),
    ("MHI-SL-002", "MHI MET33 Labyrinth Seal", "MHI", "MET33", "Seal", "Labyrinth seal kit for gas side", 1200.00, 30, 10),
    ("MHI-SH-003", "MHI MET66 Rotor Shaft", "MHI", "MET66", "Shaft", "Nitrided rotor shaft for MET66 turbo", 12000.00, 4, 2),
    ("KBB-GK-001", "KBB HPR4000 Gasket Kit", "KBB", "HPR4000", "Gasket", "Complete gasket set for HPR4000 overhaul", 850.00, 25, 10),
    ("KBB-CS-002", "KBB ST27 Casing Half", "KBB", "ST27", "Casing", "Turbine side casing (upper half)", 22000.00, 3, 2),
    ("KBB-FT-003", "KBB HPR3000 Air Filter", "KBB", "HPR3000", "Filter", "Inlet air filter element", 320.00, 40, 15),
    ("ABB-CT-001", "ABB A175 Cartridge Assembly", "ABB", "A175", "Cartridge", "Complete CHRA for A175 turbocharger", 18000.00, 5, 3),
    ("ABB-NR-002", "ABB VTR564 Nozzle Ring", "ABB", "VTR564", "Nozzle Ring", "Variable geometry nozzle ring", 9500.00, 8, 4),
    ("ABB-BRG-003", "ABB TPL77 Thrust Bearing", "ABB", "TPL77", "Bearing", "Thrust bearing pad set for TPL77", 2800.00, 18, 6),
    ("NAP-TB-001", "Napier NA357 Turbine Blade", "Napier", "NA357", "Turbine Blade", "Single crystal turbine blade for NA357", 6500.00, 10, 4),
    ("NAP-SL-002", "Napier NA295 Piston Ring Seal", "Napier", "NA295", "Seal", "Piston ring seal set", 780.00, 2, 5),
    ("MAN-FT-004", "MAN TCR22 Oil Filter", "MAN", "TCR22", "Filter", "Lube oil filter for TCR22", 180.00, 50, 20),
    ("MHI-GK-004", "MHI MET42 Gasket Set", "MHI", "MET42", "Gasket", "Full overhaul gasket set", 920.00, 22, 8),
    ("ABB-SH-004", "ABB A170 Rotor Shaft", "ABB", "A170", "Shaft", "High-speed rotor shaft A170", 11500.00, 3, 2),
    ("KBB-CW-004", "KBB HPR5000 Compressor Wheel", "KBB", "HPR5000", "Compressor Wheel", "Titanium compressor wheel", 7800.00, 7, 3),
]

part_ids = []
for p in parts_data:
    pid = str(uuid.uuid4())
    part_ids.append(pid)
    db.add(Part(id=pid, part_number=p[0], name=p[1], brand=p[2], turbo_model=p[3], category=p[4], description=p[5], unit_price=p[6]))
    db.add(Inventory(id=str(uuid.uuid4()), part_id=pid, quantity=p[7], min_quantity=p[8], warehouse="Busan HQ"))

db.commit()
print(f"Added {len(parts_data)} parts with inventory")

# ========== SERVICE ORDERS ==========
order_types = ["Overhaul", "Part Supply", "Technical Service"]
statuses = ["Pending", "In Progress", "Completed", "Cancelled"]
brands = ["MAN", "MHI", "KBB", "ABB", "Napier"]
models_map = {
    "MAN": ["TCA66", "TCA55", "NA57", "TCR22"],
    "MHI": ["MET42", "MET33", "MET66"],
    "KBB": ["HPR4000", "ST27", "HPR3000", "HPR5000"],
    "ABB": ["A175", "VTR564", "TPL77", "A170"],
    "Napier": ["NA357", "NA295"],
}
vessel_names = [
    "MV Pacific Star", "MV Hyundai Fortune", "MV Ever Given", "MV COSCO Galaxy",
    "MV Stena Superior", "MV MOL Triumph", "MV Oldendorff Hansa", "MV NYK Vega",
    "MV Maersk Alabama", "MV Pacific Venture", "MV Global Spirit", "MV Ocean Pioneer",
    "MV Eastern Dream", "MV Nordic Queen", "MV Asia Progress",
]

descriptions = {
    "Overhaul": [
        "Complete turbocharger overhaul - 20000 hrs service interval",
        "Emergency overhaul due to abnormal vibration detected",
        "Scheduled major overhaul per class survey requirement",
        "Post-damage overhaul after bearing failure incident",
    ],
    "Part Supply": [
        "Urgent spare parts required for scheduled dry-dock",
        "Stock replenishment order for warehouse inventory",
        "Parts required for onboard maintenance by crew",
        "Pre-delivery spare parts package for new build vessel",
    ],
    "Technical Service": [
        "On-site technical service for turbo balancing",
        "Remote diagnostic support for performance degradation",
        "Vibration analysis and alignment check requested",
        "Commissioning support for newly installed turbocharger",
    ],
}

for i in range(20):
    brand = random.choice(brands)
    model = random.choice(models_map[brand])
    otype = random.choice(order_types)
    status = random.choice(statuses)
    desc = random.choice(descriptions[otype])
    days_ago = random.randint(0, 180)
    created = datetime.utcnow() - timedelta(days=days_ago)

    db.add(ServiceOrder(
        id=str(uuid.uuid4()),
        customer_id=random.choice(customer_ids),
        order_type=otype,
        turbo_brand=brand,
        turbo_model=model,
        vessel_name=random.choice(vessel_names),
        status=status,
        description=desc,
        created_at=created,
        updated_at=created + timedelta(days=random.randint(0, 10)),
    ))

db.commit()
print("Added 20 service orders")

# ========== INQUIRIES ==========
inquiry_data = [
    ("Request for turbocharger overhaul quotation",
     "We would like to request a quotation for a complete turbocharger overhaul. The unit has been running for approximately 18,000 hours and is due for scheduled maintenance."),
    ("Availability of MAN TCA66 spare parts",
     "Please advise on the availability and lead time for MAN TCA66 nozzle ring and bearing set. We need them delivered to Busan port within 2 weeks."),
    ("Technical question about MHI MET42",
     "We have been experiencing a slight drop in turbocharger performance on MHI MET42. Could your technical team provide remote diagnostic support?"),
    ("Emergency repair service needed",
     "Our vessel is currently at Busan port and requires emergency repair service for the turbocharger. Abnormal noise was detected during the last voyage."),
    ("Warranty claim for bearing",
     "The bearing supplied under our last PO failed after only 3,000 operating hours. We would like to file a warranty claim."),
    ("Annual maintenance contract inquiry",
     "We are interested in establishing an annual maintenance contract covering 5 vessels in our fleet. Please provide available service packages."),
    ("KBB HPR4000 exchange program",
     "Could you provide details about the exchange program for KBB HPR4000 turbochargers? We have 3 units that need refurbishment."),
    ("ABB A175 cartridge delivery update",
     "We placed an order for ABB A175 cartridge assembly 3 weeks ago. Could you provide an update on the expected delivery date?"),
    ("On-site service engineer in Singapore",
     "We need an on-site service engineer in Singapore for turbocharger alignment and commissioning work scheduled for next month."),
    ("Bulk order for Napier spare parts",
     "We are looking to place a bulk order for Napier spare parts covering our fleet of 8 vessels. Please advise on volume discounts available."),
    ("Technical data sheet request",
     "Please send us the complete technical data sheet and installation manual for the MAN TCR22 turbocharger series."),
    ("Compressor wheel balancing service",
     "We need compressor wheel dynamic balancing service. The wheel was recently repaired and requires balancing before reinstallation."),
]

for i, (subj, msg) in enumerate(inquiry_data):
    cust_idx = i % len(customer_ids)
    days_ago = random.randint(1, 90)
    resolved = i < 5  # first 5 resolved
    response = "Thank you for your inquiry. We have reviewed your request and our engineering team will contact you within 24 hours with a detailed proposal." if resolved else None

    db.add(Inquiry(
        id=str(uuid.uuid4()),
        customer_id=customer_ids[cust_idx],
        subject=subj,
        message=msg,
        contact_email=customers_data[cust_idx][2],
        is_resolved=resolved,
        response=response,
        created_at=datetime.utcnow() - timedelta(days=days_ago),
    ))

db.commit()
print("Added 12 inquiries")

# ========== NOTIFICATIONS ==========
admin_user = db.query(User).filter(User.email == "admin@yjt.com").first()
if admin_user:
    notif_data = [
        ("Low Stock Alert", "Napier NA295 Piston Ring Seal is below minimum stock (2/5)", "warning"),
        ("New Order Received", "New overhaul order from Hyundai Merchant Marine for MV Hyundai Fortune", "order"),
        ("Inquiry Received", "New inquiry from Maersk Line regarding turbocharger quotation", "inquiry"),
        ("Order Completed", "Service order for MV Pacific Star has been marked as completed", "success"),
        ("Low Stock Alert", "KBB ST27 Casing Half stock is critical (3/2)", "warning"),
        ("System Info", "Weekly database backup completed successfully", "info"),
    ]
    for n in notif_data:
        db.add(Notification(
            id=str(uuid.uuid4()),
            user_id=admin_user.id,
            title=n[0],
            message=n[1],
            type=n[2],
            is_read=False,
            created_at=datetime.utcnow() - timedelta(hours=random.randint(1, 72)),
        ))
    db.commit()
    print(f"Added {len(notif_data)} notifications for admin")

# Final summary
print()
print("=== Final Data Summary ===")
print(f"  Parts: {db.query(Part).count()}")
print(f"  Inventory: {db.query(Inventory).count()}")
print(f"  Customers: {db.query(Customer).count()}")
print(f"  Orders: {db.query(ServiceOrder).count()}")
print(f"  Inquiries: {db.query(Inquiry).count()}")
print(f"  Users: {db.query(User).count()}")
print(f"  Notifications: {db.query(Notification).count()}")
db.close()
print("\nDone! All seed data inserted successfully.")
