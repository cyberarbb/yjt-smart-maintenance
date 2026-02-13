하이브리드 데이터 저장소: Supabase PostgreSQL + Google Sheets 동기화Context
현재 SQLite(로컬 파일)를 사용 중이라 배포 시 데이터가 유실됨.
Supabase PostgreSQL을 메인 DB로, Google Sheets를 보고서/백업용으로 동기화하는 하이브리드 구조로 전환.
좋은 소식: 백엔드가 이미 PostgreSQL을 지원하도록 설계되어 있음

database.py에 QueuePool 설정 완료
psycopg2-binary 의존성 이미 포함
.env의 DATABASE_URL만 변경하면 즉시 전환 가능


Step 1: Supabase PostgreSQL 연결
사전 준비 (사용자):

Supabase 무료 프로젝트 생성 → Connection String 확보

변경 파일:

backend/.env — DATABASE_URL을 Supabase 연결 문자열로 변경
backend/app/routers/analytics.py — strftime() (SQLite 전용) → DB 호환 방식으로 수정 (Python datetime 사용)

작업:

.env의 DATABASE_URL을 postgresql+psycopg2://postgres.[ref]:[password]@aws-0-ap-northeast-2.pooler.supabase.com:6543/postgres 로 변경
analytics.py의 strftime → Python에서 월별 그룹핑으로 변경 (DB 함수 의존 제거)
서버 재시작 → Base.metadata.create_all()이 Supabase에 테이블 자동 생성
seed_phase2.py 실행으로 초기 데이터 투입


Step 2: Google Sheets 동기화 서비스
새 의존성 (requirements.txt):

gspread>=6.0 — Google Sheets Python 라이브러리
google-auth>=2.0 — 서비스 계정 인증

사전 준비 (사용자):

Google Cloud Console → Sheets API 활성화
서비스 계정 생성 → JSON 키 다운로드
Google Sheets 스프레드시트 생성 (5개 시트: Parts, Orders, Customers, Inquiries, Inventory)
서비스 계정 이메일에 편집 권한 부여

새 파일:

backend/app/services/google_sheets_service.py — Google Sheets API 연동

sync_parts_to_sheet() — Parts + Inventory 동기화
sync_orders_to_sheet() — Service Orders 동기화
sync_customers_to_sheet() — Customers 동기화
sync_inquiries_to_sheet() — Inquiries 동기화
sync_all() — 전체 동기화


backend/app/routers/sync.py — POST /api/sync/sheets (관리자 전용)

변경 파일:

backend/app/config.py — Google Sheets 관련 설정 추가 (GOOGLE_SHEETS_CREDENTIALS_FILE, GOOGLE_SHEETS_SPREADSHEET_ID)
backend/app/main.py — sync 라우터 등록


Step 3: 프론트엔드 동기화 버튼
변경 파일:

frontend/src/lib/api.ts — syncToSheets() API 함수 추가
frontend/src/app/analytics/page.tsx — "Sync to Google Sheets" 버튼 추가 (Export Report 옆)


전체 수정/생성 파일 목록
파일유형변경 내용backend/.env수정DATABASE_URL + Google Sheets 설정backend/app/config.py수정Google Sheets 설정 필드 추가backend/app/routers/analytics.py수정strftime → DB 호환 방식backend/app/main.py수정sync 라우터 등록backend/requirements.txt수정gspread, google-auth 추가backend/app/services/google_sheets_service.py신규Sheets API 연동 서비스backend/app/routers/sync.py신규동기화 엔드포인트frontend/src/lib/api.ts수정syncToSheets 함수 추가frontend/src/app/analytics/page.tsx수정Sync 버튼 추가

검증 방법

Supabase 대시보드에서 7개 테이블 생성 확인
curl로 모든 API 엔드포인트 200 OK 확인 (특히 analytics의 monthly-orders)
프론트엔드에서 데이터 정상 표시 확인
"Sync to Google Sheets" 버튼 클릭 → Google Sheets에 데이터 반영 확인
백엔드 재시작 후에도 데이터 유지 확인 (SQLite와 달리 영속적)