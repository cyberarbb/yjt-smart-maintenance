#!/usr/bin/env bash
# Buzz 릴레이 자체 호스팅 부트스트랩.
#
# block/buzz 저장소를 내려받고, deploy/compose/.env 에 들어갈 모든 시크릿을
# 생성한 뒤(릴레이 서명키 / 오너 Nostr 키쌍 / DB·Redis·S3 비밀번호),
# 곧바로 기동 가능한 상태로 만들어 둔다.
#
# 필요 도구: docker (compose v2.24.4+), git, openssl
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATE_FILE="${SCRIPT_DIR}/.buzz-env"
SECRETS_DIR="${SCRIPT_DIR}/secrets"

BUZZ_SRC="${BUZZ_SRC:-${HOME}/buzz}"
BUZZ_IMAGE="${BUZZ_IMAGE:-ghcr.io/block/buzz:main}"
BUZZ_REF="${BUZZ_REF:-main}"
DOMAIN=""
MODE="tls"   # tls | plain | local
FORCE="false"

usage() {
  cat <<'MSG'
사용법: ./bootstrap.sh --domain <도메인> [옵션]

옵션:
  --domain <host>   릴레이 공개 도메인 (예: buzz.yjt.co.kr). --local 이면 생략 가능
  --local           localhost 로컬 검증용 설정 (ws://localhost:3000, TLS 없음)
  --plain           도메인은 쓰되 TLS 종단은 외부(기존 nginx/LB)에서 처리
  --src <path>      buzz 소스를 둘 경로 (기본: ~/buzz, 환경변수 BUZZ_SRC)
  --ref <git-ref>   클론할 브랜치/태그 (기본: main)
  --image <image>   릴레이 이미지 (기본: ghcr.io/block/buzz:main)
  --force           이미 존재하는 .env 를 덮어씀 (기존 시크릿 폐기 — 주의)
  -h, --help        도움말

예:
  ./bootstrap.sh --domain buzz.yjt.co.kr
  ./bootstrap.sh --local
MSG
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --domain) DOMAIN="${2:?--domain 값이 필요합니다}"; shift 2 ;;
    --local)  MODE="local"; shift ;;
    --plain)  MODE="plain"; shift ;;
    --src)    BUZZ_SRC="${2:?--src 값이 필요합니다}"; shift 2 ;;
    --ref)    BUZZ_REF="${2:?--ref 값이 필요합니다}"; shift 2 ;;
    --image)  BUZZ_IMAGE="${2:?--image 값이 필요합니다}"; shift 2 ;;
    --force)  FORCE="true"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "알 수 없는 옵션: $1" >&2; usage >&2; exit 1 ;;
  esac
done

if [[ "${MODE}" == "local" ]]; then
  DOMAIN="localhost"
fi
if [[ -z "${DOMAIN}" ]]; then
  echo "오류: --domain 을 지정하거나 --local 을 사용하세요." >&2
  exit 1
fi

for cmd in docker git openssl awk; do
  command -v "${cmd}" >/dev/null 2>&1 || { echo "오류: '${cmd}' 가 필요합니다." >&2; exit 1; }
done
docker compose version >/dev/null 2>&1 || { echo "오류: docker compose v2 가 필요합니다." >&2; exit 1; }

# 1. 소스 확보 --------------------------------------------------------------
if [[ -d "${BUZZ_SRC}/.git" ]]; then
  echo "==> 기존 소스 사용: ${BUZZ_SRC}"
else
  echo "==> block/buzz 클론 → ${BUZZ_SRC} (ref=${BUZZ_REF})"
  git clone --depth 1 --branch "${BUZZ_REF}" https://github.com/block/buzz.git "${BUZZ_SRC}"
fi

COMPOSE_DIR="${BUZZ_SRC}/deploy/compose"
ENV_FILE="${COMPOSE_DIR}/.env"
[[ -f "${COMPOSE_DIR}/.env.example" ]] || { echo "오류: ${COMPOSE_DIR}/.env.example 이 없습니다." >&2; exit 1; }

if [[ -f "${ENV_FILE}" && "${FORCE}" != "true" ]]; then
  echo "이미 ${ENV_FILE} 가 있습니다. 기존 시크릿을 유지하려면 그대로 두고,"
  echo "정말 새로 만들려면 --force 를 붙여 다시 실행하세요."
  exit 1
fi

# 2. 키/시크릿 생성 ---------------------------------------------------------
echo "==> 릴레이 이미지 준비 (키 생성에 buzz-admin 사용): ${BUZZ_IMAGE}"
docker pull -q "${BUZZ_IMAGE}" >/dev/null

gen_key() {
  docker run --rm --entrypoint /usr/local/bin/buzz-admin "${BUZZ_IMAGE}" generate-key
}

echo "==> 릴레이 서명 키쌍 생성"
RELAY_GEN="$(gen_key)"
RELAY_SK="$(echo "${RELAY_GEN}" | awk '/Secret key:/ {print $3}')"
RELAY_PK="$(echo "${RELAY_GEN}" | awk '/Public key:/ {print $3}')"

echo "==> 오너(관리자) 키쌍 생성"
OWNER_GEN="$(gen_key)"
OWNER_SK="$(echo "${OWNER_GEN}" | awk '/Secret key:/ {print $3}')"
OWNER_PK="$(echo "${OWNER_GEN}" | awk '/Public key:/ {print $3}')"

for v in RELAY_SK RELAY_PK OWNER_SK OWNER_PK; do
  [[ -n "${!v}" ]] || { echo "오류: ${v} 생성 실패 (buzz-admin generate-key 출력 확인 필요)" >&2; exit 1; }
