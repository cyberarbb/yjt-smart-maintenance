"""Google Sheets 동기화 서비스 - DB 데이터를 Google Sheets로 내보내기"""
import logging
from datetime import datetime
from sqlalchemy.orm import Session

logger = logging.getLogger("uvicorn.error")

# Google Sheets 라이브러리 (선택적 의존성)
try:
    import gspread
    from google.oauth2.service_account import Credentials
    GSPREAD_AVAILABLE = True
except ImportError:
    GSPREAD_AVAILABLE = False


def _get_client(credentials_file: str):
    """Google Sheets API 클라이언트 생성"""
    if not GSPREAD_AVAILABLE:
        raise RuntimeError("gspread 라이브러리가 설치되지 않았습니다. pip install gspread google-auth")
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_file(credentials_file, scopes=scopes)
    return gspread.authorize(creds)


def _ensure_worksheet(spreadsheet, title: str, headers: list[str]):
    """워크시트가 없으면 생성, 있으면 가져오기"""
    try:
        ws = spreadsheet.worksheet(title)
    except gspread.exceptions.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(title=title, rows=1000, cols=len(headers))
    # 헤더 설정
    ws.update(range_name="A1", values=[headers])
    return ws


def sync_parts_to_sheet(db: Session, spreadsheet):
    """Parts + Inventory 데이터를 시트에 동기화"""
    from app.models.part import Part
    from app.models.inventory import Inventory

    headers = ["Part Number", "Name", "Brand", "Turbo Model", "Category", "Unit Price (USD)", "Quantity", "Min Qty", "Warehouse", "Low Stock"]
    ws = _ensure_worksheet(spreadsheet, "Parts & Inventory", headers)

    parts = db.query(Part).all()
    rows = []
    for p in parts:
        inv = db.query(Inventory).filter(Inventory.part_id == p.id).first()
        qty = inv.quantity if inv else 0
        min_qty = inv.min_quantity if inv else 0
        warehouse = inv.warehouse if inv else ""
        low = "YES" if inv and inv.quantity <= inv.min_quantity else "NO"
        rows.append([
            p.part_number, p.name, p.brand, p.turbo_model, p.category,
            p.unit_price, qty, min_qty, warehouse, low,
        ])

    # 기존 데이터 지우고 새로 쓰기 (헤더 제외)
    ws.batch_clear(["A2:Z10000"])
    if rows:
        ws.update(range_name=f"A2:J{len(rows)+1}", values=rows)
    return len(rows)


def sync_orders_to_sheet(db: Session, spreadsheet):
    """Service Orders 데이터를 시트에 동기화"""
    from app.models.service_order import ServiceOrder
    from app.models.customer import Customer

    headers = ["Company", "Contact", "Order Type", "Turbo Brand", "Turbo Model", "Vessel", "Status", "Description", "Created"]
    ws = _ensure_worksheet(spreadsheet, "Service Orders", headers)

    orders = db.query(ServiceOrder).all()
    rows = []
    for o in orders:
        cust = db.query(Customer).filter(Customer.id == o.customer_id).first()
        company = cust.company_name if cust else "Unknown"
        contact = cust.contact_name if cust else ""
        created = o.created_at.strftime("%Y-%m-%d") if o.created_at else ""
        rows.append([
            company, contact, o.order_type, o.turbo_brand, o.turbo_model,
            o.vessel_name or "", o.status, o.description or "", created,
        ])

    ws.batch_clear(["A2:Z10000"])
    if rows:
        ws.update(range_name=f"A2:I{len(rows)+1}", values=rows)
    return len(rows)


def sync_customers_to_sheet(db: Session, spreadsheet):
    """Customers 데이터를 시트에 동기화"""
    from app.models.customer import Customer

    headers = ["Company", "Contact Name", "Email", "Phone", "Country", "Vessel Type", "Registered"]
    ws = _ensure_worksheet(spreadsheet, "Customers", headers)

    customers = db.query(Customer).all()
    rows = []
    for c in customers:
        created = c.created_at.strftime("%Y-%m-%d") if c.created_at else ""
        rows.append([
            c.company_name, c.contact_name, c.email, c.phone or "",
            c.country, c.vessel_type or "", created,
        ])

    ws.batch_clear(["A2:Z10000"])
    if rows:
        ws.update(range_name=f"A2:G{len(rows)+1}", values=rows)
    return len(rows)


def sync_inquiries_to_sheet(db: Session, spreadsheet):
    """Inquiries 데이터를 시트에 동기화"""
    from app.models.inquiry import Inquiry
    from app.models.customer import Customer

    headers = ["Company", "Subject", "Message", "Contact Email", "Resolved", "Response", "Created"]
    ws = _ensure_worksheet(spreadsheet, "Inquiries", headers)

    inquiries = db.query(Inquiry).all()
    rows = []
    for inq in inquiries:
        cust = db.query(Customer).filter(Customer.id == inq.customer_id).first() if inq.customer_id else None
        company = cust.company_name if cust else "N/A"
        created = inq.created_at.strftime("%Y-%m-%d") if inq.created_at else ""
        rows.append([
            company, inq.subject, inq.message[:200], inq.contact_email,
            "YES" if inq.is_resolved else "NO", (inq.response or "")[:200], created,
        ])

    ws.batch_clear(["A2:Z10000"])
    if rows:
        ws.update(range_name=f"A2:G{len(rows)+1}", values=rows)
    return len(rows)


def sync_all(db: Session, credentials_file: str, spreadsheet_id: str) -> dict:
    """전체 데이터를 Google Sheets에 동기화"""
    if not credentials_file or not spreadsheet_id:
        raise ValueError("Google Sheets credentials file and spreadsheet ID are required. Set GOOGLE_SHEETS_CREDENTIALS_FILE and GOOGLE_SHEETS_SPREADSHEET_ID in .env")

    client = _get_client(credentials_file)
    spreadsheet = client.open_by_key(spreadsheet_id)

    results = {
        "parts": sync_parts_to_sheet(db, spreadsheet),
        "orders": sync_orders_to_sheet(db, spreadsheet),
        "customers": sync_customers_to_sheet(db, spreadsheet),
        "inquiries": sync_inquiries_to_sheet(db, spreadsheet),
        "synced_at": datetime.utcnow().isoformat(),
    }

    logger.info(f"Google Sheets sync completed: {results}")
    return results