done

rand_hex() { openssl rand -hex "${1:-32}"; }

GIT_HMAC="$(rand_hex 32)"
PG_PASSWORD="$(rand_hex 24)"
REDIS_PASSWORD="$(rand_hex 24)"
S3_ACCESS_KEY="$(rand_hex 12)"
S3_SECRET_KEY="$(rand_hex 32)"

# 3. .env 작성 --------------------------------------------------------------
case "${MODE}" in
  local)
    RELAY_URL="ws://localhost:3000"
    MEDIA_BASE_URL="http://localhost:3000/media"
    CORS_ORIGINS="http://localhost:3000"
    ;;
  *)
    RELAY_URL="wss://${DOMAIN}"
    MEDIA_BASE_URL="https://${DOMAIN}/media"
    CORS_ORIGINS="https://${DOMAIN}"
    ;;
esac

umask 077
cat > "${ENV_FILE}" <<EOF
# infra/buzz/bootstrap.sh 가 생성한 파일입니다. 여기 있는 값은 재시작 사이에
# 절대 바뀌면 안 됩니다(키가 바뀌면 기존 이벤트 검증/멤버십이 깨집니다).
BUZZ_IMAGE=${BUZZ_IMAGE}

BUZZ_DOMAIN=${DOMAIN}
RELAY_URL=${RELAY_URL}
BUZZ_MEDIA_BASE_URL=${MEDIA_BASE_URL}
BUZZ_MEDIA_SERVER_DOMAIN=${DOMAIN}
BUZZ_CORS_ORIGINS=${CORS_ORIGINS}

BUZZ_REQUIRE_AUTH_TOKEN=true
BUZZ_REQUIRE_RELAY_MEMBERSHIP=true
BUZZ_ALLOW_NIP_OA_AUTH=true
BUZZ_AUTO_MIGRATE=true
BUZZ_GIT_CONFORMANCE_PROBE=true
RUST_LOG=buzz_relay=info,buzz_db=info,buzz_auth=info,buzz_pubsub=info,tower_http=info

RELAY_OWNER_PUBKEY=${OWNER_PK}

BUZZ_RELAY_PRIVATE_KEY=${RELAY_SK}
BUZZ_GIT_HOOK_HMAC_SECRET=${GIT_HMAC}
POSTGRES_DB=buzz
POSTGRES_USER=buzz
POSTGRES_PASSWORD=${PG_PASSWORD}
REDIS_PASSWORD=${REDIS_PASSWORD}
BUZZ_S3_ACCESS_KEY=${S3_ACCESS_KEY}
BUZZ_S3_SECRET_KEY=${S3_SECRET_KEY}
BUZZ_S3_BUCKET=buzz-media
BUZZ_S3_ADDRESSING_STYLE=path

BUZZ_HTTP_PORT=3000

CADDY_HTTP_PORT=80
CADDY_HTTPS_PORT=443

POSTGRES_PORT=5432
REDIS_PORT=6379
MINIO_API_PORT=9000
MINIO_CONSOLE_PORT=9001
ADMINER_PORT=8082
PROMETHEUS_PORT=9090
EOF
chmod 600 "${ENV_FILE}"

# 4. 오너 키 백업 (커밋 금지 — .gitignore 로 차단됨) -------------------------
mkdir -p "${SECRETS_DIR}"
OWNER_FILE="${SECRETS_DIR}/owner-key.txt"
cat > "${OWNER_FILE}" <<EOF
# Buzz 오너(관리자) 신원. 이 개인키를 잃어버리면 관리자 권한을 복구할 수 없습니다.
# 비밀번호 관리자(1Password 등)에 옮겨 두고 이 파일은 지우는 것을 권장합니다.
생성일: $(date -u +%Y-%m-%dT%H:%M:%SZ)
도메인: ${DOMAIN}
OWNER_PUBLIC_KEY=${OWNER_PK}
OWNER_SECRET_KEY=${OWNER_SK}
RELAY_PUBLIC_KEY=${RELAY_PK}
EOF
chmod 600 "${OWNER_FILE}"

cat > "${STATE_FILE}" <<EOF
# manage.sh 가 읽는 상태 파일 (bootstrap.sh 생성)
BUZZ_SRC=${BUZZ_SRC}
BUZZ_MODE=${MODE}
BUZZ_DOMAIN=${DOMAIN}
BUZZ_RELAY_URL=${RELAY_URL}
EOF
chmod 600 "${STATE_FILE}"
umask 022

cat <<MSG

완료했습니다.

  소스        : ${BUZZ_SRC}
  설정 파일   : ${ENV_FILE}
  오너 공개키 : ${OWNER_PK}
  오너 개인키 : ${OWNER_FILE}  ← 지금 바로 안전한 곳에 옮기세요

다음 단계:
  1) 기동          : ./manage.sh start
  2) 상태 확인     : ./manage.sh status  /  ./manage.sh health
  3) 팀원 추가     : ./manage.sh add-member <npub 또는 64자리 hex>
  4) 에이전트 연결 : agent/README 절차 (infra/buzz/README.md 6장)
MSG

if [[ "${MODE}" == "tls" ]]; then
  echo
  echo "TLS 모드입니다. ${DOMAIN} 의 A/AAAA 레코드가 이 서버를 가리키고 80/443 이"
  echo "열려 있어야 Let's Encrypt 발급이 됩니다. (manage.sh 가 Caddy 오버레이를 자동 적용)"
fi
